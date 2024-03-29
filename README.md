# SIRS Project - A43 - Remote document access

In this repository we include our CA, OpenSSL configurations and self-signed certificates for localhost.

Our private key is stored in a Vault and the password to decrypt it is asked once you run the server.

The default password for the Vault is: `@!Sa#XA&4A7PJF`


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
To install the software dependencies execute the following commands:
``` ssh
$ pip3 install requests
$ pip3 install django
$ pip3 install django[argon2]
$ pip3 install django-sslserver
$ pip3 install cryptography
```

After installing the dependencies you need to install the software. To do so execute the following commands (you must be in the folder src):
``` ssh
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py migrate --database=replica1
$ python3 manage.py migrate --database=replica2
$ python3 manage.py collectstatic
```

or optionally use the following script to install all the dependencies and the software in one command:

``` ssh
$ ./install.sh
```


## Quick note:
If you want to configure extra replicas (probably you don´t want this) you need to execute the command `$ python3 manager.py migrate --database=<replica_name>` for each additional replica.


# How to run
To run the software execute the following command:
``` ssh
$ python3 manage.py runsslserver --certificate certificates/https-cert.pem --key certificates/https-key.pem --noreload
```

or equivalently you may run the following script:

``` ssh
$ ./run.sh
```


## Quick note:
Once you run the server it will ask you for a key to decrypt the `Vault` where our private keys are stored. The default password is `@!Sa#XA&4A7PJF`. If you type in a wrong password the server will continue running but it won´t be able to decrypt any files and because of that it will assume that they are corrupted.


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
