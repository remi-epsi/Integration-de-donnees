# Integration-de-donnees

Ce document présente comment intégrer des données de l'API du gouvernement dans une base de données SQL Server Windows.

Prérequis :

- Environnement Windows
- Installer la base de données SQL Server
- Avoir une table code_insee avec trois colonne code_commune_INSEE (nvarchar(50), NULL) , Nom_de_la_commune(nvarchar(50), non NULL) ,  Code_postal(int, non NULL)  (TP1)
- Installer Python3 sur le PC local


Présentation des fichiers:

- Integrations.py : Fait la connexion à la base de données et transmet les requêtes SQL
- Create_table.sql : Créer la table SQL pour la gestion des LOG
- Vue.sql : Créer la vue qui affiche uniquement les villes du Nord Pas de Calais
- Trigger.sql : Créer un trigger qui se déclenche à l'intégration des codes INSEE-
- Intergration.bat : Interface simplifié pour l'utilisateur du choix de l'intégration et de l'authentification à la base de donnée
