@echo off

echo Merci de renseigner vos donnees d'authentification a la base de donnees

set /p nom_serveur="Entrer le nom du serveur : "
set /p nom_bdd="Entrer le nom de votre base de donnees : "
set /p nom_utilisateur="Entrer votre nom d'utilisateur : "
set /p mdp="Entrer votre mot de passe : "

python3 integrations.py %nom_serveur% %nom_bdd% %nom_utilisateur% %mdp%

pause