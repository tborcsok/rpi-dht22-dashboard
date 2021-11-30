
# Hasznos parancsok

Fájlok egyszeri másolása:

    scp -r pi@raspberrypi.local:/home/pi/workspace/dht22/data/test_log\*.csv /home/btamas/workspace/raspberry/data

Fájlok szinkronizálása:

    rsync -avhr -e ssh pi@raspberrypi.local:/home/pi/workspace/dht22/data/test_log\*.csv /home/btamas/workspace/raspberry/data
