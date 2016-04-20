FROM python:2.7

# Copy source code
WORKDIR /recast-newfrontend
COPY . /recast-newfrontend/

# Install dependencies using setup file
RUN pip install -e . --process-dependency-links

# Add user
RUN groupadd -r recast && useradd -r -g recast recast

EXPOSE 5000
USER recast

CMD ["recast-frontend", "server"]