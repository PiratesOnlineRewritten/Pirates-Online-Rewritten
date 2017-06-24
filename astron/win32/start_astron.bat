@echo off
title Pirates Online Rewritten - Astron Cluster
cd ../

:main
astrond.exe --loglevel debug config/astrond.yml
goto main
