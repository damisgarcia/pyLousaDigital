#!/bin/bash
# @autor: Damis Garcia

echo "Criando diretórios"
mkdir -p $HOME/digitalclass/DEBIAN/usr/lib/digitalclass
mkdir -p $HOME/digitalclass/DEBIAN/usr/share
mkdir -p $HOME/digitalclass/DEBIAN/usr/share/applications
mkdir -p $HOME/digitalclass/DEBIAN/usr/share/icons/hicolor/48x48/apps

echo "Copiando Manifesto ..."
cp control $HOME/digitalclass/DEBIAN/
echo "Copiando Instalador de Depêndencias ..."
cp preinst $HOME/digitalclass/DEBIAN
cp digitalclass.desktop $HOME/digitalclass/DEBIAN/usr/share/applications
cp digitalclass.png $HOME/digitalclass/DEBIAN/usr/share/icons/hicolor/48x48/apps
echo "Copiando Projeto ..."
cp -r ../src/ $HOME/digitalclass/DEBIAN/usr/lib/digitalclass
# To Compact Folder
cd $HOME/digitalclass/DEBIAN/
tar -zcf usr.tar usr
gzip -9 usr.tar
rm -r $HOME/digitalclass/DEBIAN/usr

# Create Package
dpkg-deb -b $HOME/digitalclass $HOME
