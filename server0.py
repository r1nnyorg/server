import asyncssh, aiohttp, asyncio, base64, argparse, pathlib

parser = argparse.ArgumentParser()
parser.add_argument('github')
parser.add_argument('password')
args = parser.parse_args()
subscription = '326ccd13-f7e0-4fbf-be40-22e42ef93ad5'
key = asyncssh.generate_private_key('ssh-rsa')
key.write_private_key('key')

async def linux(session, token, network):
    async with session.put(f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/westus2/providers/Microsoft.Network/publicIPAddresses/linux?api-version=2021-03-01', headers={'Authorization':f'Bearer {token}'}, json={'location':'westus2'}) as ip:
        if ip.status == 201:    
            while True:
                await asyncio.sleep(int(ip.headers.get('retry-after')))
                async with session.get(ip.headers.get('azure-asyncOperation'), headers={'Authorization':f'Bearer {token}'}) as _:
                    if (await _.json()).get('status') == 'Succeeded': break
        async with session.put(f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/westus2/providers/Microsoft.Network/networkInterfaces/linux?api-version=2021-03-01', headers={'Authorization':f'Bearer {token}'}, json={'location':'westus2', 'properties':{'ipConfigurations':[{'name':'linux', 'properties':{'publicIPAddress':{'id':(await ip.json()).get('id')}, 'subnet':{'id':(await network.json()).get('properties').get('subnets')[0].get('id')}}}]}}) as interface:
            if interface.status == 201:
                while True:
                    await asyncio.sleep(10)
                    async with session.get(interface.headers.get('azure-asyncOperation'), headers={'Authorization':f'Bearer {token}'}) as _:
                        if (await _.json()).get('status') == 'Succeeded': break
            async with session.put(f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/westus2/providers/Microsoft.Compute/virtualMachines/linux?api-version=2021-07-01', headers={'Authorization':f'Bearer {token}'}, json={'location':'westus2', 'properties':{'hardwareProfile':{'vmSize':'Standard_B1s'}, 'osProfile':{'adminUsername':'ubuntu', 'computerName':'linux', 'linuxConfiguration':{'ssh':{'publicKeys':[{'path':'/home/ubuntu/.ssh/authorized_keys', 'keyData':key.export_public_key().decode()}]}, 'disablePasswordAuthentication':True}}, 'storageProfile':{'imageReference':{'sku':'20_04-lts-gen2', 'publisher':'Canonical', 'version':'latest', 'offer':'0001-com-ubuntu-server-focal'}, 'osDisk':{'diskSizeGB':64, 'createOption':'FromImage'}}, 'networkProfile':{'networkInterfaces':[{'id':(await interface.json()).get('id')}]}}}) as machine:
                if machine.status == 201:
                    while True:
                        await asyncio.sleep(int(machine.headers.get('retry-after')))
                        async with session.get(machine.headers.get('azure-asyncOperation'), headers={'Authorization':f'Bearer {token}'}) as _:
                            if (await _.json()).get('status') == 'Succeeded': break
    #async with session.put(f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/westus2/providers/Microsoft.Network/networkSecurityGroups/linux?api-version=2021-03-01', headers={'Authorization':f'Bearer {token}'}, json={'location':'westus2', 'properties':{'securityRules':[{'name':'https', 'properties':{'protocol':'*', 'sourceAddressPrefix':'*', 'destinationAddressPrefix':'*', 'access':'Allow', 'destinationPortRange':'443', 'sourcePortRange':'*', 'priority':130, 'direction':'Inbound'}}]}}) as security:
    #    if security.status == 201:
    #        while True:
    #            await asyncio.sleep(int(security.headers.get('retry-after')))
    #            async with session.get(security.headers.get('azure-asyncOperation'), headers={'Authorization':f'Bearer {token}'}) as _:
    #               if (await _.json()).get('status') == 'Succeeded': break
    async with session.get(f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/westus2/providers/Microsoft.Network/publicIPAddresses/linux?api-version=2021-03-01', headers={'Authorization':f'Bearer {token}'}) as response:
        ip = (await response.json()).get('properties').get('ipAddress')
        await asyncio.sleep(60)
        async with asyncssh.connect(ip, username='ubuntu', client_keys=['key'], known_hosts=None) as ssh: await ssh.run('''sudo apt purge -y snapd
sudo apt update
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y --no-install-recommends docker.io ./google-chrome-stable_current_amd64.deb libx11-xcb1 x2goserver-xsession
rm google-chrome-stable_current_amd64.deb
encrypt=/etc/letsencrypt/live/chaowenguo.eu.org
sudo mkdir -p $encrypt
sudo chmod 757 $encrypt''')
        return ip

async def win(session, token, network):
    async with session.put(f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/westus2/providers/Microsoft.Network/publicIPAddresses/win?api-version=2021-03-01', headers={'Authorization':f'Bearer {token}'}, json={'location':'westus2'}) as ip:
        if ip.status == 201:
            while True:
                await asyncio.sleep(int(ip.headers.get('retry-after')))
                async with session.get(ip.headers.get('azure-asyncOperation'), headers={'Authorization':f'Bearer {token}'}) as _:
                    if (await _.json()).get('status') == 'Succeeded': break
        async with session.put(f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/westus2/providers/Microsoft.Network/networkInterfaces/win?api-version=2021-03-01', headers={'Authorization':f'Bearer {token}'}, json={'location':'westus2', 'properties':{'ipConfigurations':[{'name':'win', 'properties':{'publicIPAddress':{'id':(await ip.json()).get('id')}, 'subnet':{'id':(await network.json()).get('properties').get('subnets')[0].get('id')}}}]}}) as interface:
            if interface.status == 201:
                while True:
                    await asyncio.sleep(10)
                    async with session.get(interface.headers.get('azure-asyncOperation'), headers={'Authorization':f'Bearer {token}'}) as _:
                        if (await _.json()).get('status') == 'Succeeded': break
            async with session.put(f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/westus2/providers/Microsoft.Compute/virtualMachines/win?api-version=2021-07-01', headers={'Authorization':f'Bearer {token}'}, json={'location':'westus2', 'properties':{'hardwareProfile':{'vmSize':'Standard_B1s'}, 'osProfile':{'adminUsername':'ubuntu', 'computerName':'win', 'adminPassword':args.password}, 'storageProfile':{'imageReference':{'sku':'2019-datacenter-core-with-containers-smalldisk-g2', 'publisher':'MicrosoftWindowsServer', 'version':'latest', 'offer':'WindowsServer'}, 'osDisk':{'diskSizeGB':64, 'createOption':'FromImage'}}, 'networkProfile':{'networkInterfaces':[{'id':(await interface.json()).get('id')}]}}}) as machine:
                if machine.status == 201:
                    while True:
                        await asyncio.sleep(int(machine.headers.get('retry-after')))
                        async with session.get(machine.headers.get('azure-asyncOperation'), headers={'Authorization':f'Bearer {token}'}) as _:
                            if (await _.json()).get('status') == 'Succeeded': break
    #async with session.put(f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/win/providers/Microsoft.Network/networkSecurityGroups/win?api-version=2021-03-01', headers={'Authorization':f'Bearer {token}'}, json={'location':'westus2', 'properties':{'securityRules':[{'name':'https', 'properties':{'protocol':'*', 'sourceAddressPrefix':'*', 'destinationAddressPrefix':'*', 'access':'Allow', 'destinationPortRange':'443', 'sourcePortRange':'*', 'priority':130, 'direction':'Inbound'}}]}}) as security:
    #    if security.status == 201:
    #        while True:
    #            await asyncio.sleep(int(security.headers.get('retry-after')))
    #            async with session.get(security.headers.get('azure-asyncOperation'), headers={'Authorization':f'Bearer {token}'}) as _:
    #               if (await _.json()).get('status') == 'Succeeded': break
                    
async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://login.microsoftonline.com/deb7ba76-72fc-4c07-833f-1628b5e92168/oauth2/token', data={'grant_type':'client_credentials', 'client_id':'60f0699c-a6da-4a59-be81-fd413d2c68bc', 'client_secret':'ljEw3qnk.HcDcd85aSBLgjdJ4uA~bqPKYz', 'resource':'https://management.azure.com/'}) as response:
            token = (await response.json()).get('access_token')
            async with session.head(f'https://management.azure.com/subscriptions/{subscription}/resourcegroups/westus2?api-version=2021-04-01', headers={'Authorization':f'Bearer {token}'}) as response:
                if response.status == 204:
                    async with session.delete(f'https://management.azure.com/subscriptions/{subscription}/resourcegroups/westus2?api-version=2021-04-01', headers={'Authorization':f'Bearer {token}'}) as response:
                        if response.status == 202:
                            while True:
                                await asyncio.sleep(int(response.headers.get('retry-after')))
                                async with session.get(response.headers.get('location'), headers={'Authorization':f'Bearer {token}'}) as _:
                                    if _.status == 200: break
            async with session.put(f'https://management.azure.com/subscriptions/{subscription}/resourcegroups/westus2?api-version=2021-04-01', headers={'Authorization':f'Bearer {token}'}, json={'location':'westus2'}) as _: pass
            async with session.put(f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/westus2/providers/Microsoft.Network/virtualNetworks/westus2?api-version=2021-03-01', headers={'Authorization':f'Bearer {token}'}, json={'location':'westus2', 'properties':{'addressSpace':{'addressPrefixes':['10.0.0.0/16']}, 'subnets':[{'name':'westus2', 'properties':{'addressPrefix':'10.0.0.0/24'}}]}}) as network:
                if network.status == 201:
                    while True:
                        await asyncio.sleep(int(network.headers.get('retry-after')))
                        async with session.get(network.headers.get('azure-asyncOperation'), headers={'Authorization':f'Bearer {token}'}) as _:
                            if (await _.json()).get('status') == 'Succeeded': break
                await asyncio.gather(win(session, token, network), linux(session, token, network))
            async with session.put(f'https://api.github.com/repos/chaowenGUO/key/contents/0', headers={'authorization':f'token {args.github}'}, json={'message':'message', 'content':base64.b64encode(pathlib.Path(__file__).resolve().parent.joinpath('key').read_bytes()).decode()}) as _: pass

asyncio.run(main())
