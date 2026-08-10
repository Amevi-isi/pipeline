#!/bin/bash 
# Script en boucle continue pour consommer des données de Kafka
python3 consommation.py mongodb://172.18.0.12:27017/ database collection_test topic_ingestion kafka1:19092