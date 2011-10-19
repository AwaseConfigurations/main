#5005
i=0
for mac in aa:aa:aa:c0:8a:7f aa:aa:aa:c1:11:03 aa:aa:aa:c0:88:49 aa:aa:aa:c1:0a:83 aa:aa:aa:c0:88:fc aa:aa:aa:c0:97:e7 aa:aa:aa:c1:0a:85 aa:aa:aa:c1:09:a6 aa:aa:aa:c0:8a:7b aa:aa:aa:ba:7a:6b aa:aa:aa:c0:8e:ba aa:aa:aa:c0:8d:e0 aa:aa:aa:c1:09:9c aa:aa:aa:c1:09:56 aa:aa:aa:ba:77:e4 aa:aa:aa:c1:08:56 aa:aa:aa:c1:09:ae aa:aa:aa:ba:78:0b aa:aa:aa:c1:0a:42 aa:aa:aa:c2:8b:b5 aa:aa:aa:c0:8a:d0 aa:aa:aa:c2:8c:cd aa:aa:aa:c0:88:62 aa:aa:aa:c1:09:cb aa:aa:aa:c1:0a:87;
do
  sudo cobbler system add --name=$mac --profile=ubuntu-alternate-i386 --mac=$mac --hostname=host$((i++))
done
