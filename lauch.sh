 #=========== VSCODE ============
sudo apt update
sudo apt-get update
sudo apt-get install wget gpg
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" |sudo tee /etc/apt/sources.list.d/vscode.list > /dev/null
rm -f packages.microsoft.gpg

sudo apt install apt-transport-https

sudo apt install code

 #=========== NODEJS ==============
curl -sL https://deb.nodesource.com/setup_20.x | sudo -E bash -apt-get update apt-get install nodejs 
sudo apt-get update 
sudo apt-get install nodejs

#============= GIT =====================
# Copier la clef ssh
sudo apt install git
git clone git@github.com:mentolGitHub/StageIoT.git

 #========= lancement vscode ==========

cd ~/Documents/StageIoT/
code --extensions-dir ./.vscode/extensions/