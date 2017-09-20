@echo off
title Pirates Online Rewritten - Client

set GAME_INGAME_MANAGE_ACCT=http://www.piratesrewritten.com/account

set POR_GAMESERVER=127.0.0.1
set /P POR_TOKEN=Token (Default: dev): || ^
set POR_TOKEN=dev
echo.

echo ====================================
echo Starting Pirates Online Rewritten...
echo Token: %POR_TOKEN%
echo Gameserver: %POR_GAMESERVER%
echo ====================================

cd ../

:main
ppython2 -h >nul 2>&1 && (
    ppython2 -m pirates.piratesbase.PiratesStart
) || (
    ppython -m pirates.piratesbase.PiratesStart
)
pause
goto :main
