@echo off
title Pirates Online Rewritten - AI
cd ../../

:main
ppython2 -h >nul 2>&1 && (
    ppython2 -m pirates.ai.ServiceStart
) || (
    ppython -m pirates.ai.ServiceStart
)
goto main