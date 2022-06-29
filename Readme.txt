Exécuter en premier le fichier create_directory.py
Exécuter ensuite le fichier Public_Key_Manage.py


CONSTAT

Lorsque vous essayer d'importer une clé, toutes les clés correspondant au mail renseigné sont importés et ceux qui ne
correspondent pas sont supprimés.

###########################

2.3.2 DataShareSecure

Le respect des recommandations précitées vous aideront inévitablement à protéger vos données.
L’une des recommandations est de chiffrer les données avant l’envoi et de mettre en place une signa-
ture électronique. Ce qui permettrait aux expéditeurs d’envoyer un courrier confidentiel, authentique
et intègre. C’est exactement ce à quoi notre solution DataShareSecure concoure.

2.3.2.1 PRESENTATION

DataShareSecure est un programme écrit en langage python qui permet à l’utilisateur de communi-
quer avec son correspondant de maniére sécurisée au moyen de fichiers sur lesquelles sont appliqués
des mécanismes permettant d’assurer la confidentialité de l’information, l’intégrité de l’information
reçue et l’authenticité de l’information.

2.3.2.2 DESCRIPTION

1. create_directory.py

Le fichier create_directory.py permet de créer les répertoires nécessaires à l’utilisation et au bon
fonctionnement de DataShareSecure. Il permet de créer :

