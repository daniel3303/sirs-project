python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py migrate --database=replica1
python3 manage.py migrate --database=replica2
python3 manage.py collectstatic
