import aiohttp, asyncio, argparse
parser = argparse.ArgumentParser()
parser.add_argument('token')

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://compute.googleapis.com/compute/v1/projects/chaowenguo/zones/us-central1-a/instances/google', headers={'authorization':f'bearer {parser.parse_args().token}'}) as response: print(await response.json())

asyncio.run(main())
