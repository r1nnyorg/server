import aiohttp.web, asyncio, ssl

async def main():
    sslcontext = ssl.create_default_context(cafile='/etc/ssl/certs/ca-certificates.crt')
    async with aiohttp.ClientSession() as session:
        async def f(_):
            try:
                async with session.get(f'https://app{_}ap.azurewebsites.net', ssl=sslcontext) as __, session.get(f'https://app{_}bp.azurewebsites.net', ssl=sslcontext) as __: pass
            except: pass
        await asyncio.gather(*(f(_) for _ in range(10)))

asyncio.run(main())
