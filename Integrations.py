import sys
import pyodbc
import requests

def verif_existe_sql(sql_query):
    cursor.execute(sql_query)
    requete = str(cursor.fetchone())
    if requete == "('1',)":
        res = 1
    else:
        res = 0  
    return res

# Informations de connexion à la BDD
nom_serveur = sys.argv[1]
nom_base_de_donnees = sys.argv[2]
nom_utilisateur = sys.argv[3]
mot_de_passe = sys.argv[4]

connexion_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={nom_serveur};DATABASE={nom_base_de_donnees};UID={nom_utilisateur};PWD={mot_de_passe}'

end=0

while end != 1:

    try:
        # Connexion à la base de données
        connexion = pyodbc.connect(connexion_string)
        cursor = connexion.cursor()

        #Choix de l'intégration par l'utilisateur
        choix= input("\n Quelle inétragtion souhaitez-vous réaliser ? \n 1 - Intégrer un trigger qui se déclenche à l'intégration des codes INSEE (Taper 1) \n 2 - Intégrer une vue qui affiche les villes du Nord Pas de Calais (Taper 2) \n 3 - Ajouter les informations de population à la table (Taper 3) \n 4 - Souhaitez-vous quitter le programme ? (Taper 4) \n Votre choix : \n ")

        match choix:
            #Création de la table de log
            case "1":
                sql_exist = f"IF OBJECT_ID('log_codeINSEE', 'U') IS NOT NULL BEGIN SELECT '1'; END ELSE BEGIN SELECT '0'; END"
                
                if verif_existe_sql(sql_exist) == 0 :
                    with open('create_table.sql','r') as file:
                        sql_query= file.read()
                    cursor.execute(sql_query)
                    print("Création de la table de log OK")     
                else:
                    print("La table log_codeINSEE est déjà créé !")

                sql_exist2 = f"IF OBJECT_ID('Trigger_CodeINSEE', 'TR') IS NOT NULL BEGIN SELECT '1'; END ELSE BEGIN SELECT '0'; END"
                if verif_existe_sql(sql_exist2) == 0:
                    #Crtéation du trigger
                    with open('trigger.sql','r') as file:
                        sql_query= file.read()
                    cursor.execute(sql_query)
                    print("Création du trigger OK \n")
                else:
                    print("Le trigger Trigger_CodeINSEE existe déjà")
                

            #Création de la vue
            case "2":
                sql_exist3 = f"IF OBJECT_ID('vue_departement_59_62', 'V') IS NOT NULL BEGIN  SELECT '1'; END ELSE BEGIN SELECT '0'; END"
                print(verif_existe_sql(sql_exist3))
                if verif_existe_sql(sql_exist3) == 0:
                    with open('vue.sql', 'r') as file:
                        sql_query= file.read()
                    cursor.execute(sql_query)
                    print("Création de la vue OK \n")
                else:
                    print("La vue vue_departement_59_62 existe déjà !")

            #Ajout de la colonne population et des données dans cette colonne
            case "3":

                sql_exist = f"IF COL_LENGTH('Code_INSEE', 'popula') IS NOT NULL BEGIN  SELECT '1'; END ELSE BEGIN SELECT '0'; END"

                if verif_existe_sql(sql_exist) == 0:
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
                else:
                    print("La colonne population existe déjà et les données dont intégrées !")
        
            case "4":
                print("Bonne continuation ! \n")
                sys.exit()

            #Choix autre que 1,2,3 ou 4
            case _:
                print("Votre choix ne correspond pas à 1, 2, 3 ou 4. Veuillez sélectionner l'un de ces trois choix. Le programme se stop.")
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