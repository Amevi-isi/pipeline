import argparse
from pymongo import MongoClient



def inserer_donnees_mongodb(url_connexion, nom_base_donnees, nom_collection, donnees):
    # Connexion à MongoDB
    client = MongoClient(url_connexion)

    # Sélection de la base de données
    db = client[nom_base_donnees]

    # Sélection de la collection
    collection = db[nom_collection]
    if donnees:
    # Insertion des données dans la collection
        result = collection.insert_many(donnees)
        return result.acknowledged
    return False
    

def lecture_donnees_mongodb(url_connexion, nom_base_donnees, nom_collection):
    # Connexion à MongoDB
    client = MongoClient(url_connexion)

    # Sélection de la base de données
    db = client[nom_base_donnees]

    # Sélection de la collection
    collection = db[nom_collection]

    # Insertion des données dans la collection
    result = collection.find()
    #data_list = [doc for doc in result]
    #json_data = json.dumps(data_list, default=str, indent=4)
    # Conversion en BSON
    #bson_data = bson.BSON.encode(json_data)
    return result



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script pour copier d'une base de données à une autre")
    parser.add_argument('url_srce', help='URL de connexion de la base de données qui contient les données')
    parser.add_argument('database_srce', help='Nom de la base de données source')
    parser.add_argument('collection_srce', help='Nom de la collection source')
    parser.add_argument('url_dest', help='URL de connexion de la base de données de destination')
    parser.add_argument('database_dest', help='Nom de la base de données destination')
    parser.add_argument('collection_dest', help='Nom de la collection destination')
    
    args = parser.parse_args()
    
    donnees = lecture_donnees_mongodb(args.url_srce, args.database_srce, args.collection_srce)
    try:
        inserer_donnees_mongodb(args.url_dest, args.database_dest, args.collection_dest, donnees)
    except Exception as e:
        print(f"Erreur lors de la lecture des données (copi deja effectue): {e}")
    finally:
        print("vous pouvez continuer")
    """ 
    if inserer_donnees_mongodb(args.url_dest, args.database_dest, args.collection_dest, donnees):
        print("Données insérées avec succès.")
    else:
        print("Erreur lors de l'insertion des données.")
    """   