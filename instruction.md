# Python app in docker container
```
$ cd simple-flask
$ sudo docker build -t johnderasia/simple-flask:v1.0 .
$ sudo docker run --rm -it -p 5001:5000 johnderasia/simple-flask:v1.0
```
![](./images/1.png)

# Shipping image to Docker Hub
```
$ sudo docker login --username=johnderasia
$ sudo docker push johnderasia/simple-flask:v1.0
```
![](./images/2.png)

# Running app on AWS
```
$ sudo docker-machine create --driver amazonec2 --amazonec2-open-port 5000 --amazonec2-region eu-west3 aws-machine
$ sudo docker-machine env aws-machine
$ bash
$ eval $(docker-machine env aws-machine)
$ docker-machine ip aws-machine
$ docker run --rm -it -p 5001:5000 johnderasia/simple-flask:v1.0
```
![](./images/3.png)
## delete the ec2
```
$ sudo docker-machine rm aws-machine
```

# Docker on Linux - Security Warning
- docker only runs with root privilege
> user in the docker group can add themselves to sudoers and also modify host
```
$ docker run -it --rm -v /:/host centos chroot /host
```

# Lauch python interpreter from docker
## pull python image
```
$ sudo docker image pull python
```
## create container
```
$ sudo docker container create --tty --interactive python
```
## list the created container
```
$ sudo docker container ps --all
CONTAINER ID        IMAGE                 COMMAND                  CREATED              STATUS                     PORTS               NAMES
6e760fc8e2a8        python                "python3"                About a minute ago   Created                                        practical_villani
```
## rename the container
```
$ sudo docker container rename practical_villani mypython

$ sudo docker container ps --all
CONTAINER ID        IMAGE                 COMMAND                  CREATED             STATUS                     PORTS               NAMES
6e760fc8e2a8        python                "python3"                3 minutes ago       Created                                        mypython
```
## use the container
```
$ sudo docker container start --interactive mypython
Python 3.8.3 (default, May 16 2020, 07:08:28) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```
## get hostname and exit with 99 code
```
$ sudo docker container start --interactive mypython
Python 3.8.3 (default, May 16 2020, 07:08:28) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import socket
>>> print(socket.gethostname())
6e760fc8e2a8
>>> 
>>> exit(99)

$ sudo docker container ps --all
CONTAINER ID        IMAGE                 COMMAND                  CREATED             STATUS                      PORTS               NAMES
6e760fc8e2a8        python                "python3"                7 minutes ago       Exited (99) 4 seconds ago                       mypython
```
## delete the container
```
$ sudo docker container rm mypython

$ sudo docker container ps --all
CONTAINER ID        IMAGE                 COMMAND                  CREATED             STATUS                     PORTS               NAMES
```
## delete the python image
```
$ sudo docker rmi python
```

# Command Abbreviations
![](./images/4.png)

## run container and download image if not in local storage
```
$ sudo docker run -it --name mypython python
```

