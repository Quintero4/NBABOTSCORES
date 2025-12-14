@echo off
REM Navega a la carpeta donde está el script
cd C:\Users\Fernando\desktop\

REM Ejecuta el script de Python usando la ruta exacta: C:\Users\Fernando\AppData\Local\Programs\Python\Python313\python.exe
"C:\Users\Fernando\AppData\Local\Programs\Python\Python313\python.exe" nba_bot.py

REM El timeout mantiene la ventana abierta 5 segundos por si hay algún error
timeout /t 5 /nobreak