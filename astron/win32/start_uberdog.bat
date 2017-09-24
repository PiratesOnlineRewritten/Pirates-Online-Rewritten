@echo off
title Pirates Online Rewritten - UberDOG
cd ../../

rem Choose correct python command to execute the game
ppython -h >nul 2>&1 && (
    set PYTHON_CMD=C:\Panda3D-1.10.0\python\ppython.exe
) || (
    set PYTHON_CMD=ppython2
) || (
    set PYTHON_CMD=ppython
) || (
    set PYTHON_CMD=python
)

echo ====================================
echo Starting Pirates Online Rewritten...
echo PPython: %PYTHON_CMD%
echo ====================================

rem Start AI server
:main
%PYTHON_CMD% -m pirates.uberdog.ServiceStart 
goto main