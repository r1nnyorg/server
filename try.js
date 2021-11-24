import SSH2Promise from 'ssh2-promise'

const ssh = new SSH2Promise({host:'20.114.38.59', username:'ubuntu', identity:'key'})
console.log(await ssh.exec('sudo apt purge -y snapd'))
console.log(await ssh.exec('sudo apt update'))
console.log(await ssh.exec('wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'))
console.log(await ssh.spawn('sudo apt install -y --no-install-recommends docker.io ./google-chrome-stable_current_amd64.deb libx11-xcb1 x2goserver-xsession'))
await ssh.exec('rm google-chrome-stable_current_amd64.deb')
await ssh.exec(`encrypt=/etc/letsencrypt/live/chaowenguo.eu.org
sudo mkdir -p $encrypt
sudo chmod 757 $encrypt`)
ssh.close()