# Intergrating Containers with Host System
![](./images/5.png)
```
$ git clone https://github.com/pythonincontainers/myfirst.git
$ cd myfirst
$ cat myfirst.py
print('Python in Containers! Version 1')
```
![](./images/6.png)
![](./images/7.png)
## modify myfirst.py
```
$ vim myfirst.py
$ cat myfirst.py
print('Python in Containers! Version 2000')
```
## Mount directory that has source code into container
```
$ sudo docker run -it --name mypython -v ${PWD}:/app python
Python 3.8.3 (default, May 16 2020, 07:08:28) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> exec(open('/app/myfirst.py').read())
Python in Containers! Version 2000
>>>
```
## Run Command Argument
![](./images/8.png)
## modify myfirst.py again
```
$ vim myfirst.py
$ cat myfirst.py
print('Python in Containers! Version 2000.0')
```
## run docker container with argument
```
$ sudo docker run -it --name myfirst -v ${PWD}:/app python /app/myfirst.py
Python in Containers! Version 2000,0
```
## we can use start to see the output each time we modify myfirst.py
```
$ sudo docker start -i myfirst
Python in Containers! Version 3
```
## start second container
```
$ sudo docker run -it --name mysecond -v ${PWD}:/app python /app/mysecond.py
Python in Containers!
What is your name? kris
Greetings kris
```
## more interactive when started with plain shell promt
```
$ sudo docker run -it --name mypython -v ${PWD}:/app python /bin/bash
root@ffa2999f1926:/# cd /app
root@ffa2999f1926:/app# python mysecond.py 
Python in Containers!
What is your name? kris
Greetings kris
root@ffa2999f1926:/app#
```
# Bind port
![](./images/9.png)
## execute flask in container
```
$ sudo docker run -it --name mypython -v ${PWD}:/app -p 5001:5000 python /bin/bash
root@2922078afc21:/# cd /app
root@2922078afc21:/app# pip install flask
Collecting flask
  Downloading Flask-1.1.2-py2.py3-none-any.whl (94 kB)
     |████████████████████████████████| 94 kB 369 kB/s 
Collecting itsdangerous>=0.24
  Downloading itsdangerous-1.1.0-py2.py3-none-any.whl (16 kB)
Collecting Werkzeug>=0.15
  Downloading Werkzeug-1.0.1-py2.py3-none-any.whl (298 kB)
     |████████████████████████████████| 298 kB 3.4 MB/s 
Collecting click>=5.1
  Downloading click-7.1.2-py2.py3-none-any.whl (82 kB)
     |████████████████████████████████| 82 kB 189 kB/s 
Collecting Jinja2>=2.10.1
  Downloading Jinja2-2.11.2-py2.py3-none-any.whl (125 kB)
     |████████████████████████████████| 125 kB 3.3 MB/s 
Collecting MarkupSafe>=0.23
  Downloading MarkupSafe-1.1.1-cp38-cp38-manylinux1_x86_64.whl (32 kB)
Installing collected packages: itsdangerous, Werkzeug, click, MarkupSafe, Jinja2, flask
Successfully installed Jinja2-2.11.2 MarkupSafe-1.1.1 Werkzeug-1.0.1 click-7.1.2 flask-1.1.2 itsdangerous-1.1.0
root@2922078afc21:/app# 
root@2922078afc21:/app# export FLASK_DEBUG=1
root@2922078afc21:/app# export FLASK_APP=mythird.py
root@2922078afc21:/app# flask run --host=0.0.0.0
 * Serving Flask app "mythird.py" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 105-860-997
```
## access 127.0.0.1:5001 from host browser
![](./images/10.png)
# Summary Intergrating Containers with Host System
![](./images/11.png)


# Container Images
## Image Start-up Command
![](./images/12.png)
![](./images/13.png)

```
$ sudo docker run pythonincontainers/entrypoint
one two three

$ sudo docker run pythonincontainers/entrypoint four five six
one four five six
```
![](./images/14.png)

```
$ sudo docker inspect --format "ENTRYPOINT={{.Config.Entrypoint}} CMD={{.Config.Cmd}}" pythonincontainers/entrypoint
ENTRYPOINT=[echo one] CMD=[two three]

$ sudo docker inspect --format "ENTRYPOINT={{.Config.Entrypoint}} CMD={{.Config.Cmd}}" python
ENTRYPOINT=[] CMD=[python3]

$ sudo docker inspect --format "ENTRYPOINT={{.Config.Entrypoint}} CMD={{.Config.Cmd}}" centos
ENTRYPOINT=[] CMD=[/bin/bash]

$ sudo docker pull nginx
$ sudo docker inspect --format "ENTRYPOINT={{.Config.Entrypoint}} CMD={{.Config.Cmd}}" nginx
ENTRYPOINT=[/docker-entrypoint.sh] CMD=[nginx -g daemon off;]

$ sudo docker pull postgres
$ sudo docker inspect --format "ENTRYPOINT={{.Config.Entrypoint}} CMD={{.Config.Cmd}}" postgres
ENTRYPOINT=[docker-entrypoint.sh] CMD=[postgres]
```

## overwrite entry point
```
$ sudo docker run --rm --entrypoint date centos
Wed Jun 10 16:43:52 UTC 2020
```

