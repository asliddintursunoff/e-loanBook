# Runs only once during deployment
release: python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --noinput

# Main web server
web: gunicorn project.wsgi:application --log-file -

# Background Telegram bot process
worker: python telegram_bot.py
