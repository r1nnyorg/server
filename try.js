import SSH2Promise from 'ssh2-promise'

const ssh = new SSH2Promise({host:'20.114.38.59', username:'ubuntu', identity:'key'})
console.log(await ssh.exec(`sudo apt-get purge -y snapd
sudo apt-get update`))
ssh.close()
