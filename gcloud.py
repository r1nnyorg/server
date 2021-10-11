import aiohttp, asyncio

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://compute.googleapis.com/compute/v1/projects/chaowenguo/zones/us-central1-a/instances/google', headers=headers) as _: pass

asyncio.run(main())
