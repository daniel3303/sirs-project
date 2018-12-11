# sirs-project
SIRS Project - GROUP A43

In this repository we include our CA, OpenSSL configurations and self-signed certificates for localhost.
The key to decrypt our db-key.pem RSA private key is: `@!Sa#XA&4A7PJF`


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

You can also add our CA certificate (ca-certificate.crt) to your trusted roots. To do so follow the steps in the article below.
[How to install a self signed certificate on chrome](https://stackoverflow.com/questions/7580508/getting-chrome-to-accept-self-signed-localhost-certificate?page=1&tab=votes#tab-top)

# OpenSSL
The confiration used for OpenSSL is included in this repository under the folder `openssl`.
Here is a brief explaination for the most important files in that folder.

| File | Description |
| ------ | -------------------- |
|private/cakey.pem | It is our CA private key |
|cacert.crt| Our CA certificate (that should be added to your browser trusted roots) |
|caconfig.cnf  | OpenSSL confiration used to create our CA and to sign new certificate signing requests   |
|index.txt  | Our CA database |
|localhost.cnf | OpenSSL configuration used to generate a certificate signing request for our application's server |
|server_crt.pem | Our application's server public key|
|server_key.pem | Our application's server private key|

We did not use our CA to sign our 8192bits RSA key used to encrypt our database symmetrical keys because it was not necessary.

# Usefull tools
https://sqliteonline.com/ - Check the database structure online
