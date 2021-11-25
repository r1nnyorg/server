import fetch from 'node-fetch'

const subscription = '326ccd13-f7e0-4fbf-be40-22e42ef93ad5'
const token = (await fetch('https://login.microsoftonline.com/deb7ba76-72fc-4c07-833f-1628b5e92168/oauth2/token', {method:'post', body:new globalThis.URLSearchParams({grant_type:'client_credentials', client_id:'60f0699c-a6da-4a59-be81-fd413d2c68bc', client_secret:'ljEw3qnk.HcDcd85aSBLgjdJ4uA~bqPKYz', resource:'https://management.azure.com/'})}).then(_ => _.json())).access_token
const group = `https://management.azure.com/subscriptions/${subscription}/resourcegroups/machine?api-version=2021-04-01`
const response = await fetch(`https://management.azure.com/subscriptions/${subscription}/resourceGroups/machine/providers/Microsoft.Compute/virtualMachines/win/runCommand?api-version=2021-07-01`, {method:'post', headers:{authorization:`Bearer ${token}`, 'content-type':'application/json'}, body:globalThis.JSON.stringify({commandId:'RunPowerShellScript', script:['Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0', 'Start-Service sshd', 'Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force', 'Install-Module -Name DockerMsftProvider -Repository PSGallery -Force', 'Install-Package -Name docker -ProviderName DockerMsftProvider -Force', 'Restart-Computer -Force']})})
if (globalThis.Object.is(response.status, 202))
{
    while (true)
    {
        await new globalThis.Promise(_ => globalThis.setTimeout(_, 10 * 1000))
        if (globalThis.Object.is((await fetch(response.headers.get('azure-asyncOperation'), {headers:{authorization:`Bearer ${token}`}}).then(_ => _.json())).status, 'Succeeded')) break
    }
}
console.log(await response.json())
//
