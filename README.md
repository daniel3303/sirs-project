# sirs-project
Projecto de Segurança Informática em Redes e Sistemas

O certificado (.pem) é uma chave RSA de 16384bits. A chave de desencriptação é:
8M@!Sa#XA&4A7PJF


# Depencencies
| Module | Installation command |
| ------ | -------------------- |
|python3 | [Python official repository](https://www.python.org/downloads/)
|requests| pip install requests |
|django  | pip install django   |
|argon2  | pip install django[argon2] |
|ssl-server | pip install django-sslserver|
|cryptography | pip install cryptography|


# Installation
To install the software execute the following commands (you must be in the folder src):
``` ssh
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py migrate --database=replica1
$ python3 manage.py migrate --database=replica2
$ python3 manage.py collectstatic
```

or optionally:

``` ssh
$ ./install.sh
```


## Note:
The command `$ python3 manager.py migrate --database=<replica_name>` must be applied to each replica configured.


# How to run
To run the software execute the following commands:
``` ssh
$ python3 manage.py runsslserver --certificate certificates/https-cert.pem --key certificates/https-key.pem
```

or optionally:

``` ssh
$ ./run.sh
```


The webapp will be available at https://localhost:8000/app/index.html (you must include the index.html part).

[How to install a self signed certificate on chrome](https://stackoverflow.com/questions/7580508/getting-chrome-to-accept-self-signed-localhost-certificate?page=1&tab=votes#tab-top)


# Usefull tools
https://sqliteonline.com/ - Check the database structure online
