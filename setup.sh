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
code ../Documents/StageIoT


#========== GDOWN =============

pip install gdown
export PATH=$PATH:/home/local/.local/bin
echo "export PATH=$PATH:/home/local/.local/bin" >> ~/.bashrc
#========= GetCubeIde ==========
cd /home/local/Téléchargements/
gdown https://drive.google.com/uc?id=1lUXRF5xAX0Q55UL_0ZMYPDgUpGt2td_x
sudo mkdir /opt/st
tar -xf stm32cubeide_1.15.1.tar.gz
sudo cp -r ./stm32cubeide_1.15.1 /opt/st/
sudo rm -rf ./stm32cubeide_1.15.1
sudo rm -rf ./stm32cubeide_1.15.1.tar.gz
sudo apt-get install libncurses5 -y
#========= GetSTlink ============
doc="st-stlink-server-2.1.1-1-linux-amd64.deb"
cd /home/local/Téléchargements/
gdown https://drive.google.com/uc?id=1W9A_pyXGvcN3RtvXQHMTdM7Nhi7Zc0Ws
sudo dpkg -i st-stlink-server-2.1.1-1-linux-amd64.deb
sudo rm -rf ./$doc

sudo chmod  -R 777 /home/local/STM32CubeIDE/

echo "alias cube-ide=\"/opt/st/stm32cubeide_1.15.1/stm32cubeide &\"" >> ~/.bashrc
/opt/st/stm32cubeide_1.15.1/stm32cubeide &
exec bash
#========= fin ========
