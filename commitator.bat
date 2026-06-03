@echo off
chcp 65001 > nul
echo === Quick commit ===
git status
echo Добавление файлов...
git add .
if "%commit_message%"=="" set commit_message="Auto commit from %date% at %time%"
git commit -m "%commit_message%"
echo Отправка на GitHub...
git push origin main

echo === ГОТОВО! ===
pause
