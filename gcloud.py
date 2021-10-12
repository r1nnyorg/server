import aiohttp, asyncio, google.auth, google.auth.transport.requests, google.oauth2

credentials = google.oauth2.service_account.Credentials.from_service_account_file('gcloud', scopes=['https://www.googleapis.com/auth/cloud-platform'])
auth_req = google.auth.transport.requests.Request()
credentials.refresh(auth_req)
project=chaowenguo
zone=us-central1-a

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://compute.googleapis.com/compute/v1/projects/{project}/zones/{zone}/instances', headers={'authorization':f'Bearer {credentials.token}'}, json={'name':'google','machineType':f'zones/{zone}/machineTypes/f1-micro','disks':[{'initializeParams':{'diskSizeGb':'30','sourceImage':'projects/debian-cloud/global/images/family/debian-9'}}]}) as _: pass
        async with session.get(f'https://compute.googleapis.com/compute/v1/projects/{project}/zones/{zone}/instances/google', headers={'authorization':f'Bearer {credentials.token}'}) as response: print((await response.json()).get('networkInterfaces')[0].get('accessConfigs')[0].get('natIP'))

asyncio.run(main())
