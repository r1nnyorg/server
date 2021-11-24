import fetch from 'node-fetch'
import process from 'process'
import SSH2Promise from 'ssh2-promise'

const subscription = '326ccd13-f7e0-4fbf-be40-22e42ef93ad5'

async function linux(token, subnet)
{
    let ip = await fetch(`https://management.azure.com/subscriptions/${subscription}/resourceGroups/machine/providers/Microsoft.Network/publicIPAddresses/linux?api-version=2021-03-01`, {method:'put', headers:{authorization:`Bearer ${token}`, 'content-type':'application/json'}, body:globalThis.JSON.stringify({location:'westus2'})})
    if (globalThis.Object.is(ip.status, 201))
    {
        while (true)
        {
            await new globalThis.Promise(_ => globalThis.setTimeout(_, ip.headers.get('retry-after') * 1000))
            if (globalThis.Object.is((await fetch(network.headers.get('azure-asyncOperation'), {headers:{authorization:`Bearer ${token}`}}).then(_ => _.json())).status, 'Succeeded')) break
        }
    }
    const networkInterface = await fetch(`https://management.azure.com/subscriptions/${subscription}/resourceGroups/machine/providers/Microsoft.Network/networkInterfaces/linux?api-version=2021-03-01`, {method:'put', headers:{authorization:`Bearer ${token}`, 'content-type':'application/json'}, body:globalThis.JSON.stringify({location:'westus2', properties:{ipConfigurations:[{name:'linux', properties:{publicIPAddress:{id:(await ip.json()).id}, subnet:{id:subnet}}}]}})})
    if (globalThis.Object.is(networkInterface.status, 201))
    {
        while (true)
        {
            await new globalThis.Promise(_ => globalThis.setTimeout(_, networkInterface.headers.get('retry-after') * 1000))
            if (globalThis.Object.is((await fetch(network.headers.get('azure-asyncOperation'), {headers:{authorization:`Bearer ${token}`}}).then(_ => _.json())).status, 'Succeeded')) break
        }
    }
    const machine = await fetch(`https://management.azure.com/subscriptions/${subscription}/resourceGroups/machine/providers/Microsoft.Compute/virtualMachines/linux?api-version=2021-07-01`, {method:'put', headers:{authorization:`Bearer ${token}`, 'content-type':'application/json'}, body:globalThis.JSON.stringify({location:'westus2', properties:{hardwareProfile:{vmSize:'Standard_B1s'}, osProfile:{adminUsername:'ubuntu', computerName:'linux', linuxConfiguration:{ssh:{publicKeys:[{path:'/home/ubuntu/.ssh/authorized_keys', keyData:await new SSH2Promise({host:(await fetch('https://raw.githubusercontent.com/chaowenGUO/key/main/ip', {headers:{authorization:`token ${process.argv.at(2)}`}}).then(_ => _.json())).at(0), username:'ubuntu', identity:'key'}).exec('cat /home/ubuntu/.ssh/authorized_keys')}]}, disablePasswordAuthentication:true}}, storageProfile:{imageReference:{sku:'20_04-lts-gen2', publisher:'Canonical', version:'latest', offer:'0001-com-ubuntu-server-focal'}, osDisk:{diskSizeGB:64, createOption:'FromImage'}}, networkProfile:{networkInterfaces:[{id:(await networkInterface.json()).id}]}}})})
    if (globalThis.Object.is(machine.status, 201))
    {
        while (true)
        {
            await new globalThis.Promise(_ => globalThis.setTimeout(_, machine.headers.get('retry-after') * 1000))
            if (globalThis.Object.is((await fetch(network.headers.get('azure-asyncOperation'), {headers:{authorization:`Bearer ${token}`}}).then(_ => _.json())).status, 'Succeeded')) break
        }
    }
    const response = await fetch(`https://management.azure.com/subscriptions/${subscription}/resourceGroups/machine/providers/Microsoft.Network/publicIPAddresses/linux?api-version=2021-03-01`, {headers:{authorization:`Bearer ${token}`}})
    ip = (await response.json()).properties.ipAddress
    await new globalThis.Promise(_ => globalThis.setTimeout(_, 60 * 1000))
    await new SSH2Promise({host:ip, username:'ubuntu', identity:'key'}).exec(`sudo apt purge -y snapd
sudo apt update
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y --no-install-recommends docker.io ./google-chrome-stable_current_amd64.deb libx11-xcb1 x2goserver-xsession
rm google-chrome-stable_current_amd64.deb
encrypt=/etc/letsencrypt/live/chaowenguo.eu.org
sudo mkdir -p $encrypt
sudo chmod 757 $encrypt`)
    return ip
}
                                                                                                                       
