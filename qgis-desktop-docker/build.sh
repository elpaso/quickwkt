#Build with localhost address: APT_CATCHER_IP=192.168.99.16

# Start APT Catcher
# docker run -d --name apt-acng -p 3142:3142 acng:latest
# docker logs -f apt-acng

ADDR=`ifconfig wlp2s0 | grep 'indirizzo inet:' | cut -d: -f2 | awk '{ print $1}'`
docker build -t qgis-desktop  --build-arg APT_CATCHER_IP=$ADDR .
#docker build -t docker-qgis-server-boundless  --build-arg "$@" .
