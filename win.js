import fetch from 'node-fetch'
import process from 'process'

const subscription = '326ccd13-f7e0-4fbf-be40-22e42ef93ad5'

const token = (await fetch('https://login.microsoftonline.com/deb7ba76-72fc-4c07-833f-1628b5e92168/oauth2/token', {method:'post', body:new globalThis.URLSearchParams({grant_type:'client_credentials', client_id:'60f0699c-a6da-4a59-be81-fd413d2c68bc', client_secret:'ljEw3qnk.HcDcd85aSBLgjdJ4uA~bqPKYz', resource:'https://management.azure.com/'})}).then(_ => _.json())).access_token
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