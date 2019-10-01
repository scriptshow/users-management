FROM python:3.7

# Environment variable
ENV ALLOWED_HOSTS 'ALLOWED_HOSTS'
ENV POSTGRES_DB_NAME 'DATABASE_NAME_HERE'
ENV POSTGRES_DB_HOST 'DATABASE_HOST_HERE'
ENV POSTGRES_DB_PORT 'DATABASE_PORT_HERE'
ENV POSTGRES_DB_USERNAME 'DATABASE_USERNAME_HERE'
ENV POSTGRES_DB_PASSWORD 'DATABASE_PASSWORD_HERE'
ENV GOOGLE_OAUTH2_KEY 'GOOGLE_OAUTH_KEY_HERE'
ENV GOOGLE_OAUTH2_SECRET 'GOOGLE_OAUTH_SECRET_HERE'

# change work directory
RUN mkdir -p /users-management
WORKDIR /users-management

ADD ./ /users-management/
RUN pip install -r requirements.txt

EXPOSE 8000
EXPOSE 5432

# Uncomment following lines and comment the test one, to start docker application to work
# RUN ["python", "manage.py", "migrate"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Comment this line once tests done
CMD ["python", "manage.py", "test"]
