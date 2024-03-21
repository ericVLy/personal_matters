# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.11.8-alpine3.18

# Add user that will be used in the container.
RUN addgroup -g 1000 -S wagtail && adduser wagtail -h /home/wagtail -D -G wagtail  -u 1000 -s /bin/sh 

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system packages required by Wagtail and Django.
RUN apk update && apk upgrade && apk add  nodejs npm

# Install the application server.
RUN pip install "gunicorn==20.0.4"

# Install the project requirements.
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Use /app folder as a directory where the source code is stored.
WORKDIR /home/wagtail

# Set this directory to be owned by the "wagtail" user. This Wagtail project
# uses SQLite, the folder needs to be owned by the user that
# will be writing to the database file.
RUN chown wagtail:wagtail /home/wagtail

# Copy the source code of the project into the container.
COPY --chown=wagtail:wagtail . .

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

# Collect static files.
# RUN python manage.py collectstatic --noinput --clear

# Runtime command that executes when "docker run" is called, it does the
# following:
#   1. Migrate the database.
#   2. Start the application server.
# WARNING:
#   Migrating database at the same time as starting the server IS NOT THE BEST
#   PRACTICE. The database should be migrated manually or using the release
#   phase facilities of your hosting platform. This is used only so the
#   Wagtail instance can be started with a simple "docker run" command.
CMD set -xe; python manage.py collectstatic --noinput --clear; \
python manage.py install_node_dependencies; \
python manage.py makemigrations --noinput; \
python manage.py migrate --noinput; \
gunicorn personal_matters.wsgi:application
