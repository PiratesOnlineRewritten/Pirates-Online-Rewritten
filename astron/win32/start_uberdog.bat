@echo off
title Pirates Online Rewritten - UberDOG
cd ../../

rem Choose correct python command to execute the game
set PYTHON_CMD=ppython

echo ====================================
echo Starting Pirates Online Rewritten...
echo PPython: %PYTHON_CMD%
echo ====================================

rem Start AI server
:main
%PYTHON_CMD% -m pirates.uberdog.ServiceStart 
goto main