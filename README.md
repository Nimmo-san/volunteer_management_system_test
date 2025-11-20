# NHS Volunteer Management System

# Deployment plan

1. Add a Dockerfile for the Django app (gunicorn).
2. Add docker-compose.yml with:
    - web (Django + gunicorn)
    - db (Postgres)
3. Small entrypoint.sh for migrations + collectstatic.



# Localhost with no port maps to port 80 automatically
host: localhost
port: 80

# Vue Frontend -> NGINX -> gunicorn flow
User → http://localhost:5173  (Vue dev server)
              |
              | Vue JS running in browser
              v
User → http://localhost/api/...  (API request)
              |
              | host port 80
              v
Docker → nginx:80
              |
              | proxy_pass
              v
Django via Gunicorn on django-web:8000


# Next up: CORS