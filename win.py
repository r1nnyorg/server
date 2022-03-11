import aiohttp, asyncio, argparse

parser = argparse.ArgumentParser()
for _ in ('clientid', 'clientsecret', 'tenantid'): parser.add_argument(_)
parser.add_argument('password')
args = parser.parse_args()

subscription = '9046396e-e215-4cc5-9eb7-e25370140233'

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://login.microsoftonline.com/{args.tenantid}/oauth2/token', data={'grant_type':'client_credentials', 'client_id':args.clientid, 'client_secret':args.clientsecret, 'resource':'https://management.azure.com/'}) as response:
            token = (await response.json()).get('access_token')
        #async with session.put(f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/machine/providers/Microsoft.Compute/virtualMachines/win?api-version=2021-07-01', headers={'authorization':f'Bearer {token}'}, json={'location':'westus', 'properties':{'hardwareProfile':{'vmSize':'Standard_B1s'}, 'osProfile':{'adminUsername':'ubuntu', 'computerName':'win', 'adminPassword':args.password}, 'storageProfile':{'imageReference':{'sku':'2022-datacenter-azure-edition-core-smalldisk', 'publisher':'MicrosoftWindowsServer', 'version':'latest', 'offer':'WindowsServer'}, 'osDisk':{'diskSizeGB':64, 'createOption':'FromImage'}}, 'networkProfile':{'networkInterfaces':[{'id':'/subscriptions/9046396e-e215-4cc5-9eb7-e25370140233/resourceGroups/machine/providers/Microsoft.Network/networkInterfaces/win'}]}, 'availabilitySet':{'id':'/subscriptions/9046396e-e215-4cc5-9eb7-e25370140233/resourceGroups/machine/providers/Microsoft.Compute/availabilitySets/MACHINE'}}}) as machine:
        async with session.put(f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/machine/providers/Microsoft.Compute/virtualMachines/win?api-version=2021-07-01', headers={'authorization':f'Bearer {token}'}, json={'location':'westus', 'properties':{'hardwareProfile':{'vmSize':'Standard_B1s'}, 'osProfile':{'adminUsername':'ubuntu', 'computerName':'win', 'adminPassword':args.password}, 'storageProfile':{'imageReference':{'sku':'win11-21h2-entn', 'publisher':'MicrosoftWindowsDesktop', 'version':'latest', 'offer':'windows-11'}, 'osDisk':{'diskSizeGB':64, 'createOption':'FromImage'}}, 'networkProfile':{'networkInterfaces':[{'id':'/subscriptions/9046396e-e215-4cc5-9eb7-e25370140233/resourceGroups/machine/providers/Microsoft.Network/networkInterfaces/win'}]}, 'availabilitySet':{'id':'/subscriptions/9046396e-e215-4cc5-9eb7-e25370140233/resourceGroups/machine/providers/Microsoft.Compute/availabilitySets/MACHINE'}}}) as machine:
            print(machine.status, await machine.json(), flush=True)
            if machine.status == 201:
                while True:
                    await asyncio.sleep(int(machine.headers.get('retry-after')))
                    async with session.get(machine.headers.get('azure-asyncOperation'), headers={'authorization':f'Bearer {token}'}) as _:
                        if (await _.json()).get('status') == 'Succeeded': break                       
        async with session.post(f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/machine/providers/Microsoft.Compute/virtualMachines/win/runCommand?api-version=2021-07-01', headers={'authorization':f'Bearer {token}'}, json={'commandId':'RunPowerShellScript', 'script':['Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0', 'Start-Service sshd', 'New-ItemProperty -Path HKLM:/SOFTWARE/OpenSSH -Name DefaultShell -Value C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -PropertyType String -Force']}) as response:
            if response.status == 202:
                while True:
                    await asyncio.sleep(10)
                    async with session.get(response.headers.get('azure-asyncOperation'), headers={'authorization':f'Bearer {token}'}) as _:
                        if (await _.json()).get('status') == 'Succeeded': break
                            
asyncio.run(main())
# delete vm and os disk
