<?php
/**
 * Заявки с часовое-ателье.рф → Telegram.
 * Токен и chat_id лежат ВНЕ webroot: ../lead_config.php (return ['bot_token' => ..., 'chat_id' => ...]).
 * Копия каждой заявки — ../leads.log. Защита: скрытое поле, время заполнения, не больше 5 заявок в час с одного IP.
 * Совместим с PHP 5.6.
 */
header('Content-Type: application/json; charset=utf-8');
header('X-Robots-Tag: noindex, nofollow');

function out($code, $data)
{
    http_response_code($code);
    echo json_encode($data, JSON_UNESCAPED_UNICODE);
    exit;
}

function field($key, $max)
{
    $v = isset($_POST[$key]) ? (string) $_POST[$key] : '';
    $v = trim(preg_replace('/[ \t]+/u', ' ', strip_tags($v)));
    return mb_substr($v, 0, $max, 'UTF-8');
}

if (!isset($_SERVER['REQUEST_METHOD']) || $_SERVER['REQUEST_METHOD'] !== 'POST') {
    out(405, array('ok' => false, 'error' => 'method'));
}

// Боты заполняют скрытое поле — делаем вид, что всё хорошо.
if (field('website', 100) !== '') {
    out(200, array('ok' => true));
}

// Форма отправлена быстрее, чем человек успел бы её заполнить, или страница открыта слишком давно.
$ts = (int) field('ts', 12);
$age = time() - $ts;
if ($ts <= 0 || $age < 3 || $age > 86400) {
    out(422, array('ok' => false, 'error' => 'Обновите страницу и отправьте заявку ещё раз.'));
}

$phone = field('phone', 40);
$name = field('name', 80);
$message = field('message', 1000);
$digits = preg_replace('/\D/', '', $phone);
if (strlen($digits) < 10 || strlen($digits) > 15) {
    out(422, array('ok' => false, 'error' => 'Укажите номер телефона, чтобы мастер мог перезвонить.'));
}

$base = dirname(__DIR__);

// Лимит по IP: не больше 5 заявок в час.
$ip = isset($_SERVER['HTTP_X_REAL_IP']) ? $_SERVER['HTTP_X_REAL_IP'] : (isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : '');
$rlDir = $base . '/lead_rl';
if (!is_dir($rlDir)) {
    @mkdir($rlDir, 0700);
}
$rlFile = $rlDir . '/' . md5($ip);
$hits = array();
if (is_file($rlFile)) {
    foreach (explode("\n", (string) @file_get_contents($rlFile)) as $t) {
        if ($t !== '' && time() - (int) $t < 3600) {
            $hits[] = (int) $t;
        }
    }
}
if (count($hits) >= 5) {
    out(429, array('ok' => false, 'error' => 'Слишком много заявок подряд. Позвоните нам, пожалуйста.'));
}
$hits[] = time();
@file_put_contents($rlFile, implode("\n", $hits), LOCK_EX);

$page = isset($_SERVER['HTTP_REFERER']) ? mb_substr((string) $_SERVER['HTTP_REFERER'], 0, 300, 'UTF-8') : '';
$text = "⌚ Заявка с часовое-ателье.рф\n"
    . "Телефон: " . $phone . "\n"
    . ($name !== '' ? "Имя: " . $name . "\n" : '')
    . ($message !== '' ? "Сообщение: " . $message . "\n" : '')
    . ($page !== '' ? "Страница: " . rawurldecode($page) . "\n" : '')
    . "Время: " . date('d.m.Y H:i');

@file_put_contents($base . '/leads.log', date('c') . "\t" . str_replace("\n", ' | ', $text) . "\n", FILE_APPEND | LOCK_EX);

$cfg = @include $base . '/lead_config.php';
if (!is_array($cfg) || empty($cfg['bot_token']) || empty($cfg['chat_id'])) {
    // Заявка сохранена в лог, но в Telegram не ушла — человеку всё равно отвечаем успехом.
    out(200, array('ok' => true));
}

$ctx = stream_context_create(array('http' => array(
    'method' => 'POST',
    'header' => "Content-Type: application/x-www-form-urlencoded\r\n",
    'content' => http_build_query(array('chat_id' => $cfg['chat_id'], 'text' => $text, 'disable_web_page_preview' => 'true')),
    'timeout' => 10,
    'ignore_errors' => true,
)));
$res = @file_get_contents('https://api.telegram.org/bot' . $cfg['bot_token'] . '/sendMessage', false, $ctx);
$json = $res ? json_decode($res, true) : null;
if (!is_array($json) || empty($json['ok'])) {
    @file_put_contents($base . '/leads.log', date('c') . "\tTELEGRAM_FAIL\t" . substr((string) $res, 0, 200) . "\n", FILE_APPEND | LOCK_EX);
}
out(200, array('ok' => true));