# Managing Containers

## interactive and non interactive
![](./images/15.png)
```
$ sudo docker run -d -p 5000:5000 --name simple-flask pythonincontainers/simple-flask
```

## interact with detached container
```
$ sudo docker logs simple-flask
 * Serving Flask app "hello" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```
## tail the logs
```
$ sudo docker logs -t -f simple-flask
2020-06-11T02:19:53.637968644Z  * Serving Flask app "hello" (lazy loading)
2020-06-11T02:19:53.638053236Z  * Environment: production
2020-06-11T02:19:53.638064418Z    WARNING: Do not use the development server in a production environment.
2020-06-11T02:19:53.638091376Z    Use a production WSGI server instead.
2020-06-11T02:19:53.638100957Z  * Debug mode: off
2020-06-11T02:19:53.781179927Z  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
2020-06-11T02:22:08.065403094Z 172.17.0.1 - - [11/Jun/2020 02:22:08] "GET / HTTP/1.1" 200 -
```
## run adhoc commands on running container
```
$ sudo docker ps -a
CONTAINER ID        IMAGE                             COMMAND                  CREATED             STATUS              PORTS                    NAMES
56a49f92bd7e        pythonincontainers/simple-flask   "/bin/sh -c 'python …"   4 minutes ago       Up 4 minutes        0.0.0.0:5000->5000/tcp   simple-flask

$ sudo docker exec simple-flask ps -ef
UID        PID  PPID  C STIME TTY          TIME CMD
root         1     0  0 02:19 ?        00:00:00 /bin/sh -c python hello.py
root         6     1  0 02:19 ?        00:00:00 python hello.py
root         8     0  2 02:24 ?        00:00:00 ps -ef

$ sudo docker exec -it simple-flask bash
root@56a49f92bd7e:/usr/src/app# 
```

## Limit Container Resources
![](./images/16.png)
### Limit memory
```
$ sudo docker run -it -m 100m --memory-swap 100m python bash
root@1981990bd882:/# pip install numpy
Collecting numpy
  Downloading numpy-1.18.5-cp38-cp38-manylinux1_x86_64.whl (20.6 MB)
     |████████████████████████████████| 20.6 MB 45 kB/s 
Installing collected packages: numpy
Successfully installed numpy-1.18.5
root@1981990bd882:/# python
Python 3.8.3 (default, Jun  9 2020, 17:39:39) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import numpy
>>> result = [numpy.random.bytes(1024*1024) for x in range(10240)]
Killed
root@1981990bd882:/#

$ sudo docker stats
CONTAINER ID        NAME                CPU %               MEM USAGE / LIMIT     MEM %               NET I/O             BLOCK I/O           PIDS
1981990bd882        pedantic_cray       24.00%              99.37MiB / 100MiB     99.37%              21.8MB / 487kB      300MB / 14.9GB      5
```
### Limit CPU
```
$ sudo docker run -it -m 100m --memory-swap 100m --cpus 0.1 python bash
```
## Remove containers
```
$ sudo docker ps -a
CONTAINER ID        IMAGE                             COMMAND                  CREATED             STATUS                       PORTS                    NAMES
6442ef2f8a2c        python                            "bash"                   6 minutes ago       Exited (130) 9 seconds ago                            tender_brattain
1981990bd882        python                            "bash"                   17 minutes ago      Exited (137) 7 minutes ago                            pedantic_cray
56a49f92bd7e        pythonincontainers/simple-flask   "/bin/sh -c 'python …"   29 minutes ago      Up 29 minutes                0.0.0.0:5000->5000/tcp   simple-flask

$ sudo docker rm -f $(sudo docker ps -a -q)
6442ef2f8a2c
1981990bd882
56a49f92bd7e
```

# Running Multiple Containers
> Needs proper networking
```
$ sudo docker run -d -p 5000:5000 --name simple-flask pythonincontainers/simple-flask
```
## Access flask app from host
```
$ curl 127.0.0.1:5000
Flask Hello world! Version 1
```

