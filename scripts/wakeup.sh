for MAC in 78:ac:c0:c0:8a:7f 78:ac:c0:c1:11:03 78:ac:c0:c0:88:49 78:ac:c0:c1:0a:83 78:ac:c0:c0:88:fc 78:ac:c0:c0:97:e7 78:ac:c0:c1:0a:85 78:ac:c0:c1:09:a6 78:ac:c0:c0:8a:7b 78:ac:c0:ba:7a:6b 78:ac:c0:c0:8e:ba 78:ac:c0:c0:8d:e0 78:ac:c0:c1:09:9c 78:ac:c0:c1:09:56 78:ac:c0:ba:77:e4 78:ac:c0:c1:08:56 78:ac:c0:c1:09:ae 78:ac:c0:ba:78:0b 78:ac:c0:c1:0a:42 78:ac:c0:c2:8b:b5 78:ac:c0:c0:8a:d0 78:ac:c0:c2:8c:cd 78:ac:c0:c0:88:62 78:ac:c0:c1:09:cb 78:ac:c0:c1:0a:87
do
  wakeonlan $MAC
  sleep 10
done
