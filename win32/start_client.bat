@echo off
title Pirates Online Rewritten - Client

echo Choose your server
echo #1 - Localhost
echo #2 - Dev Server
echo #3 - Custom

:selection

set INPUT=-1
set /P INPUT=Selection: 

if %INPUT%==1 (
    set POR_GAMESERVER=127.0.0.1
) else if %INPUT%==2 (
    set POR_GAMESERVER=game.dev.piratesrewritten.com
) else if %INPUT%==3 (
    set /P POR_GAMESERVER=Gameserver: 
) else (
    goto selection
)
title Pirates Online Rewritten - Client (%POR_GAMESERVER%)

set GAME_INGAME_MANAGE_ACCT=http://www.piratesrewritten.com/account

set /P POR_TOKEN=Token (Default: dev): || ^
set POR_TOKEN=dev

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