## Access flask app from another container
```
$ sudo docker run -it --name centos centos
[root@8d8a9f3243ac /]# curl 127.0.0.1:5000
curl: (7) Failed to connect to 127.0.0.1 port 5000: Connection refused
```

## get containers IP
```
$ sudo docker inspect --format "{{.NetworkSettings.IPAddress}}" simple-flask
172.17.0.2
$ sudo docker inspect --format "{{.NetworkSettings.IPAddress}}" centos
172.17.0.3
```

## Access flask app from another container using IP
```
$ sudo docker run -it --name centos centos
[root@71a732cba418 /]# curl 172.17.0.2:5000
Flask Hello world! Version 1
```

## Add simple-flask to /etc/hosts of container
```
$ sudo docker run --rm -it --name centos --add-host simple-flask:172.17.0.2 centos
[root@d11c21c5d670 /]# cat /etc/hosts
127.0.0.1	localhost
::1	localhost ip6-localhost ip6-loopback
fe00::0	ip6-localnet
ff00::0	ip6-mcastprefix
ff02::1	ip6-allnodes
ff02::2	ip6-allrouters
172.17.0.2	simple-flask
172.17.0.3	d11c21c5d670
[root@d11c21c5d670 /]# 
[root@d11c21c5d670 /]# curl simple-flask:5000 
Flask Hello world! Version 1
```


## Add vnet
> Use virtual network vnet to group all containers in one network and all the containers will be able to talk with each another using hostnames

## Create virtual network
```
$ sudo docker network create my-vnet
```

## Add containers to the virtual network and access flask
```
$ sudo docker run -d --name simple-flask --network my-vnet pythonincontainers/simple-flask

$ sudo docker run --rm -it --name centos --network my-vnet centos
[root@29ca1ef0e206 /]# curl simple-flask:5000
Flask Hello world! Version 1
```

## setup postgress database container and access it using pgadmin container
![](./images/17.png)

```
$ sudo docker run -d --name posgres --network my-vnet --env "POSTGRES_PASSWORD=mysecret" postgres

$ sudo docker logs --tail 1 posgres
2020-06-11 04:35:36.327 UTC [1] LOG:  database system is ready to accept connections

$ sudo docker run -d --name pgadmin --network my-vnet -e "PGADMIN_DEFAULT_EMAIL=user@example.com" -e "PGADMIN_DEFAULT_PASSWORD=supersecret" -p 8088:80 dpage/pgadmin4
```

## Access pgadmin from host
![](./images/18.png)
![](./images/19.png)
![](./images/20.png)

## set connection to postgres database
![](./images/21.png)
![](./images/22.png)

## create new database called mydatabase
![](./images/23.png)
![](./images/24.png)
![](./images/25.png)

## use sqlalchemy to update database
```
$ git clone https://github.com/pythonincontainers/sqlalchemy-psql.git

$ docker run --rm -it -v ${PWD}:/app --network my-vnet python bash
root@a78db869ffbc:/# cd /app/
root@a78db869ffbc:/app# pip install -r requirements.txt 
Collecting psycopg2
  Downloading psycopg2-2.8.5.tar.gz (380 kB)
     |████████████████████████████████| 380 kB 150 kB/s 
Collecting sqlalchemy
  Downloading SQLAlchemy-1.3.17-cp38-cp38-manylinux2010_x86_64.whl (1.3 MB)
     |████████████████████████████████| 1.3 MB 423 kB/s 
Building wheels for collected packages: psycopg2
  Building wheel for psycopg2 (setup.py) ... done
  Created wheel for psycopg2: filename=psycopg2-2.8.5-cp38-cp38-linux_x86_64.whl size=500518 sha256=6461212f046740f647308dadc8fa2c4fbb57552d4afdec81ada8199c787be9b7
  Stored in directory: /root/.cache/pip/wheels/35/64/21/9c9e2c1bb9cd6bca3c1b97b955615e37fd309f8e8b0b9fdf1a
Successfully built psycopg2
Installing collected packages: psycopg2, sqlalchemy
Successfully installed psycopg2-2.8.5 sqlalchemy-1.3.17
root@a78db869ffbc:/app# 
root@a78db869ffbc:/app# python alchemy-psql.py
```

