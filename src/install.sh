#!/bin/bash#
# This script check all dependencies to run digitalclass

# Ubuntu Distro =>

# Add Repository FFMPEG
sudo add-apt-repository ppa:mc3man/trusty-media
sudo apt-get update
sudo add-apt-get install ffmpeg

# Add Python Installers => pip
sudo apt-get install python-pip python-dev build-essential
sudo pip install --upgrade pip
sudo pip install --upgrade virtualenv

# Install Python Dependencies
# pygame
sudo apt-get build-dep python-pygame
# pyaudio
sudo apt-get install python-pyaudio
