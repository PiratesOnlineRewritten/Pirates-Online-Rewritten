@echo off
title Pirates Online Rewritten - Client

set /P POR_USERNAME=Username: 
set POR_GAMESERVER="127.0.0.1"

cd ../

:main
ppython2 -h >nul 2>&1 && (
    ppython2 -m pirates.piratesbase.PiratesStart
) || (
    ppython -m pirates.piratesbase.PiratesStart
)
pause
goto :goto
