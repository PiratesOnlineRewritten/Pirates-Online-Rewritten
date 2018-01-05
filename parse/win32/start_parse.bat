@echo off
title Project Toontown - Parse

rem Verify npm is on the PATH
WHERE npm
IF %ERRORLEVEL% NEQ 0 (
    ECHO npm was not found. Is NodeJS in your Path variable? 
    pause
    goto :eof 
)

rem Start Parse
echo Starting Project Toontown Parse server
:parse
cd ../
npm start
pause
goto :parse