@echo off
title Pirates Online Rewritten - UberDOG
cd ../../

:main
ppython -m pirates.uberdog.ServiceStart
goto main