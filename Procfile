web: python manage.py makemigrations && python manage.py migrate && python manage.py create_superuser && gunicorn project.wsgi && python manage.py collectstatic
worker: python telegram_bot.py
