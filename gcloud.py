import aiohttp, asyncio, google.auth
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('gcloud', scopes=['https://www.googleapis.com/auth/cloud-platform'])
auth_req = google.auth.transport.requests.Request()
credentials.refresh(auth_req)

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://compute.googleapis.com/compute/v1/projects/chaowenguo/zones/us-central1-a/instances/google', headers={'authorization':f'Bearer {credentials.token}'}) as response: print(await response.json())

asyncio.run(main())
