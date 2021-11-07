import oci, asyncssh, aiohttp, asyncio, base64, argparse, pathlib, json

parser = argparse.ArgumentParser()
for _ in ('clientid', 'clientsecret', 'tenantid'): parser.add_argument(_)
parser.add_argument('github')
args = parser.parse_args()
configure = {'user':'ocid1.user.oc1..aaaaaaaalwudh6ys7562qtyfhxl4oji25zn6aapndqfuy2jfroyyielpu3pa', 'key_file':'oci.key', 'fingerprint':'bd:01:98:0d:5d:4a:6f:b2:49:b4:7f:df:43:00:32:39', 'tenancy':'ocid1.tenancy.oc1..aaaaaaaa4h5yoefhbxm4ybqy6gxl6y5cgxmdijira7ywuge3q4cbdaqnyawq', 'region':'us-sanjose-1'}
virtualNetworkClient = oci.core.VirtualNetworkClient(configure)
virtualNetworkClientCompositeOperations = oci.core.VirtualNetworkClientCompositeOperations(virtualNetworkClient)
createVcnDetails = oci.core.models.CreateVcnDetails(compartment_id=configure.get('tenancy'), cidr_block='10.0.0.0/16')
vcn = virtualNetworkClientCompositeOperations.create_vcn_and_wait_for_state(createVcnDetails, wait_for_states=[oci.core.models.Vcn.LIFECYCLE_STATE_AVAILABLE]).data
createSubnetDetails = oci.core.models.CreateSubnetDetails(compartment_id=vcn.compartment_id,vcn_id=vcn.id,cidr_block=vcn.cidr_block)
subnet = virtualNetworkClientCompositeOperations.create_subnet_and_wait_for_state(createSubnetDetails,wait_for_states=[oci.core.models.Subnet.LIFECYCLE_STATE_AVAILABLE]).data
createInternetGatewayDetails = oci.core.models.CreateInternetGatewayDetails(compartment_id=vcn.compartment_id, is_enabled=True, vcn_id=vcn.id)
gateway = virtualNetworkClientCompositeOperations.create_internet_gateway_and_wait_for_state(createInternetGatewayDetails, wait_for_states=[oci.core.models.InternetGateway.LIFECYCLE_STATE_AVAILABLE]).data
route_rules = virtualNetworkClient.get_route_table(vcn.default_route_table_id).data.route_rules
route_rules.append(oci.core.models.RouteRule(cidr_block=None, destination='0.0.0.0/0', destination_type='CIDR_BLOCK', network_entity_id=gateway.id))
updateRouteTableDetails = oci.core.models.UpdateRouteTableDetails(route_rules=route_rules)
virtualNetworkClientCompositeOperations.update_route_table_and_wait_for_state(vcn.default_route_table_id, updateRouteTableDetails, wait_for_states=[oci.core.models.RouteTable.LIFECYCLE_STATE_AVAILABLE])
createNetworkSecurityGroupDetails = oci.core.models.CreateNetworkSecurityGroupDetails(compartment_id=vcn.compartment_id,vcn_id=vcn.id)
#security = virtualNetworkClientCompositeOperations.create_network_security_group_and_wait_for_state(createNetworkSecurityGroupDetails, wait_for_states=[oci.core.models.RouteTable.LIFECYCLE_STATE_AVAILABLE]).data
#addSecurityRuleDetails = oci.core.models.AddSecurityRuleDetails(direction='INGRESS', source='0.0.0.0/0', source_type='CIDR_BLOCK', protocol='6', tcp_options=oci.core.models.TcpOptions(destination_port_range=oci.core.models.PortRange(min=443, max=443)))
#addSecurityRulesDetails = oci.core.models.AddNetworkSecurityGroupSecurityRulesDetails(security_rules=[addSecurityRuleDetails])
#virtualNetworkClient.add_network_security_group_security_rules(security.id, addSecurityRulesDetails)
computeClient = oci.core.ComputeClient(configure)
computeClientCompositeOperations = oci.core.ComputeClientCompositeOperations(computeClient)
key = asyncssh.generate_private_key('ssh-rsa')
key.write_private_key('key')
launchInstanceDetails = oci.core.models.LaunchInstanceDetails(availability_domain=oci.identity.IdentityClient(configure).list_availability_domains(compartment_id=vcn.compartment_id).data[0].name, compartment_id=vcn.compartment_id, shape='VM.Standard.E2.1.Micro', metadata={'ssh_authorized_keys':key.export_public_key().decode()}, image_id=computeClient.list_images(compartment_id=vcn.compartment_id, operating_system='Canonical Ubuntu', operating_system_version='20.04 Minimal').data[0].id, subnet_id=subnet.id)

