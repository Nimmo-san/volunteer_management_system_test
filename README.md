# NHS Volunteer Management System

# Deployment plan

1. Add a Dockerfile for the Django app (gunicorn).
2. Add docker-compose.yml with:
    - django-web (Django + gunicorn)
    - db (Postgres)
3. Small entrypoint.prod.sh for migrations + collectstatic.



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

Serving frontend, using NGINX

- "try_files $uri $uri/ /index.html" is required so client-side routes (Vue Router in history mode) returns index.html
- changing to VITE_API_BASE_URL=/api for same-origin api calls in prod, for simpler CORS
- using relative /api, the frontend can be served over https
- adding auth cookies, need to set proxy_set_header and configure Django "SECURE_PROXY_SSL_HEADER"