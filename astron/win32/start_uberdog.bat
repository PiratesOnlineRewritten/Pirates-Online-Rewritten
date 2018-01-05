@echo off
title Pirates Online Rewritten - UberDOG
cd ../../

rem Choose correct python command to execute the game
set PYTHON_CMD=ppython

echo ============================================
echo Starting Pirates Online Rewritten UberDOG...
echo PPython: %PYTHON_CMD%
echo ============================================

rem Start UberDOG server
:main
%PYTHON_CMD% -m pirates.uberdog.ServiceStart --parse-hostname http://127.0.0.1:1337/por-parse
goto main