## person table created and populated with data from alchemy-psql.py
![](./images/26.png)

# Container Networking
## View all networks
```
$ docker network ls
NETWORK ID          NAME                   DRIVER              SCOPE
f094375d36c6        bridge                 bridge              local
46d548312e32        frappedocker_default   bridge              local
67f31866166a        host                   host                local
0fcf8cac2e33        my-net                 bridge              local
978b606f5105        my-vnet                bridge              local
2275499b573c        none                   null                local
489fcda7f785        snakeeyes_default      bridge              local
```
## delete network
```
$ docker network rm my-net
my-net
```
## custom subnet
```
$ docker network create --subnet 10.10.0.0/16 my-addr

$ docker run --rm -it --name alpine1 --network my-addr alpine
/ # ifconfig 
eth0      Link encap:Ethernet  HWaddr 02:42:0A:0A:00:02  
          inet addr:10.10.0.2  Bcast:10.10.255.255  Mask:255.255.0.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:52 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:6851 (6.6 KiB)  TX bytes:0 (0.0 B)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

/ # 
```
## start another container
```
$ docker run --rm -it --name alpine2 alpine
/ # ifconfig 
eth0      Link encap:Ethernet  HWaddr 02:42:AC:11:00:02  
          inet addr:172.17.0.2  Bcast:172.17.255.255  Mask:255.255.0.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:26 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:3142 (3.0 KiB)  TX bytes:0 (0.0 B)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

 
```
## connect alpine2 to my-addr network
```
$ docker network connect my-addr alpine2
```
## ifconfig on alpine2 again
```
/ # ifconfig 
eth0      Link encap:Ethernet  HWaddr 02:42:AC:11:00:02  
          inet addr:172.17.0.2  Bcast:172.17.255.255  Mask:255.255.0.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:28 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:3319 (3.2 KiB)  TX bytes:0 (0.0 B)

eth1      Link encap:Ethernet  HWaddr 02:42:0A:0A:00:03  
          inet addr:10.10.0.3  Bcast:10.10.255.255  Mask:255.255.0.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:14 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:1798 (1.7 KiB)  TX bytes:0 (0.0 B)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

/ #
```

## create LAN only network
```
$ docker network create --internal int-net

$ docker run -dit --name int1 --network int-net alpine

$ docker run -dit --name int2 --network int-net alpine
```

# Data Persistency - Volumes
> docker container are stateless
> file will exist as long container exists

```
$ docker run -it --name mypython python bash
root@709220a34b5e:/# mkdir /app
root@709220a34b5e:/# cd /app
root@709220a34b5e:/app# touch hi.txt
root@709220a34b5e:/app# 
root@709220a34b5e:/app# exit

$ docker start -i mypython
root@709220a34b5e:/# ls -l /app/hi.txt 
-rw-r--r-- 1 root root 0 Jun 11 15:25 /app/hi.txt
root@709220a34b5e:/# exit

$ docker rm mypython

$ docker run -it --name mypython python bash
root@3d7cd75e7cbb:/# ls -l /app/hi.txt
ls: cannot access '/app/hi.txt': No such file or directory
```

## create volume
```
$ docker volume create my-vol
```
## volume location
```
$ docker volume inspect my-vol
[
    {
        "CreatedAt": "2020-06-11T23:33:08+08:00",
        "Driver": "local",
        "Labels": {},
        "Mountpoint": "/var/lib/docker/volumes/my-vol/_data",
        "Name": "my-vol",
        "Options": {},
        "Scope": "local"
    }
]
```

## create container with volume
```
$ docker run -it --name mypyhon --volume my-vol:/app python bash
root@7ff61074210a:/# 
root@7ff61074210a:/# cd /app
root@7ff61074210a:/app# touch hi.txt
root@7ff61074210a:/app# exit

$ docker rm mypyhon

$ docker run -it --name mypyhon --volume my-vol:/app python bash
root@39beaf9e14c0:/# ls -l /app/hi.txt 
-rw-r--r-- 1 root root 0 Jun 11 15:33 /app/hi.txt
```

## delete volume
```
$ docker volume rm my-vol
```

