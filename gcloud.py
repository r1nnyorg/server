import aiohttp, asyncio, google.auth, google.auth.transport.requests, google.oauth2, pathlib

credentials = google.oauth2.service_account.Credentials.from_service_account_file('gcloud', scopes=['https://www.googleapis.com/auth/cloud-platform'])
auth_req = google.auth.transport.requests.Request()
credentials.refresh(auth_req)
project='chaowenguo'
zone='us-central1-a'

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://compute.googleapis.com/compute/v1/projects/{project}/zones/{zone}/instances', headers={'authorization':f'Bearer {credentials.token}'}, json={'name':'google','tags':{'items':['https-server']},'machineType':f'zones/{zone}/machineTypes/f1-micro','networkInterfaces':[{'accessConfigs':[{'type':'ONE_TO_ONE_NAT','name':'External NAT'}],'network':'global/networks/default'}],'disks':[{'boot':True,'initializeParams':{'diskSizeGb':'30','sourceImage':'projects/ubuntu-os-cloud/global/images/family/ubuntu-2004-lts'}}], 'metadata':{'items':[{'key':'ssh-keys','value':'chaowen_guo1:' + pathlib.Path(__file__).resolve().parent.join('google.pub').read_text()}]}}) as _: pass
        async with session.get(f'https://compute.googleapis.com/compute/v1/projects/{project}/zones/{zone}/instances/google', headers={'authorization':f'Bearer {credentials.token}'}) as response: print((await response.json()).get('networkInterfaces')[0].get('accessConfigs')[0].get('natIP'))

asyncio.run(main())
#gcloud auth activate-service-account --key-file=gcloud --project chaowenguo
#gcloud compute instances create google --image-family=ubuntu-2004-lts --image-project=ubuntu-os-cloud --machine-type=f1-micro --zone=us-central1-a --boot-disk-size=30GB --tags https-server --metadata=ssh-keys="chaowen_guo1:`cat google.pub`"