async def oracle(): 
    instance = computeClientCompositeOperations.launch_instance_and_wait_for_state(launchInstanceDetails, wait_for_states=[oci.core.models.Instance.LIFECYCLE_STATE_RUNNING]).data
    ip = oci.core.VirtualNetworkClient(configure).get_vnic(computeClient.list_vnic_attachments(compartment_id=vcn.compartment_id, instance_id=instance.id).data[0].vnic_id).data.public_ip
    await asyncio.sleep(45)
    async with asyncssh.connect(ip, username='ubuntu', client_keys=['key'], known_hosts=None) as ssh: await ssh.run('''sudo apt purge -y snapd
sudo apt update
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y --no-install-recommends docker.io ./google-chrome-stable_current_amd64.deb libx11-xcb1 x2goserver-xsession
rm google-chrome-stable_current_amd64.deb
encrypt=/etc/letsencrypt/live/chaowenguo.eu.org
sudo mkdir -p $encrypt
sudo chmod 757 $encrypt''')
    return ip

import google.auth, google.auth.transport.requests, google.oauth2, builtins

credentials = google.oauth2.service_account.Credentials.from_service_account_file('gcloud', scopes=['https://www.googleapis.com/auth/cloud-platform'])
auth_req = google.auth.transport.requests.Request()
credentials.refresh(auth_req)
project = 'chaowenguo'
zone = 'us-central1-a'

async def gcloud(session):
    instance = f'https://compute.googleapis.com/compute/v1/projects/{project}/zones/{zone}/instances'
    async with session.get(instance + '/google', headers={'authorization':f'Bearer {credentials.token}'}) as response:
        if response.status == 200:
            async with session.delete(instance + '/google', headers={'authorization':f'Bearer {credentials.token}'}) as _: pass
    firewall = f'https://compute.googleapis.com/compute/v1/projects/{project}/global/firewalls'
    async with session.get(firewall + '/https', headers={'authorization':f'Bearer {credentials.token}'}) as response:
        if response == 200:
            async with session.delete(firewall + '/https', headers={'authorization':f'Bearer {credentials.token}'}) as _: pass
    async with session.post(firewall, headers={'authorization':f'Bearer {credentials.token}'}, json={'name':'https','allowed':[{'IPProtocol':'tcp','ports':['443']}]}) as _: pass
    async with session.post(instance, headers={'authorization':f'Bearer {credentials.token}'}, json={'name':'google','machineType':f'zones/{zone}/machineTypes/f1-micro','networkInterfaces':[{'accessConfigs':[{'type':'ONE_TO_ONE_NAT','name':'External NAT'}],'network':'global/networks/default'}],'disks':[{'boot':True,'initializeParams':{'diskSizeGb':'30','sourceImage':'projects/ubuntu-os-cloud/global/images/family/ubuntu-2004-lts'}}], 'metadata':{'items':[{'key':'ssh-keys','value':'ubuntu: ' + key.export_public_key().decode()}]}}) as _: pass
    await asyncio.sleep(45)
    async with session.get(instance + '/google', headers={'authorization':f'Bearer {credentials.token}'}) as response:
        ip = (await response.json()).get('networkInterfaces')[0].get('accessConfigs')[0].get('natIP')
        async with asyncssh.connect(ip, username='ubuntu', client_keys=['key'], known_hosts=None) as ssh: await ssh.run('''sudo apt update
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y --no-install-recommends docker.io ./google-chrome-stable_current_amd64.deb libx11-xcb1 x2goserver-xsession
rm google-chrome-stable_current_amd64.deb
encrypt=/etc/letsencrypt/live/chaowenguo.eu.org
sudo mkdir -p $encrypt
sudo chmod 757 $encrypt''')
        return ip
