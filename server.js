 import fetch from 'node-fetch'
import process from 'process'
import SSH2Promise from 'ssh2-promise'
import {promises as fs} from 'fs'
import sshpk from 'sshpk'
import path from 'path'

const subscription = '326ccd13-f7e0-4fbf-be40-22e42ef93ad5'

async function linux(token, subnet)
{
    let ip = await fetch(`https://management.azure.com/subscriptions/${subscription}/resourceGroups/machine/providers/Microsoft.Network/publicIPAddresses/linux?api-version=2021-03-01`, {method:'put', headers:{authorization:`Bearer ${token}`, 'content-type':'application/json'}, body:globalThis.JSON.stringify({location:'westus2', zones:['1']})})
    if (globalThis.Object.is(ip.status, 201))
    {
        const header = ip.headers
        while (true)
        {
            await new globalThis.Promise(_ => globalThis.setTimeout(_, header.get('retry-after') * 1000))
            if (globalThis.Object.is((await fetch(header.get('azure-asyncOperation'), {headers:{authorization:`Bearer ${token}`}}).then(_ => _.json())).status, 'Succeeded')) break
        }
    }
    const networkInterface = await fetch(`https://management.azure.com/subscriptions/${subscription}/resourceGroups/machine/providers/Microsoft.Network/networkInterfaces/linux?api-version=2021-03-01`, {method:'put', headers:{authorization:`Bearer ${token}`, 'content-type':'application/json'}, body:globalThis.JSON.stringify({location:'westus2', properties:{ipConfigurations:[{name:'linux', properties:{publicIPAddress:{id:(await ip.json()).id}, subnet:{id:subnet}}}]}})})
    if (globalThis.Object.is(networkInterface.status, 201))
    {
        while (true)
        {
            await new globalThis.Promise(_ => globalThis.setTimeout(_, networkInterface.headers.get('retry-after') * 1000))
            if (globalThis.Object.is((await fetch(networkInterface.headers.get('azure-asyncOperation'), {headers:{authorization:`Bearer ${token}`}}).then(_ => _.json())).status, 'Succeeded')) break
        }
    }
    const machine = await fetch(`https://management.azure.com/subscriptions/${subscription}/resourceGroups/machine/providers/Microsoft.Compute/virtualMachines/linux?api-version=2021-07-01`, {method:'put', headers:{authorization:`Bearer ${token}`, 'content-type':'application/json'}, body:globalThis.JSON.stringify({location:'westus2', properties:{hardwareProfile:{vmSize:'Standard_B1s'}, osProfile:{adminUsername:'ubuntu', computerName:'linux', linuxConfiguration:{ssh:{publicKeys:[{path:'/home/ubuntu/.ssh/authorized_keys', keyData: 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDnUAIjuu5vXtwsEjyL0PV2SCZso1wYSBM2HlECYZ3nh2u9bLl+iTcPbDjCyZ1Q6/PRz7UGceG504fA7SzaXSMircmfiMeshPw+6Qs9N5l/KvsE7sJ6WHvNCFYPIoExamCx1rAU5YZRKZibfrhPaA8/CagrvzmKU/5EvyGR/VgQPjQVO2CMDKwkv6C6sE6V9oqyHTiwitzFI6bpoPaRE83CDkpAXKSa0F6UljT6CTivVm3Upn84Ooz+ecfbV0mhFefnTu8YbsFr5JHfGa4d8RLn0t1tFWv+35uJ9BobjugbT5kLzdtGtot4mf1udvNqmqblXQg8GxrtmXjApl26LG9f4AF+FYjxXzXtM9/GkdYOmDUCOXLu403NxEcueM4lih1iCowxCvttWx1jaN+XroODfhakLUAtKfhwV0MsWfcwMHUd0oQqCjoBxUK4qsddv2NvKL8jJfULFCjREPeJJQ97a+uZTNpEiYn/BR9DYalvy3g0sZTxWqElYBdBRfs54TE='}]}, disablePasswordAuthentication:true}}, storageProfile:{imageReference:{sku:'22_04-lts-gen2', publisher:'Canonical', version:'latest', offer:'0001-com-ubuntu-server-jammy'}, osDisk:{diskSizeGB:64, createOption:'FromImage'}}, networkProfile:{networkInterfaces:[{id:(await networkInterface.json()).id}]}}, zones:['1']})})
    if (globalThis.Object.is(machine.status, 201))
    {
        while (true)
        {
            await new globalThis.Promise(_ => globalThis.setTimeout(_, machine.headers.get('retry-after') * 1000))
            if (globalThis.Object.is((await fetch(machine.headers.get('azure-asyncOperation'), {headers:{authorization:`Bearer ${token}`}}).then(_ => _.json())).status, 'Succeeded')) break
        }
    }
    const key = sshpk.parsePrivateKey(await fs.readFile(path.join(path.dirname(new globalThis.URL(import.meta.url).pathname), 'key')))
    let command = await fetch(`https://management.azure.com/subscriptions/${subscription}/resourceGroups/machine/providers/Microsoft.Compute/virtualMachines/linux/runCommand?api-version=2021-07-01`, {method:'post', headers:{authorization:`Bearer ${token}`, 'content-type':'application/json'}, body:globalThis.JSON.stringify({commandId:'RunShellScript', script:[`echo ${key.toPublic().toString().split(' ', 2).join(' ')} > /home/ubuntu/.ssh/authorized_keys`]})})
    if (globalThis.Object.is(command.status, 202))
    {
        while (true)
        {
            await new globalThis.Promise(_ => globalThis.setTimeout(_, 10 * 1000))
            if (globalThis.Object.is((await fetch(command.headers.get('azure-asyncOperation'), {headers:{authorization:`Bearer ${token}`}}).then(_ => _.json())).status, 'Succeeded')) break
        }
    }
    const response = await fetch(`https://management.azure.com/subscriptions/${subscription}/resourceGroups/machine/providers/Microsoft.Network/publicIPAddresses/linux?api-version=2021-03-01`, {headers:{authorization:`Bearer ${token}`}})
    ip = (await response.json()).properties.ipAddress
    await new globalThis.Promise(_ => globalThis.setTimeout(_, 90 * 1000))
    const ssh = new SSH2Promise({host:ip, username:'ubuntu', privateKey:await fs.readFile(path.join(path.dirname(new globalThis.URL(import.meta.url).pathname), 'key'))})
    try
    {
        await ssh.exec(`wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt update
sudo apt install -y --no-install-recommends docker.io ./google-chrome-stable_current_amd64.deb libx11-xcb1 x2goserver-xsession
rm google-chrome-stable_current_amd64.deb
encrypt=/etc/letsencrypt/live/chaowenguo.eu.org
sudo mkdir -p $encrypt
sudo chmod 757 $encrypt`)
    }
    catch {}
    await ssh.close()
    return ip
}
                                                                                                                       
async function win(token, subnet)
{
    let ip = await fetch(`https://management.azure.com/subscriptions/${subscription}/resourceGroups/machine/providers/Microsoft.Network/publicIPAddresses/win?api-version=2021-03-01`, {method:'put', headers:{authorization:`Bearer ${token}`, 'content-type':'application/json'}, body:globalThis.JSON.stringify({location:'westus2', zones:['2']})})
    if (globalThis.Object.is(ip.status, 201))
    {
        while (true)
        {
            await new globalThis.Promise(_ => globalThis.setTimeout(_, ip.headers.get('retry-after') * 1000))
            if (globalThis.Object.is((await fetch(ip.headers.get('azure-asyncOperation'), {headers:{authorization:`Bearer ${token}`}}).then(_ => _.json())).status, 'Succeeded')) break
        }
    }
    const networkInterface = await fetch(`https://management.azure.com/subscriptions/${subscription}/resourceGroups/machine/providers/Microsoft.Network/networkInterfaces/win?api-version=2021-03-01`, {method:'put', headers:{authorization:`Bearer ${token}`, 'content-type':'application/json'}, body:globalThis.JSON.stringify({location:'westus2', properties:{ipConfigurations:[{name:'win', properties:{publicIPAddress:{id:(await ip.json()).id}, subnet:{id:subnet}}}]}})})
    if (globalThis.Object.is(networkInterface.status, 201))
    {
        while (true)
        {
            await new globalThis.Promise(_ => globalThis.setTimeout(_, networkInterface.headers.get('retry-after') * 1000))
            if (globalThis.Object.is((await fetch(networkInterface.headers.get('azure-asyncOperation'), {headers:{authorization:`Bearer ${token}`}}).then(_ => _.json())).status, 'Succeeded')) break
        }
    }
    const machine = await fetch(`https://management.azure.com/subscriptions/${subscription}/resourceGroups/machine/providers/Microsoft.Compute/virtualMachines/win?api-version=2021-07-01`, {method:'put', headers:{authorization:`Bearer ${token}`, 'content-type':'application/json'}, body:globalThis.JSON.stringify({location:'westus2', properties:{hardwareProfile:{vmSize:'Standard_B1s'}, osProfile:{adminUsername:'ubuntu', computerName:'win', 'adminPassword':process.argv.at(2)}, storageProfile:{imageReference:{sku:'2022-datacenter-azure-edition-core-smalldisk', publisher:'MicrosoftWindowsServer', version:'latest', offer:'WindowsServer'}, osDisk:{diskSizeGB:64, createOption:'FromImage'}}, networkProfile:{networkInterfaces:[{id:(await networkInterface.json()).id}]}}, zones:['2']})})
    if (globalThis.Object.is(machine.status, 201))
    {
        while (true)
        {
            await new globalThis.Promise(_ => globalThis.setTimeout(_, machine.headers.get('retry-after') * 1000))
            if (globalThis.Object.is((await fetch(machine.headers.get('azure-asyncOperation'), {headers:{authorization:`Bearer ${token}`}}).then(_ => _.json())).status, 'Succeeded')) break
        }
    }
    let command = await fetch(`https://management.azure.com/subscriptions/${subscription}/resourceGroups/machine/providers/Microsoft.Compute/virtualMachines/win/runCommand?api-version=2021-07-01`, {method:'post', headers:{authorization:`Bearer ${token}`, 'content-type':'application/json'}, body:globalThis.JSON.stringify({commandId:'RunPowerShellScript', script:['Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0', 'Start-Service sshd', 'New-ItemProperty -Path HKLM:/SOFTWARE/OpenSSH -Name DefaultShell -Value C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -PropertyType String -Force']})})
    if (globalThis.Object.is(command.status, 202))
    {
        while (true)
        {
            await new globalThis.Promise(_ => globalThis.setTimeout(_, 10 * 1000))
            if (globalThis.Object.is((await fetch(command.headers.get('azure-asyncOperation'), {headers:{authorization:`Bearer ${token}`}}).then(_ => _.json())).status, 'Succeeded')) break
        }
    }
    const response = await fetch(`https://management.azure.com/subscriptions/${subscription}/resourceGroups/machine/providers/Microsoft.Network/publicIPAddresses/win?api-version=2021-03-01`, {headers:{authorization:`Bearer ${token}`}})
    ip = (await response.json()).properties.ipAddress
    await new globalThis.Promise(_ => globalThis.setTimeout(_, 90 * 1000))
    const ssh = new SSH2Promise({host:ip, username:'ubuntu', password:process.argv.at(2)})
    console.log(await ssh.exec(`ls`))
    await ssh.close()
}

const token = (await fetch('https://login.microsoftonline.com/deb7ba76-72fc-4c07-833f-1628b5e92168/oauth2/token', {method:'post', body:new globalThis.URLSearchParams({grant_type:'client_credentials', client_id:'60f0699c-a6da-4a59-be81-fd413d2c68bc', client_secret:'ljEw3qnk.HcDcd85aSBLgjdJ4uA~bqPKYz', resource:'https://management.azure.com/'})}).then(_ => _.json())).access_token
const group = `https://management.azure.com/subscriptions/${subscription}/resourcegroups/machine?api-version=2021-04-01` 
if (globalThis.Object.is((await fetch(group, {method:'head', headers:{authorization:`Bearer ${token}`}})).status, 204))
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
await globalThis.Promise.all([linux(token, subnet), win(token, subnet)])
process.exit(0)
//await fetch('https://api.github.com/repos/chaowenGUO/key/contents/0', {method:'put', headers:{'authorization':`token ${process.argv.at(2)}`}, body:globalThis.JSON.stringify({message:'message', content:globalThis.btoa(globalThis.JSON.stringify(await linux(token, subnet)))})})