# Atelier 01 — luxury watch service website

Готовый статический сайт. Открывайте через локальный веб-сервер, чтобы видео и вложенные страницы работали одинаково во всех браузерах.

## На Mac
1. Дважды кликните `start.command`.
2. Откроется `http://localhost:8080`.
3. Для остановки сервера закройте окно Terminal или нажмите `Ctrl+C`.

## Видео
- `assets/videos/hero-watch.mp4` — главное видео.
- `assets/videos/watchmaker.mp4` — мастер за работой.
- `assets/videos/detail-01.mp4` — макро 1.
- `assets/videos/detail-02.mp4` — макро 2.
- `assets/videos/detail-03.mp4` — макро 3.

Главное видео физически НЕ перекодировано в ЧБ. Монохромный характер задаёт CSS в `assets/css/styles.css`:

```css
.hero-media video {
  filter: grayscale(.96) saturate(.15) contrast(1.12) brightness(.62);
}
```

Чтобы вернуть цвет — замените `grayscale(.96)` на `grayscale(0)` и `saturate(.15)` на `saturate(1)`.

## Перед публикацией
Смотрите `TODO-CONTENT.md`.
