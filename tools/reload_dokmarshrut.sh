#!/bin/bash
set -euo pipefail
BIN="/Applications/1cv8t.localized/8.5.1.1150/1cv8t.app/Contents/MacOS/1cv8t"
BASE="/Users/damir/Documents/хакатоны/1С/bases/ДокМаршрут"
SRC="/Users/damir/Documents/хакатоны/1С/src/ДокМаршрут"
LOG="/Users/damir/Documents/хакатоны/1С/bases/dok_must_reload.log"
cd "/Users/damir/Documents/хакатоны/1С"
pkill -9 -f '1cv8t' 2>/dev/null || true
pkill -9 -f '1cv8ct' 2>/dev/null || true
sleep 2
python3 tools/build_dokmarshrut.py
rm -f "$LOG"
"$BIN" DESIGNER /F"$BASE" /LoadConfigFromFiles "$SRC" /UpdateDBCfg /Out "$LOG" /DisableStartupDialogs
EC=$?
echo EXIT:$EC
echo "----- LOG -----"
tail -40 "$LOG" || true
if grep -qiE 'исключение|ошибка|error|XDTO' "$LOG" 2>/dev/null; then
  echo "FAIL: в логе есть ошибка — конфигурация НЕ обновилась"
  exit 1
fi
if ! grep -q 'успешно завершено\|Конфигурация обновлена' "$LOG" 2>/dev/null; then
  echo "FAIL: нет подтверждения успешного обновления"
  exit 1
fi
ls -la "$BASE/1Cv8.1CD"
echo OK
exit $EC
