
from confluent_kafka import Consumer
import json
from pymongo import MongoClient
import argparse
from copie import inserer_donnees_mongodb




def inserer_donnees_mongodb(url_connexion, nom_base_donnees, nom_collection, donnees):
    # Connexion à MongoDB
    client = MongoClient(url_connexion)

    # Sélection de la base de données
    db = client[nom_base_donnees]

    # Sélection de la collection
    collection = db[nom_collection]
    if donnees:
        # Insertion des données dans la collection
        for donnee in donnees:
            critere = {"_id": donnee["_id"],}
            collection.update_one(critere, {'$set': donnee}, upsert=True)
        #result = collection.insert_many(donnees)
        return True
    return False


def consommation(url_connexion, nom_base_donnees, nom_collection, topic, bootstrap_server, group_cons='pipeline'):
    # Configuration Kafka
    bootstrap_servers = bootstrap_server
    topic = topic
    group_id = group_cons
    # Configuration du consommateur Kafka
    consumer_conf = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': group_id,
    'auto.offset.reset': 'earliest'  # Commencer à lire dès le début
    }
    consumer = Consumer(consumer_conf)
    if consumer:
        print("Consommateur Kafka initialisé avec succès")
    else:
        print("Erreur lors de l'initialisation du consommateur Kafka")
        return
    consumer.subscribe([topic])
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                print("pas de message recu")
                continue
            if msg.error():
                print("Erreur lors de la consommation: {}".format(msg.error()))
                continue
            # Conversion du message reçu en json
            json_obj = json.loads(msg.value().decode('utf-8'))
            print(f"données récupérées {json_obj}")
            # inserer les donnees dans une base de données mongo
            print("debut du processus d'insertion")
            if inserer_donnees_mongodb(url_connexion, nom_base_donnees, nom_collection,json_obj):
                print("données insérées avec succès")
            else:
                print("Erreur lors de l'insertion des données.")
    except KeyboardInterrupt:
        pass
    finally:
        print("Fermeture du consommateur Kafka")
        consumer.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script pour copier d'une base de données à une autre")
    parser.add_argument('url', help='URL de connexion de la base de données qui contient les données')
    parser.add_argument('database', help='Nom de la base de données source')
    parser.add_argument('collection', help='Nom de la collection source')
    parser.add_argument('topic', help='le nom du topic sur lequel se fera la publication')
    parser.add_argument('url_kafka', help='bootstrap_servers sur lequel lo topic a ete creer')
    
    args = parser.parse_args()
    consommation(args.url, args.database, args.collection, args.topic, args.url_kafka)
    