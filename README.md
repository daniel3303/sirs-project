# sirs-project
Projecto de Segurança Informática em Redes e Sistemas

O certificado (.pem) é uma chave RSA de 4096bits. A chave de desencriptação é:
8M@!Sa#XA&4A7PJF

# Requer Python 3



# Depencencies
django - pip install django

argon2 - pip install django[argon2]

ssl-server - pip install django-sslserver

cryptography - pip install cryptography


# How to run
python3 manage.py runsslserver --certificate cert.pem --key key.pem

install de certificate on chrome: https://stackoverflow.com/questions/7580508/getting-chrome-to-accept-self-signed-localhost-certificate?page=1&tab=votes#tab-top
