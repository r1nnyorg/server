certbot renew
for i in `python3 -c 'import pathlib, json; print(json.loads(pathlib.Path.home().joinpath("ip").read_text()) + [json.loads(pathlib.Path.home().joinpath("0").read_text())])'`
do
    scp -o StrictHostKeyChecking=no -i ~/key -r /etc/letsencrypt/live/chaowenguo.eu.org ubuntu@[2a03:7900:6446::`echo $i | grep -Eo [0-9.]+`]:/etc/letsencrypt/live
done
sshpass -p $password scp -o StrictHostKeyChecking=no -r /etc/letsencrypt/live/chaowenguo.eu.org root@[2a01:4f8:211:25cf::65e:1]:/etc/letsencrypt/live
curl -H authorization:token\ $github -d {\"event_type\":\"dummy\"\,\"client_payload\":{\"foo\":\"bar\"}} https://api.github.com/repos/chaowenguoorg/server/dispatches

#journalctl -u encrypt.service
