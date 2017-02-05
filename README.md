# picam

Surveillance Software for the Raspberry Pi.

## Features

- Motion detection
- Amazon S3 backed
- Service-orientated architecture using Redis as a poor-man's message bus

## Usage
Folow the setup guide below first then navigate to the picam/source folder and `chmod +x start` to make the start script runnable. Edit `settings.json` and tweak as necessary.
From different console windows, or in background tasks, run the following commands

- `./start uploader`
- `./start camera`
- `./start busmonitor` (not necessary, only used during development)

The uploader listens for 'image-saved' messages and punts them to S3.
The camera starts the raspberry pi camera and starts taking photos in-memory. These are analysed and if reasonably different from the last saved to disk and an 'image-saved' message published on the bus.
The busmonitor displays all bus messages in the console to help with development.

## Setup

    git clone git@github.com:rba100/picam.git picam
    cd picam

### Install python dependencies

    sudo pip install -r requirements.txt
    sudo apt-get install python3-picamera
    sudo aptitude install python-imaging-tk
    sudo pip3 install redis

### Configure Amazon credentials

As per http://boto3.readthedocs.io/en/latest/guide/configuration.html

    ~/.aws/credentials
    ~/.aws/config

### Intall Redis

Redis is used just to pass messages between services.
It's rubbish, because messages are lost when consumers are offline. It's no RabbitMQ.

Building and installing it is tiresome, but not very hard at all. The steps below I found here: http://mjavery.blogspot.co.uk/2016/05/setting-up-redis-on-raspberry-pi.html

    wget http://download.redis.io/redis-stable.tar.gz
    tar xvzf redis-stable.tar.gz
    cd redis-stable
    make
    cd src
    sudo cp redis-server /usr/local/bin
    sudo cp redis-cli /usr/local/bin
    sudo mkdir /etc/redis
    sudo mkdir /var/redis
    sudo cp utils/redis_init_script /etc/init.d/redis_6379
    sudo cp redis.conf /etc/redis/6379.conf
    sudo mkdir /var/redis/6379
    
Edit the configuration file

    sudo vim /etc/redis/6379.conf

Changing
    
- `daemonize` to `yes`
- `pidfile` to `/var/run/redis_6379.pid`
- `loglevel` to `notice`
- `dir` to `/var/redis/6379`

Configure autostart

    sudo update-rc.d redis_6379 defaults
    sudo update-rc.d redis_6379 start 20 2 3 4 5 . stop 80 0 1 6 .

## Appendix

- python Redis library: https://github.com/andymccurdy/redis-py
- python picamera library: http://picamera.readthedocs.io/en/release-1.12/
- pyton image library: https://pillow.readthedocs.io/en/4.0.x/
