###########
# BUILDER #
###########

# pull official base image
FROM python:3.8 as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.8

# create directory for the app user
RUN mkdir -p /home/app

# create the app user

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy entrypoint-prod.sh
COPY ./entrypoint.sh $APP_HOME

# copy project
COPY . $APP_HOME

# run entrypoint.prod.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]