## Docker Bind Mount for local development
![](./images/27.png)
```
$ docker run --rm -it -v ${PWD}:/app python bash
root@59ae5351082e:/# touch /app/hello.txt
root@59ae5351082e:/# exit

$ ls -l hello.txt 
-rw-r--r-- 1 root root 0 Jun  11 23:41 hello.txt
```

# Dockerfile Introduction
```
$ git clone https://github.com/pythonincontainers/flask-hello.git

$ cd flask-hello

$ docker run --rm -it -p 5000:5000 -v ${PWD}:/app python bash
root@0a1fdfc71b14:/# cd /app/
root@0a1fdfc71b14:/app# pip install Flask
Collecting Flask
  Downloading Flask-1.1.2-py2.py3-none-any.whl (94 kB)
     |████████████████████████████████| 94 kB 329 kB/s 
Collecting Jinja2>=2.10.1
  Downloading Jinja2-2.11.2-py2.py3-none-any.whl (125 kB)
     |████████████████████████████████| 125 kB 1.8 MB/s 
Collecting click>=5.1
  Downloading click-7.1.2-py2.py3-none-any.whl (82 kB)
     |████████████████████████████████| 82 kB 129 kB/s 
Collecting Werkzeug>=0.15
  Downloading Werkzeug-1.0.1-py2.py3-none-any.whl (298 kB)
     |████████████████████████████████| 298 kB 700 kB/s 
Collecting itsdangerous>=0.24
  Downloading itsdangerous-1.1.0-py2.py3-none-any.whl (16 kB)
Collecting MarkupSafe>=0.23
  Downloading MarkupSafe-1.1.1-cp38-cp38-manylinux1_x86_64.whl (32 kB)
Installing collected packages: MarkupSafe, Jinja2, click, Werkzeug, itsdangerous, Flask
Successfully installed Flask-1.1.2 Jinja2-2.11.2 MarkupSafe-1.1.1 Werkzeug-1.0.1 click-7.1.2 itsdangerous-1.1.0
root@0a1fdfc71b14:/app# export FLASK_DEBUG=True
root@0a1fdfc71b14:/app# python flask-hello.py 
 * Serving Flask app "flask-hello" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

> Problem too many to steps to start flask

## Solution use docker build instead

```
$ cat Dockerfile
FROM python
WORKDIR /myproject
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
ENV FLASK_DEBUG=True
CMD python flask-hello.py
```
## Build the image in the current directory with name flask-hello:1.0
```
$ docker build -t flask-hello:1.0 .
Sending build context to Docker daemon  43.01kB
Step 1/7 : FROM python
 ---> 7f5b6ccd03e9
Step 2/7 : WORKDIR /myproject
Removing intermediate container 72c722095cf4
 ---> a7c863a65188
Step 3/7 : COPY . .
 ---> fd18e75d6eae
Step 4/7 : RUN pip install -r requirements.txt
 ---> Running in 7e8b8ef3c6e0
Collecting Flask
  Downloading Flask-1.1.2-py2.py3-none-any.whl (94 kB)
Collecting click>=5.1
  Downloading click-7.1.2-py2.py3-none-any.whl (82 kB)
Collecting itsdangerous>=0.24
  Downloading itsdangerous-1.1.0-py2.py3-none-any.whl (16 kB)
Collecting Jinja2>=2.10.1
  Downloading Jinja2-2.11.2-py2.py3-none-any.whl (125 kB)
Collecting Werkzeug>=0.15
  Downloading Werkzeug-1.0.1-py2.py3-none-any.whl (298 kB)
Collecting MarkupSafe>=0.23
  Downloading MarkupSafe-1.1.1-cp38-cp38-manylinux1_x86_64.whl (32 kB)
Installing collected packages: click, itsdangerous, MarkupSafe, Jinja2, Werkzeug, Flask
Successfully installed Flask-1.1.2 Jinja2-2.11.2 MarkupSafe-1.1.1 Werkzeug-1.0.1 click-7.1.2 itsdangerous-1.1.0
Removing intermediate container 7e8b8ef3c6e0
 ---> b6297fe84ecc
