#!/bin/bash 
# Script pour copier des données de MongoDB à Kafka
python3 copie.py mongodb://172.18.0.2:27017/ database collection_test mongodb://172.18.0.12:27017/ database collection_test
sleep 5