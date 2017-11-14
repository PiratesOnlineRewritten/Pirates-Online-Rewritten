@echo off
title Pirates Online Rewritten - AI
cd ../../

rem Get the user input:
set /P DISTRICT_NAME=District name (DEFAULT: DevHaven): || ^
set DISTRICT_NAME=DevHaven
set /P BASE_CHANNEL=Base channel (DEFAULT: 401000000):  || ^
set BASE_CHANNEL=401000000

title Pirates Online Rewritten - AI (%DISTRICT_NAME%)

rem Choose correct python command to execute the game
set PYTHON_CMD=ppython

echo =============================================
echo Starting Pirates Online Rewritten District...
echo District Name: %DISTRICT_NAME%
echo Base channel: %BASE_CHANNEL%
echo ============================================

rem Start AI server
:main
%PYTHON_CMD% -m pirates.ai.ServiceStart --base-channel %BASE_CHANNEL% ^
    --district-name "%DISTRICT_NAME%"
goto main