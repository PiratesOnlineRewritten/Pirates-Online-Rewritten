@echo off
title Pirates Online Rewritten - Client

set /P POR_USERNAME=Username: 
set POR_GAMESERVEr="127.0.0.1"

cd ../

:goto
ppython -m pirates.piratesbase.PiratesStart
pause
goto :goto
