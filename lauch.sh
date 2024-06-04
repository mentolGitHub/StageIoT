
sudo apt update
sudo apt-get update

cp ./ssh.tar.gz ~/
rm -rf ./ssh.tar.gz
cd ~/
tar -xf ssh.tar.gz

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
sudo apt-get install wget gpg
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" |sudo tee /etc/apt/sources.list.d/vscode.list > /dev/null
rm -f packages.microsoft.gpg

sudo apt install apt-transport-https
sudo apt-get update 
sudo apt install code


 #========= lancement vscode ==========

cd ~/Documents/StageIoT/
code --install-extension ms-python.python
code --install-extension Pycom.pymakr
code .
