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

rem Set website urls
set GAME_INGAME_MANAGE_ACCT=http://www.piratesrewritten.com/account
set GAME_INGAME_UPGRADE=http://www.piratesrewritten.com/
set GAME_INGAME_MOREINFO=http://www.piratesrewritten.com/about/
set GAME_INGAME_NAMING=http://www.piratesrewritten.com/piratecode/

rem Set Patcher urls
set GAME_PATCHER_FILE_OPTIONS patcher.ver

rem PlayToken input
set /P POR_TOKEN=Token (Default: dev): || ^
set POR_TOKEN=dev

rem Choose correct python command to execute the game
ppython2 -h >nul 2>&1 && (
    set PYTHON_CMD=ppython2
) || (
    set PYTHON_CMD=ppython
)

rem Log file path
set LOG_FILE=pirates-dev-log.txt

echo ====================================
echo Starting Pirates Online Rewritten...
echo Token: %POR_TOKEN%
echo Gameserver: %POR_GAMESERVER%
echo PPython: %PYTHON_CMD%
echo ====================================

cd ../

rem Start the game using the PYTHON_CMD variable
:main
%PYTHON_CMD% -m pirates.piratesbase.PiratesStart >> %LOG_FILE%
pause
goto :main
