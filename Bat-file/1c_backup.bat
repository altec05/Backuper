chcp 65001

@echo off

SET LOG=%ROOT%log.txt
echo Log-файл: %LOG%.

SET ROOT=%~dp0
echo Текущая директория скрипта: %ROOT%. Путь конечного копирования начнется из этой директории!

SET COPY_TO=%ROOT%zup83
SET COPY_FROM=\\192.168.15.5\SQLBackup\zup83

echo Конечная папка: %COPY_TO%.
echo Копируем из папки: %COPY_FROM%.

dir %COPY_TO%
if errorlevel 1 ( 
echo Конечная папка %COPY_TO% не существует! Создаем.
MKDIR %COPY_TO%
echo Конечная папка %COPY_TO% создана!
 ) else ( 
echo Конечная папка уже %COPY_TO% существует.
Echo Удаляем все файлы в %COPY_TO%
DEL "%COPY_TO%\*" /F /Q /A

Echo Удаляем все директории в %COPY_TO%
FOR /F "eol=| delims=" %%I in ('dir "%COPY_TO%\*" /AD /B 2^>nul') do RMDIR /Q /S "%COPY_TO%\%%I"
@ECHO Конечная папка "%COPY_TO%" очищена.
 )

robocopy "%COPY_FROM%" "%COPY_TO%" *.* /J /FFT /MAXAGE:1

SET COPY_TO=%ROOT%bgu83
SET COPY_FROM=\\192.168.15.5\SQLBackup\bgu83

echo Конечная папка: %COPY_TO%.
echo Копируем из папки: %COPY_FROM%.

dir %COPY_TO%
if errorlevel 1 ( 
echo Конечная папка %COPY_TO% не существует! Создаем.
MKDIR %COPY_TO%
echo Конечная папка %COPY_TO% создана!
 ) else ( 
echo Конечная папка уже %COPY_TO% существует.
Echo Удаляем все файлы в %COPY_TO%
DEL "%COPY_TO%\*" /F /Q /A

Echo Удаляем все директории в %COPY_TO%
FOR /F "eol=| delims=" %%I in ('dir "%COPY_TO%\*" /AD /B 2^>nul') do RMDIR /Q /S "%COPY_TO%\%%I"
@ECHO Конечная папка "%COPY_TO%" очищена.
 )

robocopy "%COPY_FROM%" "%COPY_TO%" *.* /J /FFT /MAXAGE:1
 
echo ------Копирование завершено! Подтвердите закрытие двойным нажатием "Enter"------
echo.
echo.

pause

@echo on


