import sys
import pyodbc
import requests


end=0

# Informations de connexion à la BDD
nom_serveur = sys.argv[1]
nom_base_de_donnees = sys.argv[2]
nom_utilisateur = sys.argv[3]
mot_de_passe = sys.argv[4]

connexion_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={nom_serveur};DATABASE={nom_base_de_donnees};UID={nom_utilisateur};PWD={mot_de_passe}'


while end != 1:

    try:
        # Connexion à la base de données
        connexion = pyodbc.connect(connexion_string)
        cursor = connexion.cursor()

        #Choix de l'intégration par l'utilisateur
        choix= input("\n Quelle inétragtion souhaitez-vous réaliser ? \n 1 - Intégrer un trigger qui se déclenche à l'intégration des codes INSEE (Taper 1) \n 2 - Intégrer une vue qui affiche les villes du Nord Pas de Calais (Taper 2) \n 3 - Ajouter les informations de population à la table (Taper 3) \n 4 - Souhaitez-vous quitter le programme ? (Taper 4) \n Votre choix : \n ")

        match choix:
            #Créatio de la Vue
            case "1":
                with open('create_table.sql','r') as file:
                    sql_query= file.read()
                cursor.execute(sql_query)
                print("Création de la table de log OK")

                with open('trigger.sql','r') as file:
                    sql_query= file.read()
                cursor.execute(sql_query)
                print("Création du trigger OK \n")

            #Création du Trigger
            case "2":
                with open('vue.sql', 'r') as file:
                    sql_query= file.read()
                cursor.execute(sql_query)
                print("Création de la vue OK \n")

            #Ajout de la colonne population
            case "3":

                sql_query=f"ALTER TABLE Code_INSEE ADD popula NVARCHAR(50)"
                cursor.execute(sql_query)
                connexion.commit()
                print("Ajout de la colonne population dans la table")

                api_url = "https://geo.api.gouv.fr/communes"
                response = requests.get(api_url)
                data = response.json()

                for commune in data:
                    code_insee = commune.get("code")
                    population = commune.get("population", None)

                    if code_insee[0] == '0':
                        chaine_abrege = code_insee[1:]
                    else:
                        chaine_abrege = code_insee

                    if population != None:
                        sql_query = f"UPDATE Code_INSEE SET popula = {population} WHERE code_commune_INSEE = '{chaine_abrege}';"
                        
                        print("Modification OK :" , chaine_abrege)
                        cursor.execute(sql_query)
                        connexion.commit()
                
                print("La colonne population est bien ajoutée \n")
        
            case "4":
                print("Bonne continuation ! \n")
                sys.exit()

            #Choix autre que 1,2,3 ou 4
            case _:
                print("Votre choix ne correspond pas à 1, 2 ou 3. Veuillez sélectionner l'un de ces trois choix. Le programme se stop.")
                sys.exit()

        connexion.commit()
        connexion.close()

    except pyodbc.Error as erreur:
        print("Erreur sur la communication avec la base de données. \n (Vérifier bien les identifiants et les droits) \n Voici l'erreur remontée : \n", erreur)

    end = int(input("Voulez-vous stoppper le progragmme (Taper sur 1) ou ajouter une nouvelle intégration (Taper sur 0) ? \n"))

    #L'utilisateur peut effectué une 2ème intégration
    match end:
        case 1:
            end=1
            print("Bonne continuation ! \n")
        case 0:
            end=0
        case _:
            print("Le choix est différent de 0 ou 1. Le programme se stop.")
            sys.exit()