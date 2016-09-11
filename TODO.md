# À faire

## Inscription

* [x] Inscription d'un nouvel utilisateur :
    * [x] Utilise la table User de Django
    * [x] Étend la table avec les champs :
        * [x] show_name : le nom affiché sur BioInfuse
        * [x] role : le rôle de l'utilisateur  (concurrent, jury, admin)
        * [x] associated_key : la clé unique associée à  l'utilisateur pour le concours
* [x] Page de connection
* [x] Page de deconnection
* [x] Ajouter automatiquement une nouvelle clé d'association pour l'utilisateur à la création du compte
  * [ ] Générer une clé d'association uniquement pour les candidats d'un concours ?
* [x] Associer la clé au concours

## Clé d'association

La clé d'association ne peut pas être créée si aucun concours n'est ouvert.

* [ ] À l'ouverture d'un nouveau concours, regénérer des clés d'association pour
les utilisateurs existants qui sont dans la table bioinfuse et qui sont actifs.
* [ ]

## Utilisateurs

* [x] Page de modification de profil pour l'utilisateur (champ role non utilisé)
* [x] Page de soumission de vidéo pour l'utilisateur Concurrent
* [x] Page des vidéos soumises pour l'utilisateur Jury
  * [ ] Fixer le bug d'affichage de la vidéo : s'affiche en local mais pas en ligne
  * [ ] Afficher la note moyenne attribuée à la vidéo par le membre du jury ou par l'ensemble des jury ?
* [x] Page d'évalution d'une vidéo pour l'utilisateur Jury

## Soumission d'une vidéo

* [x] Basée sur l'API de DailyMotion en précisant le compte de JeBiF

## Utilisateurs administrateurs

* [x] Page de gestion des membres
* [x] Page de modification de role pour un utilisateur
* [ ] Page de gestion des vidéos ?
* [ ] Page de suppression de vidéo ?
* [ ] Page de mise à jour de vidéo ?

## Gestion du site

* [x] Création de pages en utilisant le markdown
* [ ] Création d'article en utilisant le markdown
* [ ] Création d'une page pour les vainqueurs des différents concours
* [ ] Afficher un slider qui affiche les concours à venir et en cours
