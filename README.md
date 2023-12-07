# Integration-de-donnees

Ce document présente comment intégrer des données de l'API du gouvernement dans une base de données SQL Server Windows.

## Prérequis :

- Environnement Windows
- Installer la base de données SQL Server
- Avoir une base de données créé avec une table code_insee avec trois colonne code_commune_INSEE (nvarchar(50), NULL) , Nom_de_la_commune(nvarchar(50), non NULL) ,  Code_postal(int, non NULL)  (TP1)
- Avoir un utilisateur capable de se connecter, créer, mettre à jours dans la base de données créé précedement
- Installer Python3 sur le PC local


## Présentation des fichiers:

- Information.bak : Backup de ma base de données
- Integrations.py : Fait la connexion à la base de données et transmet les requêtes SQL
- Create_table.sql : Créer la table SQL pour la gestion des LOG
- Vue.sql : Créer la vue qui affiche uniquement les villes du Nord Pas de Calais
- Trigger.sql : Créer un trigger qui se déclenche à l'intégration des codes INSEE-
- Integration.bat : Interface simplifié pour l'utilisateur du choix de l'intégration et de l'authentification à la base de donnée


## Procédure d'utilisation :

1) Récupérer le code source et laisser les fichiers dans le même dossier
2) Lancer le fichier "Integration.bat" (Double click dessus)
3) Renseigner vos identifiants : nom du serveur, nom de la base de données, nom de l'utilisateur de la BDD, mot de passe de l'utilisateur de la BDD
4) Faire le choix de votre intégrations en tapant sur 1,2,3 ou 4
5) Quitter le programme ou faîte une nouvelle intégrations
