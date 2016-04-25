FROM python:2.7

# Copy source code
WORKDIR /recast-newfrontend
COPY . /recast-newfrontend/
COPY run.sh /

# Install dependencies using setup file
RUN pip install -e . --process-dependency-links

# Add user
RUN groupadd -r recast && useradd -r -g recast recast

EXPOSE 5000
EXPOSE 6379

USER recast


CMD ["/run.sh"]