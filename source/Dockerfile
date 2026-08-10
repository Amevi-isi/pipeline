FROM python:3.10 

RUN mkdir source
WORKDIR /source
COPY requirements.txt .
COPY createdb.py .
RUN pip install --no-cache-dir -r requirements.txt 
CMD ["python3", "createdb.py", "mongodb://mongodb1:27017/", "database", "collection_test"]

