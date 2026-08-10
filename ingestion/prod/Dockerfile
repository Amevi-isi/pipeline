FROM python:3.10 

RUN mkdir  ingestion
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
RUN apt-get update && apt-get -y install cron
# Commande pour démarrer cron et exécuter le script au démarrage
#RUN chmod +x /ingestion/entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]