Step 5/7 : EXPOSE 5000
 ---> Running in d089c4609090
Removing intermediate container d089c4609090
 ---> 28a81b596bd3
Step 6/7 : ENV FLASK_DEBUG=True
 ---> Running in ac59960df036
Removing intermediate container ac59960df036
 ---> 9b16d204150c
Step 7/7 : CMD python flask-hello.py
 ---> Running in 17dd2a500779
Removing intermediate container 17dd2a500779
 ---> 84d85df2f4ae
Successfully built 84d85df2f4ae
Successfully tagged flask-hello:1.0
```
## Execute the created image
> -P will automatically expose default ports
```
$ docker run -d -P --name flask-hello flask-hello:1.0
68cfbe68fa5f5ab12ab7c46fdcad25ff33fabf315621d8c90730fcce8ae9a1dd

$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS              PORTS                     NAMES
68cfbe68fa5f        flask-hello:1.0     "/bin/sh -c 'python …"   About a minute ago   Up About a minute   0.0.0.0:32768->5000/tcp   flask-hello

$ curl 0.0.0.0:32768
Flask Hello world! Version 3
```
![](./images/28.png)
![](./images/29.png)

# Build Container Images
![](./images/30.png)

# Manual Image Build Process

```
$ mkdir manual-build

$ cd manual-build

$ vim hello.py
```
```py
# hello.py
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'
```
## create script for the following commands
![](./images/31.png)
```
$ vim start-app.sh
cd /app
export FLASK_APP='hello'
export FLASK_ENV='development'
export FLASK_RUN_HOST='0.0.0.0'
flask run

$ docker create -it --name manual -p 5000:5000 python /bin/sh
186d22242bba8cd1731b349ed5dfaced77d72061c4f024e79be1fa43c36b05f3

$ docker start -i manual
# mkdir /app
# exit

$ docker cp hello.py manual:/app

$ docker cp start-app.sh manual:/app

$ docker start -i manual
# cd /app
# ls
hello.py  start-app.sh
# chmod +x start-app.sh	
# pip install Flask
Collecting Flask
  Downloading Flask-1.1.2-py2.py3-none-any.whl (94 kB)
     |████████████████████████████████| 94 kB 376 kB/s 
Collecting Werkzeug>=0.15
  Downloading Werkzeug-1.0.1-py2.py3-none-any.whl (298 kB)
     |████████████████████████████████| 298 kB 3.3 MB/s 
Collecting click>=5.1
  Downloading click-7.1.2-py2.py3-none-any.whl (82 kB)
     |████████████████████████████████| 82 kB 150 kB/s 
Collecting Jinja2>=2.10.1
  Downloading Jinja2-2.11.2-py2.py3-none-any.whl (125 kB)
     |████████████████████████████████| 125 kB 1.1 MB/s 
Collecting itsdangerous>=0.24
  Downloading itsdangerous-1.1.0-py2.py3-none-any.whl (16 kB)
Collecting MarkupSafe>=0.23
  Downloading MarkupSafe-1.1.1-cp38-cp38-manylinux1_x86_64.whl (32 kB)
Installing collected packages: Werkzeug, click, MarkupSafe, Jinja2, itsdangerous, Flask
Successfully installed Flask-1.1.2 Jinja2-2.11.2 MarkupSafe-1.1.1 Werkzeug-1.0.1 click-7.1.2 itsdangerous-1.1.0
# /app/start-app.sh
 * Serving Flask app "hello" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 124-729-936
```

```
$ curl 127.0.0.1:5000
Hello, World!
```

## create the image
```
$ docker commit --change "CMD /app/start-app.sh" manual manual-image:1.1
sha256:acc8438ea7edd92ce31ad883f4c67bf15256487bd2bbf8663e43c30b524ccdd9
```

## start the container
```
$ docker run -it --rm -p 5001:5000 manual-image:1.1
 * Serving Flask app "hello" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 326-685-887
```

## access the flask app
```
$ curl 127.0.0.1:5001
Hello, World!
```

# Dockerfile - Automation of Image Build
![](./images/32.png)
