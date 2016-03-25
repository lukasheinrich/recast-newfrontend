FROM cbora/recast-newfrontend

EXPOSE 5000

RUN pip install --process-dependency-links .

RUN recast-frontend server