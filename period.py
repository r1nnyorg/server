import asyncio, asyncssh, pathlib

renew = '''sudo docker stop ingress
sudo docker rm ingress
sudo docker run -d --name ingress --net backend -p 443:443 -v /etc/letsencrypt/live/chaowenguo.eu.org:/encrypt:ro chaowenguo/ingress'''

async def main():
    certbot = await asyncio.create_subprocess_exec('certbot', 'renew')
    async with asyncssh.connect('2a03:7900:6446::34.133.204.86', username='ubuntu', client_keys=[str(pathlib.Path.home()) + '/.ssh/key'], known_hosts=None) as remote0, asyncssh.connect('2a03:7900:6446::155.248.205.63', username='ubuntu', client_keys=[str(pathlib.Path.home()) + '/.ssh/key'], known_hosts=None) as remote1, asyncssh.connect('2a03:7900:6446::155.248.203.218', username='ubuntu', client_keys=[str(pathlib.Path.home()) + '/.ssh/key'], known_hosts=None) as remote2:
        await asyncssh.scp('/etc/letsencrypt/live/chaowenguo.eu.org', (remote0, '/etc/letsencrypt/live'), recurse=True)
        await asyncssh.scp('/etc/letsencrypt/live/chaowenguo.eu.org', (remote1, '/etc/letsencrypt/live'), recurse=True)
        await asyncssh.scp('/etc/letsencrypt/live/chaowenguo.eu.org', (remote2, '/etc/letsencrypt/live'), recurse=True)
        await remote0.run(renew)
        await remote1.run(renew)
        await remote2.run(renew)
    await certbot.wait()

asyncio.run(main())
