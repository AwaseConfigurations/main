# Add system to server preseed

i=1
for mac in 78:ac:c0:c0:8a:7f;
do
sudo cobbler system add --name=host$i --profile=ubuntu-server-i386 --mac=$mac --hostname=host$((i++))
done
