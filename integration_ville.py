import pyodbc
import requests

'''

Objectif : Insérer dans la BDD Information dans la table code_ville
           une colonne qui ajoute le nombre d'habitant par ville 

'''
# Information de la BDD
nom_serveur = 'LAPTOP-UV063DL6'
nom_base_de_donnees = 'Information'
nom_utilisateur = 'appli'
mot_de_passe = 'Azerty123!'

api_url = "https://geo.api.gouv.fr/communes"

# Connexion à la base de données
connexion_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={nom_serveur};DATABASE={nom_base_de_donnees};UID={nom_utilisateur};PWD={mot_de_passe}'
connexion = pyodbc.connect(connexion_string)
cursor = connexion.cursor()

#Récupère les données via l'API
response = requests.get(api_url)
data = response.json()

#Insére les données dans la BDD
for commune in data:
    code_insee = commune.get("code")
    population = commune.get("population", None)

    if code_insee[0] == '0':
        chaine_abrege = code_insee[1:]
    else:
        chaine_abrege = code_insee

    if population != None:
        sql_query = f"UPDATE Code_ville SET popula = {population} WHERE code_commune_INSEE = '{chaine_abrege}';"
        
        print("Modification OK :" , chaine_abrege)


        cursor.execute(sql_query)
        connexion.commit()

connexion.close()