FROM python:2.7

#install some things beforehand for better caching
RUN pip install \
    'Flask==0.10.1'\
    'Flask-Login'\
    'Flask-SQLAlchemy'\
    'Flask-WTF'\
    'flask-api'\
    'click'\
    'pyyaml'\
    'celery'\
    'redis'\
    psycopg2

# Copy source code
WORKDIR /recast-newfrontend
COPY . /recast-newfrontend/

# Install dependencies using setup file
RUN pip install -e . --process-dependency-links

# Add user
RUN groupadd -r recast && useradd -r -g recast recast

EXPOSE 5000
EXPOSE 6379

#USER recast
#CMD ["/run.sh"]
