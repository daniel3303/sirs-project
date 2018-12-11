# sirs-project
Projecto de Segurança Informática em Redes e Sistemas

O certificado (.pem) é uma chave RSA de 4096bits. A chave de desencriptação é:
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
``` ssh
$ python3 manager.py makemigrations
$ python3 manager.py migrate
$ python3 manager.py migrate --database=replica1
$ python3 manager.py migrate --database=replica2
$ python3 manage.py runsslserver --certificate cert.pem --key key.pem
```


## Note:
The command `$ python3 manager.py migrate --database=<replica_name>` must be applied to each replica configured.


# How to run
``` ssh
$ python3 manage.py runsslserver --certificate cert.pem --key key.pem
```

The webapp will be available at https://localhost:8000/app/index.html (you must include the index.html part).

[How to install a self signed certificate on chrome](https://stackoverflow.com/questions/7580508/getting-chrome-to-accept-self-signed-localhost-certificate?page=1&tab=votes#tab-top)


# Usefull tools
https://sqliteonline.com/ - Check the database structure online
