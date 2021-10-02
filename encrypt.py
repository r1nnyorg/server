import aiohttp, asyncio, os, json, argparse
parser = argparse.ArgumentParser()
parser.add_argument('hook')

headers = {'X-Auth-Email':'chaowen.guo1@gmail.com', 'X-Auth-Key':'86c2df5f431771095ab002f77c890e6ff3162'} #cloudflare domain name Overview Get your API token API Tokens Global API Key
zone = 'a8bfa778b92fae9ca911e20acf31b85d' #cloudflare domain name Overview API Zone ID
dnsType = 'TXT'
name = '_acme-challenge.chaowenguo.eu.org'

async def pre():
    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://api.cloudflare.com/client/v4/zones/{zone}/dns_records', headers=headers, data=json.dumps({'type':dnsType, 'name':name, 'content':os.getenv('CERTBOT_VALIDATION'), 'ttl':1}).encode()) as _: pass
    await asyncio.sleep(10)

async def post():
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.cloudflare.com/client/v4/zones/{zone}/dns_records?type={dnsType}&name={name}', headers=headers) as response:
            async with session.delete(f'https://api.cloudflare.com/client/v4/zones/{zone}/dns_records/{(await response.json()).get("result")[0].get("id")}', headers=headers) as _: pass

if parser.parse_args().hook == 'pre': asyncio.run(pre())
elif parser.parse_args().hook == 'post': asyncio.run(post())
