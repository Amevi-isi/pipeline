FROM python:3.10 

RUN mkdir  -p ingestion/cons
# Copier les fichiers dans le conteneur
COPY copie.py /ingestion/copie.py
COPY production.py /ingestion/production.py
COPY consommation.py /ingestion/consommation.py
COPY requirements.txt /ingestion/requirements.txt
# donner les droits d'execution
#RUN chmod +x entrypoint.sh
# copie dans le conteneur
COPY entrypoint.sh /ingestion/entrypoint.sh
# Répertoire pour l'application
WORKDIR /ingestion
# Installation des dépendances
RUN pip install --no-cache-dir -r /ingestion/requirements.txt 

# les droits d'execution
RUN chmod 0771 entrypoint.sh
# execution des programe
ENTRYPOINT [ "./entrypoint.sh" ]