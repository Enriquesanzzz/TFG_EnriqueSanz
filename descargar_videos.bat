@echo off
echo =============================
echo   DESCARGADOR MASIVO YT-DLP
echo =============================

:: Instalar yt-dlp si no está
python -m pip install -U yt-dlp

:: Usar carpeta de salida personalizada
set "CARPETA_SALIDA=C:\Users\Enrique Sanz Tur\Desktop\TFG\Videos"

:: Crear carpeta si no existe
if not exist "%CARPETA_SALIDA%" mkdir "%CARPETA_SALIDA%"

:: Descargar vídeos desde urls.txt
python -m yt_dlp -a "C:\Users\Enrique Sanz Tur\Desktop\TFG\urls.txt" --recode-video mp4 -P "%CARPETA_SALIDA%"

:: Renombrar vídeos como control1.mp4, control2.mp4...
echo Renombrando vídeos...
setlocal enabledelayedexpansion
set count=3000
for %%f in ("%CARPETA_SALIDA%\*.mp4") do (
    ren "%%f" "Autismo!count!.mp4"
    set /a count+=1
)

echo -----------------------------
echo Todo listo. Revisa la carpeta: %CARPETA_SALIDA%
pause
