@echo off
echo ===============================
echo   DESCARGADOR MASIVO TIKTOK
echo ===============================

:: Instalar yt-dlp si no está
python -m pip install -U yt-dlp

:: Usar carpeta de salida personalizada
set "CARPETA_SALIDA=C:\Users\Enrique Sanz Tur\Desktop\TFG\Videos"

:: Crear carpeta si no existe
if not exist "%CARPETA_SALIDA%" mkdir "%CARPETA_SALIDA%"

:: Descargar vídeos desde archivo específico
python -m yt_dlp -a "C:\Users\Enrique Sanz Tur\Desktop\TFG\urls_tiktok.txt" -P "%CARPETA_SALIDA%" --user-agent "Mozilla/5.0"

:: Renombrar vídeos
echo Renombrando vídeos...
setlocal enabledelayedexpansion
set count=1
for %%f in ("%CARPETA_SALIDA%\*.mp4") do (
    ren "%%f" "Control!count!.mp4"
    set /a count+=1
)

echo -----------------------------
echo Todo listo. Revisa la carpeta: %CARPETA_SALIDA%
pause
