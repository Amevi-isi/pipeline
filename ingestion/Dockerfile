FROM python:3.10 

RUN mkdir  ingestion
# Copier les fichiers dans le conteneur
COPY copie.py /ingestion/copie.py
COPY production.py /ingestion/production.py
COPY consommation.py /ingestion/consommation.py
COPY main.py /ingestion/main.py
COPY requirements.txt /ingestion/requirements.txt
# donner les droits d'execution
#RUN chmod +x entrypoint.sh
# copie dans le conteneur
COPY copie.sh /ingestion/copie.sh
COPY prod.sh /ingestion/prod.sh
COPY conso.sh /ingestion/conso.sh
# Répertoire pour l'application
WORKDIR /ingestion
# Installation des dépendances
RUN pip install --no-cache-dir -r /ingestion/requirements.txt 
RUN apt-get update && apt-get -y install cron
# copie dans le conteneur
COPY cronjob /etc/cron.d/cronjob
# Donner les permissions au fichier cronjob
RUN chmod 0644 /etc/cron.d/cronjob
# Appliquer la crontab
RUN crontab /etc/cron.d/cronjob
# Créer un fichier de log pour cron
RUN touch /var/log/cron.log
RUN chmod 0771 copie.sh
#CMD ["./copie.sh" ]
ENTRYPOINT ["python3", "main.py"]