async function win(token, subnet)
{
    const ip = await fetch(`https://management.azure.com/subscriptions/${subscription}/resourceGroups/machine/providers/Microsoft.Network/publicIPAddresses/win?api-version=2021-03-01`, {method:'put', headers:{authorization:`Bearer ${token}`, 'content-type':'application/json'}, body:globalThis.JSON.stringify({location:'westus2'})})
    if (globalThis.Object.is(ip.status, 201))
    {
        while (true)
        {
            await new globalThis.Promise(_ => globalThis.setTimeout(_, ip.headers.get('retry-after') * 1000))
            if (globalThis.Object.is((await fetch(network.headers.get('azure-asyncOperation'), {headers:{authorization:`Bearer ${token}`}}).then(_ => _.json())).status, 'Succeeded')) break
        }
    }
    const networkInterface = await fetch(`https://management.azure.com/subscriptions/${subscription}/resourceGroups/machine/providers/Microsoft.Network/networkInterfaces/win?api-version=2021-03-01`, {method:'put', headers:{authorization:`Bearer ${token}`, 'content-type':'application/json'}, body:globalThis.JSON.stringify({location:'westus2', properties:{ipConfigurations:[{name:'win', properties:{publicIPAddress:{id:(await ip.json()).id}, subnet:{id:subnet}}}]}})})
    if (globalThis.Object.is(networkInterface.status, 201))
    {
        while (true)
        {
            await new globalThis.Promise(_ => globalThis.setTimeout(_, networkInterface.headers.get('retry-after') * 1000))
            if (globalThis.Object.is((await fetch(network.headers.get('azure-asyncOperation'), {headers:{authorization:`Bearer ${token}`}}).then(_ => _.json())).status, 'Succeeded')) break
        }
    }
    const machine = await fetch(`https://management.azure.com/subscriptions/${subscription}/resourceGroups/machine/providers/Microsoft.Compute/virtualMachines/win?api-version=2021-07-01`, {method:'put', headers:{authorization:`Bearer ${token}`, 'content-type':'application/json'}, body:globalThis.JSON.stringify({location:'westus2', properties:{hardwareProfile:{vmSize:'Standard_B1s'}, osProfile:{adminUsername:'ubuntu', computerName:'win', 'adminPassword':process.argv.at(3)}, storageProfile:{imageReference:{sku:'2022-datacenter-azure-edition-core-smalldisk', publisher:'MicrosoftWindowsServer', version:'latest', offer:'WindowsServer'}, osDisk:{diskSizeGB:64, createOption:'FromImage'}}, networkProfile:{networkInterfaces:[{id:(await networkInterface.json()).id}]}}})})
    if (globalThis.Object.is(machine.status, 201))
    {
        while (true)
        {
            await new globalThis.Promise(_ => globalThis.setTimeout(_, machine.headers.get('retry-after') * 1000))
            if (globalThis.Object.is((await fetch(network.headers.get('azure-asyncOperation'), {headers:{authorization:`Bearer ${token}`}}).then(_ => _.json())).status, 'Succeeded')) break
        }
    }
    const response = await fetch(`https://management.azure.com/subscriptions/${subscription}/resourceGroups/machine/providers/Microsoft.Compute/virtualMachines/win/runCommand?api-version=2021-07-01`, {method:'put', headers:{authorization:`Bearer ${token}`, 'content-type':'application/json'}, body:globalThis.JSON.stringify({commandId:'RunPowerShellScript', script:['Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0', 'Start-Service sshd', 'Install-Module -Name DockerMsftProvider -Repository PSGallery -Force', 'Install-Package -Name docker -ProviderName DockerMsftProvider -Force', 'Restart-Computer -Force']})})
    if (globalThis.Object.is(response.status, 202))
    {
        while (true)
        {
            await new globalThis.Promise(_ => globalThis.setTimeout(_, 10 * 1000))
            if (globalThis.Object.is((await fetch(network.headers.get('azure-asyncOperation'), {headers:{authorization:`Bearer ${token}`}}).then(_ => _.json())).status, 'Succeeded')) break
        }
    }
    const security = await fetch(`https://management.azure.com/subscriptions/${subscription}/resourceGroups/machine/providers/Microsoft.Network/networkSecurityGroups/win?api-version=2021-03-01`, {method:'put', headers:{authorization:`Bearer ${token}`, 'content-type':'application/json'}, body:globalThis.JSON.stringify({location:'westus2', properties:{securityRules:[{name:'https', properties:{protocol:'*', sourceAddressPrefix:'*', destinationAddressPrefix:'*', access:'Allow', destinationPortRange:'443', sourcePortRange:'*', priority:130, direction:'Inbound'}}, {name:'ssh', properties:{protocol:'*', sourceAddressPrefix:'*', destinationAddressPrefix:'*', access:'Allow', destinationPortRange:'22', sourcePortRange:'*', priority:130, direction:'Inbound'}}]}})})
    if (globalThis.Object.is(security.status, 201))
    {
        while (true)
        {
            await new globalThis.Promise(_ => globalThis.setTimeout(_, security.headers.get('retry-after') * 1000))
            if (globalThis.Object.is((await fetch(network.headers.get('azure-asyncOperation'), {headers:{authorization:`Bearer ${token}`}}).then(_ => _.json())).status, 'Succeeded')) break
        }
    }
}