(a) Le répertoire "DataShareSecure/" créé dans le répertoire personnel de l’utilisateur ("/ho-
me/user/" par exemple) qui sera utilisé comme répertoire parent du projet DataShareSecure

(b) Les sous-répertoires de "DataShareSecure/" que sont :
• le répertoire "ToEncrypt/" qui contient les fichiers à chiffrer ;
• le répertoire "ToSend/" qui contient les fichiers chiffrés (.dss), la signature des fichiers
originaux (.asc) et le fichier key_used qui contient la clé utilisée ;
• le répertoire "Received/" qui contient les fichiers reçus par son émetteur c’est-à-dire,
les fichiers contenus dans le "ToSend/" de l’émetteur ;
• le répertoire "Encrypted/" qui contiendra les fichiers à déchiffrer ;
• le répertoire "Decrypted/" qui contiendra les fichiers déchiffrés ainsi que la signature
des fichiers originaux ;
• le répertoire "ToImport/" qui contient les fichiers de clés à importer ;
• le répertoire "Exported/" qui contient les clés publiques exportées de votre trousseau
de clés.

2. Public_Key_M anage.py

Le fichier Public_Key_Manage.py vous permet de gérer les clés de votre trousseau de clés. Son
exécution permet de :

• créer une paire de clés RSA propre à vous qui s’ajoutera à votre trousseau ;
• lister les clés de votre trousseau ;
• envoyer votre clés sur le serveur de clés keyserver.ubuntu.com ;
• exporter votre clé publique ;
• importer les fichiers de clés publiques et recevoir une clé publique depuis le serveur de
clés keyserver.ubuntu.com ;
• supprimer votre paire de clés ;

3. Sender.py

C’est le fichier à exécuter lorsque vous êtes l’émetteur. Il permet le chiffrement des fichiers que
vous désirez envoyer à votre destinataire ainsi que le chiffrement de la clé utilisée. Il crée aussi
les signatures des fichiers originaux pour attester qu’ils proviennent de vous.

4. Receiver.py

C’est le fichier à exécuter lorsque vous êtes le destinataire. Il vous permet de déchiffrer les
fichiers que vous avez reçus de votre correspondant et de vérifier les signatures attestant de
l’intégrité des fichiers reçus et de leurs authenticités par la connaissance de l’émetteur.

2.3.2.3 FONCTIONNEMENT UTILISATION

DÉMARRER

Pour démarrer l’utilisation de DataShareSecure, avant toute chose veiller à :

1. Exécuter le fichier create_directory.py
2. Exécuter le fichier requirements.txt
3. Exécuter le fichier Public_Key_Manage.py afin de générer une paire de clés et envoyez la clé
publique sur le serveur.

ÉMETTEUR

Si vous êtes l’émetteur, le fichier à exécuter est le fichier Sender.py

1. Avant son exécution, veuillez faire une copie des fichiers à envoyer à votre correspondant que
vous placez par la suite dans le répertoire "ToEncrypt/".

2. A l’exécution du fichier Sender.py, que se passe t-il ?!

Une clé AES est généré de manière aléatoire sur la base d’octets aléatoire et d’une chaine aléa-
toire qu’il vous est demamdé de saisir. Cela réduit grandement les chances de voir une même
clé être généré deux fois différentes.

Néanmoims, une vérification est effectué pour confirmer l’utilisabilité de la clé. La clé généré
est utilisable si elle n’a pas déjà été utilisé une fois. Les clés utilisées une fois sont hashés et la
valeur du hash est enregistré dans un fichier. Donc à chaque nouvelle génération de clé, cette
dernière est hashé et on vérifie que la valeur du hash ne se trouve pas dans le fichier de hash.
Si elle s’y retrouve, on procède à une nouvelle génération de clé. Si non, cette clé est utilisé.
La clé utilisable est utilisé pour chiffrer les fichiers contenus dans le répertoire "ToEncrypt/" et
les fichiers chiffrés (.dss) résultant sont enregistrés dans le répertoire "ToSend/". Parallèlement,
les fichiers originaux sont signés en utilisant votre clé privé et les fichiers de signatures (.asc)
sont aussi enregistré dans le répertoire "ToSend/".

À la fin de ce processus, la clé utilisée, est :
• chiffrée avec la clé publique de votre destinataire importée (reçue) depuis le serveur de
clés ;
• signée avec votre clé privée et
• le résultat final est écrit dans le fichier de nom key_used qui est enregistré dans le réper-
toire "ToSend/".

3. Pour une correspondance, il faut donc envoyer à votre destinataire, tout le contenu du réper-
toire "ToSend/" en veillant à n’y apporter aucune modification.

4. À chaque exécution du fichier Sender.py, le contenu du répertoire "ToSend/" est vidé pour faire
place aux nouveaux fichiers à envoyer

5. Quant au contenu du répertoire "ToEncrypt/", veiller à vider son ancien contenu avant d’y
mettre un nouveau contenu pour une nouvelle correspondance.


DESTINATAIRE

Si vous êtes le destinataire, le fichier à exécuter est le fichier Receiver.py

1. Avant son exécution, veuillez faire une copie des fichiers .dss, .asc et key_used que vous avez
reçus de votre émetteur que vous placez dans le répertoire "Received/".

2. À l’exécution du fichier Receiver.py, que se passe t-il ? !

Il est d’abord procéder au déchiffrement du fichier key_used contenant la clé utilisée et à la
vérification de la signature qui y est attachée. Si vous confirmez que la signature appartient à
votre émetteur :
• la clé déchiffrée est utilisé pour procéder au déchiffrement des fichiers chiffrés (.dss) et
• les fichiers résultants sont enregistrés dans le répertoire "Decrypted/".

Il est procédé par la suite à la vérification des signatures des fichiers déchiffrés en les comparant
aux signatures reçues de votre émetteur. Et ce, pour attester de l’intégrité des fichiers reçues et
de leurs authenticité par l’identification de l’émetteur.

Lors de la vérification de la signature attaché à la clé utilisé, si vous ne confirmez pas que
la signature appartient à votre émetteur, nous sommes dans l’obligation d’arrêter l’exécution
du programme. Ceci parce que cela atteste d’une compromission de l’information lors de la
transmission.

3. À chaque exécution du fichier Receiver.py, le contenu des répertoires "Encrypted/" et "Decryp-
ted/" est vidé pour faire place respectivement aux nouveaux fichiers à déchiffrer et déchiffrés.

4. Quant au contenu du répertoire "Received/", veiller à vider son ancien contenu avant d’y
mettre un nouveau contenu pour chaque nouvelle correspondance.