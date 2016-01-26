@ECHO off

set install_path=dist\LousaDigital

ECHO Executando pyinstaller...
python PyInstaller-3.1\pyinstaller.py --windowed main.spec

ECHO \nPyinstaller finalizado.

ECHO Copiando dependencias...
xcopy dependencies\* /Y /E %install_path%

ECHO Copiando glade...
mkdir %install_path%\glade
xcopy src\glade\* /Y /E %install_path%\glade

ECHO Copiando imagens e web resources...
xcopy src\icon.png /Y /E %install_path%
mkdir %install_path%\www
xcopy src\www\* /Y /E %install_path%\www

ECHO Copiando libs...
xcopy src\lib\* /Y /E %install_path%\lib

ECHO Copiando banco de dados
mkdir %install_path%\.db
xcopy src\.db\* /Y /E %install_path%\.db

ECHO Final de execucao!

pause