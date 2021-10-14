import aiohttp, asyncio, google.auth, google.auth.transport.requests, google.oauth2, pathlib, argparse, base64, asyncssh

parser = argparse.ArgumentParser()
parser.add_argument('github')
credentials = google.oauth2.service_account.Credentials.from_service_account_file('gcloud', scopes=['https://www.googleapis.com/auth/cloud-platform'])
auth_req = google.auth.transport.requests.Request()
credentials.refresh(auth_req)
project='chaowenguo'
zone='us-central1-a'

async def main():
    async with aiohttp.ClientSession() as session:
        key = asyncssh.generate_private_key('ssh-rsa')
        key.write_private_key('google')
        async with session.post(f'https://compute.googleapis.com/compute/v1/projects/{project}/global/firewalls', headers={'authorization':f'Bearer {credentials.token}'}, json={'name':'https','allowed':[{'IPProtocol':'tcp','ports':['443']}]}) as _: pass
        async with session.post(f'https://compute.googleapis.com/compute/v1/projects/{project}/zones/{zone}/instances', headers={'authorization':f'Bearer {credentials.token}'}, json={'name':'google','machineType':f'zones/{zone}/machineTypes/f1-micro','networkInterfaces':[{'accessConfigs':[{'type':'ONE_TO_ONE_NAT','name':'External NAT'}],'network':'global/networks/default'}],'disks':[{'boot':True,'initializeParams':{'diskSizeGb':'30','sourceImage':'projects/ubuntu-os-cloud/global/images/family/ubuntu-2004-lts'}}], 'metadata':{'items':[{'key':'ssh-keys','value':'ubuntu: ' + key.export_public_key().decode()}]}}) as _: pass
        await asyncio.sleep(45)
        async with session.get(f'https://compute.googleapis.com/compute/v1/projects/{project}/zones/{zone}/instances/google', headers={'authorization':f'Bearer {credentials.token}'}) as response: ip = (await response.json()).get('networkInterfaces')[0].get('accessConfigs')[0].get('natIP')
        async with session.put(f'https://api.github.com/repos/chaowenGUO/key/contents/{ip}.key', headers={'authorization':f'token {parser.parse_args().github}'}, json={'message':'message', 'content':base64.b64encode(pathlib.Path(__file__).resolve().parent.joinpath('google').read_bytes()).decode()}) as _: pass
        async with asyncssh.connect(ip, username='ubuntu', client_keys=['google'], known_hosts=None) as ssh: await ssh.run('''sudo apt update
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y --no-install-recommends docker.io ./google-chrome-stable_current_amd64.deb libx11-xcb1 x2goserver-xsession
rm google-chrome-stable_current_amd64.deb
encrypt=/etc/letsencrypt/live/chaowenguo.eu.org
sudo mkdir -p $encrypt
sudo chmod 757 $encrypt''')

asyncio.run(main())
#gcloud auth activate-service-account --key-file=gcloud --project chaowenguo
#gcloud compute firewall-rules create FooService --allow=tcp:443
#gcloud compute instances create google --image-family=ubuntu-2004-lts --image-project=ubuntu-os-cloud --machine-type=f1-micro --zone=us-central1-a --boot-disk-size=30GB --tags https-server --metadata=ssh-keys="chaowen_guo1:`cat google.pub`"
