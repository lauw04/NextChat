Bonjour !! Si vous êtes ici c'est que vous désirez savoir comment faire fonctionner notre super chat inspiré du site bien connu ChatRoulette. Sur ce site de chat par vidéo, vous pouvez rentrer en connexion avec un unique utilisateur et par le simple appui sur un bouton vous changez d'interlocuteur.

Nous avons effectué ce projet à quatre, nos pseudos github sont : Potdecol, Justineantoine, 3bim, lauw04.

Dans notre cas, le principe reste le même mais uniquement avec du chat écrit.

Vous trouverez dans le dossier deux versions du code, les deux sont fonctionnelles et possèdent leur spécificités. Ainsi, la version 1 a été testé d'assez nombreuses fois pour qu'on la considère comme sans bug mais elle est moins optimisée en stockage et en simplicité d'écriture. La version 2 est une version améliorée avec un gain d'optimisation et d'ergonomie pour l'utilisateur, néanmoins sa phase de test ayant été plus courte nous ne pouvons pas assurer qu'elle ne possède aucun bug que nous aurions raté.


Version 1 : (fichiers Serveur.py et Client.py)

Lancer le fichier Serveur.py dans un terminal.

Lancer le nombre d'utilisateurs voulu en exécutant le fichier Client.py dans différents terminaux.

Après avoir choisi leur pseudonyme, les utilisateurs se retrouvent dans un accueil où ils peuvent tous discuter ensemble.

En envoyant le message "start", les utilisateurs se mettent en attente pour commencer une discussion privée.

Quand il y a plusieurs utilisateurs en attente, 2 ou 3 en fonctions des conditions, deux utilisateurs sont selectionnées pour discuter en privé. Ils ne voient plus les messages des utilisateurs dans l'accueil et leur conversation n'est vu que par eux. 

Quand un des utilisateurs en privé veut changer d'interlocuteur, il doit envoyer le message "next". Les deux utilisateurs sont alors remis en attente et ne peuvent pas retomber directement l'un sur l'autre.

A n'importe quel moment, un utilisateur peut quitter le serveur en envoyant "close".

Dans le serveur, la commande list() permet de visualiser les profils connectés et close() permet de fermer le serveur.




Version 2 : (fichier Serveurdict.py et Clientdict.py)

Lancer le fichier Serveurdict.py dans un terminal.

Lancer le nombre d'utilisateurs voulu en exécutant le fichier Clientdict.py dans différents terminaux.

Après avoir choisi leur pseudonyme, les utilisateurs se retrouvent dans un accueil où ils peuvent tous discuter ensemble.

En envoyant le message "start", les utilisateurs se mettent en attente pour commencer une discussion privée.

Quand il y a au moins 3 utilisateurs en attente, deux utilisateurs sont selectionnées pour discuter en privé. Ils ne voient plus les messages des utilisateurs dans l'accueil et leur conversation n'est vu que par eux. 

Quand un des utilisateurs en privé veut changer d'interlocuteur, il doit envoyer le message "next". Les deux utilisateurs sont alors remis en attente. Il y a un petite probabilité qu'ils retombent en communication privée, du au paramètre aléatoire du code.

Quand il est en recherche ou en chat privé, l'utilisateur peut utiliser "lobby" pour retourner dans l'accueil.

A n'importe quel moment, un utilisateur peut quitter le serveur en envoyant "close".

Dans le serveur, la commande list permet de visualiser les profils connectés, research permet de visualiser les profils en recherche et private de visualiser les profils en conversation privée et close permet de fermer le serveur.
