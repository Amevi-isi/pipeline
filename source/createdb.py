#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pymongo
import argparse
from mimesis import Generic
from mimesis.enums import Gender
from mimesis.providers.person import Person
from mimesis.providers.address import Address

def inserer_donnees_mongodb(url_connexion, nom_base_donnees, nom_collection, donnees):
    # Connexion à MongoDB
    try:
        client = pymongo.MongoClient(url_connexion)
    finally:
        print("yes\n")

    # Sélection de la base de données
    db = client[nom_base_donnees]

    # Sélection de la collection
    collection = db[nom_collection]

    # Insertion des données dans la collection
    result = collection.insert_one(donnees)
    
    print(f"Données insérées avec succès. ID de l'insertion : {result.inserted_id}")

def supprimer_collection_mongodb(url_connexion, nom_base_donnees, nom_collection):
    # Connexion à MongoDB
    client = pymongo.MongoClient(url_connexion)

    # Sélection de la base de données
    db = client[nom_base_donnees]

    # Suppression de la collection spécifique
    db.drop_collection(nom_collection)

    print(f"La collection {nom_collection} a été supprimée avec succès.")

def lecture_collection_mongodb(url_connexion, nom_base_donnees, nom_collection):
    # Connexion à MongoDB
    client = pymongo.MongoClient(url_connexion)

    # Sélection de la base de données
    db = client[nom_base_donnees]

    # Accès à la la collection spécifique
    collect = db[nom_collection]

    return collect.find()



    
def generer_donnees():
    # Initialisation des fournisseurs de données de `mimesis`
    generic = Generic()
    person = Person()
    address = Address()

    
    # Génération de données fictives pour 1 utilisateur
    user_data = {
        #"_id": person.identifier(),
        "user": person.username(),
        "firstname": person.first_name(),
        "lastname": person.last_name(),
        "gender": person.gender(),
        "birthplace": address.city(),
        "nationality": address.country(),
        "country": address.country(),
        "status": person.occupation(),
        "__v": generic.random.randint(1, 10),
        "email": person.email(),
        "mobile": person.telephone(),
        "addressAbroad": address.address(),
        "addressTogo": address.address(),
        "father": person.full_name(gender=Gender.MALE),
        "mother": person.full_name(gender=Gender.FEMALE),
        "profession": person.occupation(),
        "refEmail": person.email(),
        "refFirst": person.first_name(),
        "refGender": person.gender(),
        "refIdNum": generic.random.randint(1000, 9999),
        # Ajoutez d'autres données en suivant le même modèle pour les champs restants
    }
    return user_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script pour insérer des données dans MongoDB')
    parser.add_argument('url', help='URL de connexion à MongoDB')
    parser.add_argument('database', help='Nom de la base de données')
    parser.add_argument('collection', help='Nom de la collection')
    
    args = parser.parse_args()
    
    donnees = generer_donnees()
    #supprimer_collection_mongodb(args.url, args.database, args.collection)
    inserer_donnees_mongodb(args.url, args.database, args.collection, donnees)
    results = lecture_collection_mongodb(args.url, args.database, args.collection)
    for result in results:
        print(result)  # Affiche les données insérées dans la collection