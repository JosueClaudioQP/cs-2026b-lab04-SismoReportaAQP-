@echo off
cd /d "%~dp0"
set "TYPST_FONT_PATHS=%~dp0fonts"
unsarep docs build lab-08
pause
