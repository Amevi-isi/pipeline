from pymongo import MongoClient
from confluent_kafka import Producer
from confluent_kafka.cimpl import KafkaException
from confluent_kafka.admin import AdminClient, NewTopic
from datetime import datetime, timedelta
import argparse
import json

def lecture_par_minute(url_connexion: str, nom_base_donnees: str, nom_collection: str):
    # Connexion à MongoDB
    print("Connexion à MongoDB")
    client = MongoClient(url_connexion)
    # Sélection de la base de données
    db = client[nom_base_donnees]
    # Accès à la la collection spécifique
    collection = db[nom_collection]

    # Calculer le timestamp d'il y a une minute
    last_minute = datetime.now() - timedelta(minutes=1)
    # Récupérer les données ajoutées dans la dernière minute
    new_data = collection.find({"createdAt": {"$gte": last_minute}})
    # Convert the cursor to a list of dictionaries
    data_list = [doc for doc in new_data]
    print(f"données à enyoyé: {data_list} ok")
    # Convert the list to JSON
    json_data = json.dumps(data_list, default=str, indent=4)
    return json_data
def production(topic, bootstrap_servers, data):
    # Configuration du producteur Kafka
    producer_conf = {
        'bootstrap.servers': bootstrap_servers
    }
    
    try:
        producer = Producer(producer_conf)
        producer.produce(topic, key='key', value=data) #,
        producer.flush()
        print(f"Données publiées sur le topic '{topic}'")
    except KafkaException as e:
        print(f"Erreur Kafka lors de la production : {e}")
    except Exception as e:
        print(f"Erreur inattendue lors de la production : {e}")
    finally:
        print("producer produit")
        #producer.close()

def create_topic_if_not_exists(bootstrap_servers, topic, num_partitions=1, replication_factor=1):
    admin_conf = {'bootstrap.servers': bootstrap_servers}
    admin_client = AdminClient(admin_conf)

    topic_metadata = admin_client.list_topics(timeout=5)
    
    if topic not in topic_metadata.topics:
        new_topic = NewTopic(topic, num_partitions, replication_factor)
        fs = admin_client.create_topics([new_topic])

        for topic, f in fs.items():
            try:
                f.result()  # Attend que le résultat soit disponible
                print(f"Le topic '{topic}' a été créé avec succès.")
            except KafkaException as e:
                print(f"Erreur lors de la création du topic '{topic}': {e}")
    else:
        print(f"Le topic '{topic}' existe déjà.")

    #admin_client.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script pour copier d'une base de données à une autre")
    parser.add_argument('url', help='URL de connexion de la base de données qui contient les données')
    parser.add_argument('database', help='Nom de la base de données source')
    parser.add_argument('collection', help='Nom de la collection source')
    parser.add_argument('topic', help='le nom du topic sur lequel se fera la publication')
    parser.add_argument('url_kafka', help='bootstrap_servers sur lequel lo topic a ete creer')
    
    args = parser.parse_args()
    print("Lecture des données 1")
    donnees = lecture_par_minute(args.url, args.database, args.collection)
    print("Lecture des données")
    create_topic_if_not_exists(args.url_kafka, args.topic)
    print(f"creation du topic {args.topic}")
    production(args.topic, args.url_kafka, donnees)
    print("Publication des données")
