import asyncio, asyncssh, pathlib, aiohttp, builtins

async def main():
    certbot = await asyncio.create_subprocess_exec('certbot', 'renew')
    async with aiohttp.ClientSession() as session:
        async with session.get('https://bitbucket.org/chaowenguo/server/raw/main/server.json') as response:
            ips = await response.json(content_type=None)
            async with asyncssh.connect('2a03:7900:6446::' + ips[0], username='ubuntu', client_keys=[builtins.str(pathlib.Path.home()) + '/.ssh/key'], known_hosts=None) as remote0, asyncssh.connect('2a03:7900:6446::' + ips[1], username='ubuntu', client_keys=[builtins.str(pathlib.Path.home()) + '/.ssh/key'], known_hosts=None) as remote1, asyncssh.connect('2a03:7900:6446::' + ips[2], username='ubuntu', client_keys=[builtins.str(pathlib.Path.home()) + '/.ssh/key'], known_hosts=None) as remote2, asyncssh.connect('2a03:7900:6446::' + ips[3], username='ubuntu', client_keys=[builtins.str(pathlib.Path.home()) + '/.ssh/key'], known_hosts=None) as remote3:
                async def renew(remote):
                    await asyncssh.scp('/etc/letsencrypt/live/chaowenguo.eu.org', (remote, '/etc/letsencrypt/live'), recurse=True)
                    await remote.run('''sudo docker stop ingress
sudo docker rm ingress
sudo docker run -d --name ingress --net backend -p 443:443 -v /etc/letsencrypt/live/chaowenguo.eu.org:/encrypt:ro chaowenguo/ingress''')
                await asyncio.gather(*(renew(_) for _ in (remote0, remote1, remote2, remote3)))
    await certbot.wait()

asyncio.run(main())