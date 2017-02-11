# Applications Django de l'association JeBiF

L'association JeBiF met à jour ses applications Django. Dans ce document,
vous trouverez les différents modules réalisés et utilisés par l'assoiation dans
le cadre de son organisation interne et d'autres applications externes et publiques.

## BioInfuse

À l'occasion de la conférence [JOBIM 2016](http://jobim2016.sciencesconf.org/) qui a eu
lieu à Lyon, JeBiF organise un concours de vidéo de vulgarisation scientifique.
Dans ce cadre, l'application BioInfuse permettra :

* de s'inscrire en tant que concurrent (role par défaut), jury ou administrateur
* pour les concurrents, de soumettre leur vidéo qui sera jugé par un jury sélectionné
spécifiquement pour ce concours
* pour les membres du jury, de juger les différentes vidéos proposés par les concurrents
* pour les administrateurs, différentes actions pour gérer les concours (création d'un nouveau
concours, gestion des membres inscrits, rédaction d'information sur les concours)

### Dépendances

* Dailymotion : `pip install dailymotion`
* urllib3, module connexion : `pip install --upgrade urllib3`
* Markdown : `pip install markdown`

### Paramètrages

Pour utiliser cette application dans votre projet, vous devrez modifier les fichiers suivants :

* jebif/localsettings.py.dist : à copier dans jebif/localsettings.py et à modifier au niveau des paramètres attendus par Django (cf. Settings dans la documentation officielle pour plus de détails)
* bioinfuse/parameters.py.dist : à copier dans bioinfuse/parameters.py et à modifier au niveau des paramètres attendus par Dailymotion
  * pour les développeurs impliqués dans le projet, les identifiants seront fournis en privé

# Django applications of JeBiF association

JeBif association is updating its Django applications. In this document, you
will find the different modules developped and used by the association in the aim
of its internal organisation and other external and public applications.

## BioInfuse

For the conference [JOBIM 2016](http://jobim2016.sciencesconf.org/) who took place at Lyon (France),
JeBiF organised a challenge of scientific vulgarisation movie. In this objective, BioInfuse
web application will allow:

* to subscribe as challenger (default role), jury or administrator
* for challengers, to submit their movie that will be by a jury specifically selected for this
challenge
* for jury members, to note each movie submited by challengers
* for administrators, several actions to manage challenges (create a new challenge, manage subscribed
  members, write information for the challenges)

### Dependencies

* Dailymotion : `pip install dailymotion`
* urllib3, connection module : `pip install --upgrade urllib3`
* Markdown : `pip install markdown`

### Parameters

To use this application in your project, you have to edit those files:

* jebif/localsettings.py.dist: copy in jebif/localsettings.py and edit Django parameters (cf. Settings in official
  documentation for more details)
* bioinfuse/parameters.py.dist: copy in bioinfuse/parameters.py and edit Dailymotion parameters
  * for developpers implied in the project, identifiers will be send in private