#gcloud auth activate-service-account --key-file=gcloud --project chaowenguo
#gcloud compute firewall-rules create FooService --allow=tcp:443
#gcloud compute instances create google --image-family=ubuntu-2004-lts --image-project=ubuntu-os-cloud --machine-type=f1-micro --zone=us-central1-a --boot-disk-size=30GB --tags https-server --metadata=ssh-keys="chaowen_guo1:`cat google.pub`"

subscription = '9046396e-e215-4cc5-9eb7-e25370140233'

async def linux(session, token):
    async with session.head(f'https://management.azure.com/subscriptions/{subscription}/resourcegroups/linux?api-version=2021-04-01', headers={'Authorization':f'Bearer {token}'}) as response:
        if response.status == 204:
            async with session.delete(f'https://management.azure.com/subscriptions/{subscription}/resourcegroups/linux?api-version=2021-04-01', headers={'Authorization':f'Bearer {token}'}) as response:
                if response.status == 202:
                    while True:
                        await asyncio.sleep(int(response.headers.get('retry-after')))
                        async with session.get(response.headers.get('location'), headers={'Authorization':f'Bearer {token}'}) as _:
                            if _.status == 200: break
    async with session.put(f'https://management.azure.com/subscriptions/{subscription}/resourcegroups/linux?api-version=2021-04-01', headers={'Authorization':f'Bearer {token}'}, json={'location':'westus'}) as _: pass
    async with session.put(f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/linux/providers/Microsoft.Network/publicIPAddresses/linux?api-version=2021-03-01', headers={'Authorization':f'Bearer {token}'}, json={'location':'westus'}) as ip, session.put(f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/linux/providers/Microsoft.Network/virtualNetworks/linux?api-version=2021-03-01', headers={'Authorization':f'Bearer {token}'}, json={'location':'westus', 'properties':{'addressSpace':{'addressPrefixes':['10.0.0.0/16']}, 'subnets':[{'name':'linux', 'properties':{'addressPrefix':'10.0.0.0/24'}}]}}) as network:
        if ip.status == 201:
            while True:
                await asyncio.sleep(int(ip.headers.get('retry-after')))
                async with session.get(ip.headers.get('azure-asyncOperation'), headers={'Authorization':f'Bearer {token}'}) as _:
                    if (await _.json()).get('status') == 'Succeeded': break
        if network.status == 201:
            while True:
                await asyncio.sleep(int(network.headers.get('retry-after')))
                async with session.get(network.headers.get('azure-asyncOperation'), headers={'Authorization':f'Bearer {token}'}) as _:
                    if (await _.json()).get('status') == 'Succeeded': break
        async with session.put(f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/linux/providers/Microsoft.Network/networkInterfaces/linux?api-version=2021-03-01', headers={'Authorization':f'Bearer {token}'}, json={'location':'westus', 'properties':{'ipConfigurations':[{'name':'linux', 'properties':{'publicIPAddress':{'id':(await ip.json()).get('id')}, 'subnet':{'id':(await network.json()).get('properties').get('subnets')[0].get('id')}}}]}}) as interface:
            if interface.status == 201:
                while True:
                    await asyncio.sleep(10)
                    async with session.get(interface.headers.get('azure-asyncOperation'), headers={'Authorization':f'Bearer {token}'}) as _:
                        if (await _.json()).get('status') == 'Succeeded': break
            async with session.put(f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/linux/providers/Microsoft.Compute/virtualMachines/linux?api-version=2021-07-01', headers={'Authorization':f'Bearer {token}'}, json={'location':'westus', 'properties':{'hardwareProfile':{'vmSize':'Standard_B1s'}, 'osProfile':{'adminUsername':'ubuntu', 'computerName':'linux', 'linuxConfiguration':{'ssh':{'publicKeys':[{'path':'/home/ubuntu/.ssh/authorized_keys', 'keyData':key.export_public_key().decode()}]}, 'disablePasswordAuthentication':True}}, 'storageProfile':{'imageReference':{'sku':'20_04-lts-gen2', 'publisher':'Canonical', 'version':'latest', 'offer':'0001-com-ubuntu-server-focal'}, 'osDisk':{'diskSizeGB':64, 'createOption':'FromImage'}}, 'networkProfile':{'networkInterfaces':[{'id':(await interface.json()).get('id')}]}}}) as machine:
                if machine.status == 201:
                    while True:
                        await asyncio.sleep(int(machine.headers.get('retry-after')))
                        async with session.get(machine.headers.get('azure-asyncOperation'), headers={'Authorization':f'Bearer {token}'}) as _:
                            if (await _.json()).get('status') == 'Succeeded': break
    async with session.put(f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/linux/providers/Microsoft.Network/networkSecurityGroups/linux?api-version=2021-03-01', headers={'Authorization':f'Bearer {token}'}, json={'location':'westus', 'properties':{'securityRules':[{'name':'https', 'properties':{'protocol':'*', 'sourceAddressPrefix':'*', 'destinationAddressPrefix':'*', 'access':'Allow', 'destinationPortRange':'443', 'sourcePortRange':'*', 'priority':130, 'direction':'Inbound'}}]}}) as security:
        if security.status == 201:
            while True:
                await asyncio.sleep(int(security.headers.get('retry-after')))
                async with session.get(security.headers.get('azure-asyncOperation'), headers={'Authorization':f'Bearer {token}'}) as _:
                   if (await _.json()).get('status') == 'Succeeded': break
    async with session.get(f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/linux/providers/Microsoft.Network/publicIPAddresses/linux?api-version=2021-03-01', headers={'Authorization':f'Bearer {token}'}) as response:
        ip = (await response.json()).get('properties').get('ipAddress')
        async with asyncssh.connect(ip, username='ubuntu', client_keys=['key'], known_hosts=None) as ssh: await ssh.run('''sudo apt purge -y snapd
sudo apt update
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y --no-install-recommends docker.io ./google-chrome-stable_current_amd64.deb libx11-xcb1 x2goserver-xsession
rm google-chrome-stable_current_amd64.deb
encrypt=/etc/letsencrypt/live/chaowenguo.eu.org
sudo mkdir -p $encrypt
sudo chmod 757 $encrypt''')
        return ip
#if `az group exists -n linux`
#then
#    az group delete -n linux -y
#fi
#az group create -n linux -l westus
#az vm image list --offer UbuntuServer --all --output table#https://docs.microsoft.com/en-us/azure/virtual-machines/linux/tutorial-manage-vm#understand-vm-images
#az vm list-sizes --location westus --output table#https://docs.microsoft.com/en-us/azure/virtual-machines/linux/tutorial-manage-vm#find-available-vm-sizes
#az vm create -n linux -g linux --image Canonical:0001-com-ubuntu-server-focal:20_04-lts-gen2:latest --size Standard_B1s --admin-username ubuntu --os-disk-size-gb 64 --ssh-key-values azure.pub
#https://docs.microsoft.com/en-us/azure/virtual-machines/linux/nsg-quickstart#quickly-open-a-port-for-a-vm
#az vm open-port -g linux -n linux --port 443
#az vm show -d -g linux -n linux --query publicIps -o tsv

async def win(session, token):
    async with session.head(f'https://management.azure.com/subscriptions/{subscription}/resourcegroups/win?api-version=2021-04-01', headers={'Authorization':f'Bearer {token}'}) as response:
        if response.status == 204:
            async with session.delete(f'https://management.azure.com/subscriptions/{subscription}/resourcegroups/win?api-version=2021-04-01', headers={'Authorization':f'Bearer {token}'}) as response:
                if response.status == 202:
                    while True:
                        await asyncio.sleep(int(response.headers.get('retry-after')))
                        async with session.get(response.headers.get('location'), headers={'Authorization':f'Bearer {token}'}) as _:
                            if _.status == 200: break
    async with session.put(f'https://management.azure.com/subscriptions/{subscription}/resourcegroups/win?api-version=2021-04-01', headers={'Authorization':f'Bearer {token}'}, json={'location':'westus'}) as _: pass
    async with session.put(f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/win/providers/Microsoft.Network/publicIPAddresses/win?api-version=2021-03-01', headers={'Authorization':f'Bearer {token}'}, json={'location':'westus'}) as ip, session.put(f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/win/providers/Microsoft.Network/virtualNetworks/win?api-version=2021-03-01', headers={'Authorization':f'Bearer {token}'}, json={'location':'westus', 'properties':{'addressSpace':{'addressPrefixes':['10.0.0.0/16']}, 'subnets':[{'name':'win', 'properties':{'addressPrefix':'10.0.0.0/24'}}]}}) as network:
        if ip.status == 201:
            while True:
                await asyncio.sleep(int(ip.headers.get('retry-after')))
                async with session.get(ip.headers.get('azure-asyncOperation'), headers={'Authorization':f'Bearer {token}'}) as _:
                    if (await _.json()).get('status') == 'Succeeded': break
        if network.status == 201:
            while True:
                await asyncio.sleep(int(network.headers.get('retry-after')))
                async with session.get(network.headers.get('azure-asyncOperation'), headers={'Authorization':f'Bearer {token}'}) as _:
                    if (await _.json()).get('status') == 'Succeeded': break
        async with session.put(f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/win/providers/Microsoft.Network/networkInterfaces/win?api-version=2021-03-01', headers={'Authorization':f'Bearer {token}'}, json={'location':'westus', 'properties':{'ipConfigurations':[{'name':'win', 'properties':{'publicIPAddress':{'id':(await ip.json()).get('id')}, 'subnet':{'id':(await network.json()).get('properties').get('subnets')[0].get('id')}}}]}}) as interface:
            if interface.status == 201:
                while True:
                    await asyncio.sleep(10)
                    async with session.get(interface.headers.get('azure-asyncOperation'), headers={'Authorization':f'Bearer {token}'}) as _:
                        if (await _.json()).get('status') == 'Succeeded': break
            async with session.put(f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/win/providers/Microsoft.Compute/virtualMachines/win?api-version=2021-07-01', headers={'Authorization':f'Bearer {token}'}, json={'location':'westus', 'properties':{'hardwareProfile':{'vmSize':'Standard_B1s'}, 'osProfile':{'adminUsername':'ubuntu', 'computerName':'win', 'adminPassword':'HL798820y+HL798820y+','storageProfile':{'imageReference':{'sku':'2019-datacenter-core-with-containers-smalldisk-g2', 'publisher':'MicrosoftWindowsServer', 'version':'latest', 'offer':'WindowsServer'}, 'osDisk':{'diskSizeGB':64, 'createOption':'FromImage'}}, 'networkProfile':{'networkInterfaces':[{'id':(await interface.json()).get('id')}]}}}}) as machine:
                if machine.status == 201:
                    while True:
                        await asyncio.sleep(int(machine.headers.get('retry-after')))
                        async with session.get(machine.headers.get('azure-asyncOperation'), headers={'Authorization':f'Bearer {token}'}) as _:
                            if (await _.json()).get('status') == 'Succeeded': break
    async with session.put(f'https://management.azure.com/subscriptions/{subscription}/resourceGroups/win/providers/Microsoft.Network/networkSecurityGroups/win?api-version=2021-03-01', headers={'Authorization':f'Bearer {token}'}, json={'location':'westus', 'properties':{'securityRules':[{'name':'win', 'properties':{'protocol':'*', 'sourceAddressPrefix':'*', 'destinationAddressPrefix':'*', 'access':'Allow', 'destinationPortRange':'443', 'sourcePortRange':'*', 'priority':130, 'direction':'Inbound'}}]}}) as security:
        if security.status == 201:
            while True:
                await asyncio.sleep(int(security.headers.get('retry-after')))
                async with session.get(security.headers.get('azure-asyncOperation'), headers={'Authorization':f'Bearer {token}'}) as _:
                   if (await _.json()).get('status') == 'Succeeded': break
    
async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://login.microsoftonline.com/{args.tenantid}/oauth2/token', data={'grant_type':'client_credentials', 'client_id':args.clientid, 'client_secret':args.clientsecret, 'resource':'https://management.azure.com/'}) as response:
            token = (await response.json()).get('access_token')
            await win(session, token)
            async with session.put(f'https://api.github.com/repos/chaowenGUO/key/contents/ip', headers={'authorization':f'token {parser.parse_args().github}'}, json={'message':'message', 'content':base64.b64encode(json.dump(await asyncio.gather(oracle(), oracle(), gcloud(session), linux(session, token))).encode()).decode()}) as _: pass
            async with session.put(f'https://api.github.com/repos/chaowenGUO/key/contents/key', headers={'authorization':f'token {parser.parse_args().github}'}, json={'message':'message', 'content':base64.b64encode(pathlib.Path(__file__).resolve().parent.joinpath('key').read_bytes()).decode()}) as _: pass

#asyncio.get_event_loop().run_until_complete(asyncio.gather(main(), main()))
asyncio.run(main())
