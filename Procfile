web: gunicorn smartgym.wsgi --log-file -
web: daphne smartgym.asgi:application --port $port --bind 0.0.0.0