const token = (await fetch('https://login.microsoftonline.com/deb7ba76-72fc-4c07-833f-1628b5e92168/oauth2/token', {method:'post', body:new globalThis.URLSearchParams({grant_type:'client_credentials', client_id:'60f0699c-a6da-4a59-be81-fd413d2c68bc', client_secret:'ljEw3qnk.HcDcd85aSBLgjdJ4uA~bqPKYz', resource:'https://management.azure.com/'})}).then(_ => _.json())).access_token
const group = `https://management.azure.com/subscriptions/${subscription}/resourcegroups/machine?api-version=2021-04-01`
const response = await fetch(group, {method:'head', headers:{authorization:`Bearer ${token}`}})
if (globalThis.Object.is(response.status, 204))
{
    const response = await fetch(group, {method:'delete',  headers:{authorization:`Bearer ${token}`}})
    if (globalThis.Object.is(response.status, 202))
    {
        while (true)
        {
            await new globalThis.Promise(_ => globalThis.setTimeout(_, response.headers.get('retry-after') * 1000))
            if (globalThis.Object.is(await fetch(response.headers.get('location'), {headers:{authorization:`Bearer ${token}`}}).then(_ => _.status), 200)) break
        }
    }
}
await fetch(group, {method:'put', headers:{authorization:`Bearer ${token}`, 'content-type':'application/json'}, body:globalThis.JSON.stringify({location:'westus2'})})
const network = await fetch(`https://management.azure.com/subscriptions/${subscription}/resourceGroups/machine/providers/Microsoft.Network/virtualNetworks/machine?api-version=2021-03-01`, {method:'put', headers:{authorization:`Bearer ${token}`, 'content-type':'application/json'}, body:globalThis.JSON.stringify({location:'westus2', properties:{addressSpace:{addressPrefixes:['10.0.0.0/16']}, subnets:[{name:'machine', properties:{addressPrefix:'10.0.0.0/24'}}]}})})
if (globalThis.Object.is(network.status, 201))
{
    while (true)
    {
        await new globalThis.Promise(_ => globalThis.setTimeout(_, network.headers.get('retry-after') * 1000))
        if (globalThis.Object.is((await fetch(network.headers.get('azure-asyncOperation'), {headers:{authorization:`Bearer ${token}`}}).then(_ => _.json())).status, 'Succeeded')) break
    }
}
const subnet = (await network.json()).properties.subnets[0].id
await win(token, subnet)
await fetch('https://api.github.com/repos/chaowenGUO/key/contents/0', {method:'put', headers:{'authorization':`token ${process.argv.at(2)}`}, body:globalThis.JSON.stringify({message:'message', content:globalThis.btoa(await linux(token, subnet))})})
