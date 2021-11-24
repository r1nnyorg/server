import SSH2Promise from 'ssh2-promise'

const ssh = new SSH2Promise({host:'20.114.38.59', username:'ubuntu', identity:'key'})
try
{
console.log(await ssh.exec(`whoami
sudo apt-get update`))
}
catch (e) {console.log(e.toString('utf8'))}
ssh.close()
