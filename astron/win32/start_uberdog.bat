@echo off
title Pirates Online Rewritten - UberDOG
cd ../../

:main
:main
ppython2 -h >nul 2>&1 && (
    ppython2 -m pirates.uberdog.ServiceStart
) || (
    ppython -m pirates.uberdog.ServiceStart
)
goto main