certbot renew
for i in `python3 -c 'import pathlib, json; print(json.loads(pathlib.Path.home().joinpath("ip").read_text()) + [json.loads(pathlib.Path.home().joinpath("0").read_text())])'`
do
    scp -o StrictHostKeyChecking=no -i ~/key -r /etc/letsencrypt/live/chaowenguo.eu.org ubuntu@[2a03:7900:6446::`echo $i | grep -Eo [0-9.]+`]:/etc/letsencrypt/live
done
sshpass -p HL798820y+ scp -o StrictHostKeyChecking=no -r /etc/letsencrypt/live/chaowenguo.eu.org root@[2a01:4f8:211:25cf::2196:1]:/etc/letsencrypt/livei
curl -H authorization:token\ $github -d {\"event_type\":\"dummy\"} https://api.github.com/repos/chaowenguoorg/koa/dispatches
curl -H authorization:token\ $github -d {\"event_type\":\"dummy\"} https://api.github.com/repos/chaowenguoorg/aiohttp/dispatches
curl -H authorization:token\ $github -d {\"event_type\":\"dummy\"} https://api.github.com/repos/chaowenguoorg/vertx/dispatches
sleep 1m
redis-cli --cluster create 40.118.245.62:6379 20.112.94.147:6379 155.248.198.227:6379 --cluster-yes
