@echo off
title Pirates Online Rewritten - Client

rem Server address input selection
echo Choose your server (Default: Localhost)
echo #1 - Localhost
echo #2 - Production Server
echo #3 - Dev Server
echo #4 - Custom

:selection

set INPUT=-1
set /P INPUT=Selection: 

if %INPUT%==1 (
    set POR_GAMESERVER=127.0.0.1
) else if %INPUT%==2 (
    set POR_GAMESERVER=game.piratesrewritten.com
) else if %INPUT%==3 (
    set POR_GAMESERVER=game.dev.piratesrewritten.com
) else if %INPUT%==4 (
    set /P POR_GAMESERVER=Gameserver: 
) else (
    set POR_GAMESERVER=127.0.0.1
)
title Pirates Online Rewritten - Client (%POR_GAMESERVER%)

rem set website urls
set GAME_INGAME_MANAGE_ACCT=http://www.piratesrewritten.com/account

rem PlayToken input
set /P POR_TOKEN=Token (Default: dev): || ^
set POR_TOKEN=dev

echo ====================================
echo Starting Pirates Online Rewritten...
echo Token: %POR_TOKEN%
echo Gameserver: %POR_GAMESERVER%
echo ====================================

cd ../

rem Start the game; Use ppython2 if available
:main
ppython2 -h >nul 2>&1 && (
    ppython2 -m pirates.piratesbase.PiratesStart >> pirates-dev-log.txt
) || (
    ppython -m pirates.piratesbase.PiratesStart >> pirates-dev-log.txt
)
pause
goto :main
