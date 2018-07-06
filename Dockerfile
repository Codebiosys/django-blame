FROM python:3.6-alpine AS base

# Add missing packages for Postgres bindings
# Disable caching to keep container small
# https://stackoverflow.com/a/42224405/148781
RUN apk --no-cache add gcc postgresql-dev python3-dev musl-dev

# Declare application root for easier copying of files
WORKDIR /app

# Copy version specs first so they can be cached by Docker
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code last so it can be mounted in Compose
COPY . .

# Using "-u" with python did not work, so set an environment variable
ENV PYTHONUNBUFFERED=0


FROM base AS development
RUN pip install -r requirements-development.txt
RUN pip install -e .


FROM base AS production
RUN pip install .
