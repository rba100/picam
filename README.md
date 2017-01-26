# picam

## Install python dependencies

`sudo pip install -r requirements.txt`
`sudo apt-get install python3-picamera`
`sudo pip3 install redis` 

## Configure credentials

As per http://boto3.readthedocs.io/en/latest/guide/configuration.html

    ~/.aws/credentials
    ~/.aws/config

## Redis

https://github.com/andymccurdy/redis-py

http://mjavery.blogspot.co.uk/2016/05/setting-up-redis-on-raspberry-pi.html

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
    sudo vim /etc/redis/6379.conf

- daemonize to yes
- pidfile to /var/run/redis_6379.pid
- loglevel to notice
- dir to /var/redis/6379

    sudo update-rc.d redis_6379 defaults
    sudo update-rc.d redis_6379 start 20 2 3 4 5 . stop 80 0 1 6 .

