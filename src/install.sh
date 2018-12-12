pip3 install requests
pip3 install django
pip3 install django[argon2]
pip3 install django-sslserver
pip3 install cryptography
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py migrate --database=replica1
python3 manage.py migrate --database=replica2
python3 manage.py collectstatic
