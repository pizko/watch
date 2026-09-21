#!/bin/bash
cd "$(dirname "$0")"
(open http://localhost:8080 >/dev/null 2>&1 &) 
python3 -m http.server 8080 --bind 127.0.0.1
