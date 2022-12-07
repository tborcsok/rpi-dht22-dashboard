# Home temperature and humidity monitor

## Data collection

I scheduled the script that reads sensor values every minute on my Raspberry Pi using crontab. The data collection is scheduled to run every minute.

The data collection script is in [this](https://github.com/tborcsok/rpi-dht22-monitor) repo.

## Syncing files from the Raspberry Pi

I found that `rsync` is a great tool to sync the data on the Pi with my laptop. I run the command like this:

    rsync -avhr -e ssh pi@raspberrypi.local:/<path to DHT22 repo on the Pi>/test_log\*.csv <path to this repo on my laptop>/data

## Convenience script to start the dashboard

I run this shell script to start the dashboard on my laptop:

```bash
#!/bin/bash

rsync -avhr -e ssh pi@raspberrypi.local:/<path to DHT22 repo on the Pi>/test_log\*.csv <path to this repo on my laptop>/data

cd <path to this repo on my laptop>

google-chrome --new-window http://127.0.0.1:8000/ &

poetry run gunicorn app:server
```

![sample image](./docs/assets/dashboard.png)
