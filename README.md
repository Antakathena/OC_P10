# OC_P10


## Training Project : Création d'une API avec le framework Django REST(DRF) :
Nom : SoftDesk
système de gestion de projets BtoB qui permet aux collaborateurs d'énoncer des problèmes et de les commenter


## Infos Générales :
Le projet SoftDesk contient deux app : users et issues_manager
Il est contruit selon l'architecture Django
- le dossier **SoftDesk** contient notamment les settings et les urls,
    dont celles pour bénéficier de l'interface DRF.
    A noter : *simpleJWT* was used for token authentification
        documentation : https://django-rest-framework-simplejwt.readthedocs.io/en/latest/

- l'**app users** contient contient les urls de l'app, les modèles, vues et serializers liés au CustomUser,
- l'**app issues_manager** contient les urls de l'app,  les les modèles, vues et serializers pour :
        - les projets(projects)
        - les problèmes liés à ces projets(issues)
        - les commentaires liés à ces problèmes (comments)
        - la classe d'association pour les contributeurs (contributors).
            Elle fait le lien entre les utilisateurs inscrits et les projects.
- l'API utilise comme base de données *db.sqlite3*, la db fournie par défaut par DRF


## Utilité :
Destiné à des entreprises qui collaborent sur des projets,
l'API doit pouvoir leur permettre de soulever les problèmes rencontrés et de les commenter.


## Fonctionnalités :

### Fonctions :
L'API fourni des endpoints divers.____ lien POTSMAN : [![Run in Postman](https://run.pstmn.io/button.svg)](https://god.gw.postman.com/run-collection/20538001-90b3a3f2-b652-4c2d-a007-02b60cf8f732?action=collection%2Ffork&collection-url=entityId%3D20538001-90b3a3f2-b652-4c2d-a007-02b60cf8f732%26entityType%3Dcollection%26workspaceId%3Dacf1da6b-0679-45fa-8b42-0af0578096fd)

L'utilisateur doit être connecté, sauf pour s'inscrire et se connecter.

Il peut alors créer un projet ou obtenir la liste ou le détail des projets auxquels il collabore.

L'utilisateur connecté et collaborateur d'un projet peut soulever un problème, commenter un problème.

L'auteur d'un projet, d'un problème ou d'un commentaire peut seul le modifier ou le supprimer.


## Une méthode possible pour explorer l'API
Dans un terminal, utiliser les commandes suivantes :

$ python3 -m venv env 
(créé un dossier env dans le répértoire où vous vous trouvez)
ou créez un autre environnement virtuel

$ source env/bin/activate (sous linux) ou env\Scripts\activate.bat (pour activer l'environnement virtuel sous windows)

$ git clone https://github.com/Antakathena/OC_P10

$ cd ../chemin/du/dossier (de la copie de OC_P10 dans votre dossier env)

$ pip install -r requirements.txt

$ cd src

Une fois dans le dossier src, utiliser la commande 

$ python manage.py runserver

Vous pourrez alors explorer localement l'app
sur votre navigateur à l'adresse http://127.0.0.1:8000/
