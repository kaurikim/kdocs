#!/bin/bash

cp gitconfig ~/.gitconfig
cp kaurirc ~/.kaurirc
cp vimrc ~/.vimrc
cp vim ~/.vim -af

sudo apt-get -y install screen
sudo apt-get -y install cscope
sudo apt-get -y install exuberant-ctags
sudo apt-get -y install tree
sudo apt-get install -y vim

#sudo apt-get install -y python-dev python-virtualenv git
#sudo apt-get install -y python-oslosphinx 
#sudo apt-get install -y python-sphinx

# for linux kernel
sudo apt-get install -y bc flex bison

# for perf 
sudo apt-get install -y libelf-dev  libunwind7-dev libaudit-dev  libslang2-dev libnuma-dev 
sudo apt-get install -y libdw-dev elfutils binutils-dev zlib-bin
