sudo apt-get reinstall usbutils
#============ Python3 =============
sudo apt-get install python3-venv -y


#============ init ==============
sudo apt update
sudo apt-get update
apt --fix-broken install
cp ./ssh.tar.gz ~/
rm -rf ./ssh.tar.gz
cd ~/
tar -xf ssh.tar.gz


cd /etc/dev/rules.d/
sudo wget https://raw.githubusercontent.com/raspberrypi/openocd/rp2040/contrib/60-openocd.rules


 #=========== NODEJS ==============
curl -sL https://deb.nodesource.com/setup_20.x | sudo -E bash -apt-get update apt-get install nodejs 
sudo apt-get update 
sudo apt-get install nodejs -y

#============= GIT =====================
# Copier la clef ssh
sudo apt install git
cd ~/Documents/
git clone git@github.com:mentolGitHub/StageIoT.git
chmod -R 777 ./StageIoT


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
code --install-extension platformio.platformio-ide
code --install-extension ms-vscode.cpptools-extension-pack
code --install-extension MS-CEINTL.vscode-language-pack-fr

 #========= lancement vscode ==========

cd ~/Documents/StageIoT/

code .
