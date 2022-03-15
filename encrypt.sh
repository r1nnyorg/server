certbot renew
for i in `python3 -c 'import pathlib, json; print(json.loads(pathlib.Path.home().joinpath("ip").read_text()) + [json.loads(pathlib.Path.home().joinpath("0").read_text())])'`
do
    scp -o StrictHostKeyChecking=no -i ~/key -r /etc/letsencrypt/live/chaowenguo.eu.org ubuntu@[2a03:7900:6446::`echo $i | grep -Eo [0-9.]+`]:/etc/letsencrypt/live
done
sshpass -p $password scp -o StrictHostKeyChecking=no -r /etc/letsencrypt/live/chaowenguo.eu.org root@[2a01:4f8:211:25cf::65e:1]:/etc/letsencrypt/live
for i in 40.118.245.62 20.112.94.147 155.248.198.227
do
    ssh -o StrictHostKeyChecking=no -i ~/key ubuntu@[2a03:7900:6446::$i] 'sudo docker stop ingress;
    sudo docker rm ingress;
    sudo docker run -d --name ingress --net backend -p 443:443 -v /etc/letsencrypt/live/chaowenguo.eu.org:/encrypt:ro chaowenguo/ingress'
done

#curl -H authorization:token\ $github -d {\"event_type\":\"dummy\"\,\"client_payload\":{\"foo\":\"bar\"}} https://api.github.com/repos/chaowenguoorg/server/dispatches
#redis-cli --cluster create 40.118.245.62:6379 20.112.94.147:6379 155.248.198.227:6379 --cluster-yes
#journalctl -u encrypt.service
