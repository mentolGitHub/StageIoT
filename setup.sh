branch="TP1"

#=========== NODEJS ==============
sudo apt install python3-pip -y
curl -sL https://deb.nodesource.com/setup_20.x | sudo -E bash -apt-get update apt-get install nodejs 
sudo apt-get update 
sudo apt-get install nodejs -y


#============= GIT =====================

wget "https://github.com/mentolGitHub/StageIoT/archive/"$branch".zip"
unzip $branch.zip
chmod -R 777 ./StageIoT-$branch
mv ./StageIoT-$branch ../Documents/StageIoT
rm -rf $branch.zip

 #=========== VSCODE ============
sudo apt-get install wget gpg -y
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" |sudo tee /etc/apt/sources.list.d/vscode.list > /dev/null
rm -f packages.microsoft.gpg

sudo apt-get install apt-transport-https -y
sudo apt-get update 
sudo apt-get install code -y
code --install-extension ms-python.python
code --install-extension Pycom.pymakr
code --install-extension MS-CEINTL.vscode-language-pack-fr


#========= lancement vscode ==========
code ./StageIoT-$branch


#========== GDOWN =============

pip install gdown
export PATH=$PATH:/home/local/.local/bin
echo "export PATH=$PATH:/home/local/.local/bin" >> ~/.bashrc
#========= GetCubeIde ==========
cd /home/local/Téléchargements/
gdown 1LEMij8jHZLg1Eh1vQRqx_DuPxiijYGcH
gnome-terminal -e ./st-stm32cubeide_1.16.1_22882_20240916_0822_amd64.sh -y
sudo apt-get install libncurses5 -y

#========code==============
gdown 1nrEDy77m0Y5xivelB5xfzQWvoKEGfc8d
unzip en.i-cubeide_lrwan.zip

#========= fin ========
