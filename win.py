async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://login.microsoftonline.com/{args.tenantid}/oauth2/token', data={'grant_type':'client_credentials', 'client_id':args.clientid, 'client_secret':args.clientsecret, 'resource':'https://management.azure.com/'}) as response:
            token = (await response.json()).get('access_token')
