from create_directory import *
import gnupg
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import hashlib
from pprint import pprint
import os
import sys
import time
import getpass

home = user_home()

if os.path.exists(home + "DataShareSecure") == False:
    print("\nNous vous prions de lire le fichier \"Readme.txt\" et de suivre ces consignes.\n")
    sys.exit()

gpg = gnupg.GPG(gnupghome= home + 'DataShareSecure/', gpgbinary='/usr/bin/gpg', use_agent = True)


# ************ Fonction pour recuperer les mails enregistres ****

def mail_list():
    mails = []
    for dico in gpg.list_keys():
        chaine = dico["uids"][0]
        i = chaine.index('<')
        j = chaine.index('>')
        chaine = chaine[i + 1:j]
        mails.append(chaine)

    return mails

# ************ Fonction pour supprimer le contenu d'un dossier *****

def vide_directory(path):
    os.chdir(path)
    files = [f for f in os.listdir(path) if os.path.isfile(f)]

    for f in files:
        os.remove(f)

# ************ Menu du gestionnaire de clés *********************

def menu():
    choix = 0

    print("\nSi vous désirez faire autre chose, choisissez le numero correspondant dans ce menu.\n"
          "Si non, entrez un autre caractère, cela vous fera quitter le programme\n")
    print("1- Generer une paire de clés")
    print("2- Lister les clés de votre trousseau")
    print("3- Exporter votre clé")
    print("4- Envoyer votre clé sur le serveur")
    print("5- Importer une clé")
    print("6- Supprimer votre clé")
    print()

    try:
        choix = input("Faites votre choix: ")
        choix = int(choix)
    except ValueError:
        print("\nNous vous remercions d'avoir utilisé ce gestionnaire de clés. A bientôt.\n")
        sys.exit()

    if choix != 1 and choix != 2 and choix != 3 and choix != 4 and choix != 5 and choix != 6:
        print("\nNous vous remercions d'avoir utilisé ce gestionnaire de clés. A bientôt.\n")
        sys.exit()
    else:
        return choix


# ************ Fonction pour supprimer les clés *****************

def delete_key(fing_recv = []):

    if fing_recv == []:
        print("\n################## SUPPRESSION DE CLÉ ##################\n")
        print("Pour supprimer votre paire de clés, vous devriez supprimer votre clé privé en premier.\n"
              "Nous avons donc besoin d'un identifiant de votre clé, ainsi que de votre passphrase.\n"
              "Nous préconisons l'empreinte de la clé pour des raisons de sécurité.\n")

        finger = get_key_id()
        phrase = get_pass_user()

        gpg.delete_keys(finger, True, phrase)

        if str(gpg.delete_keys(finger)) == "ok":
            print("Votre clé a été bien supprimée\n")
        else:
            print("La clé n'a pu être supprimé. Soit aucune clé n'a cette empreinte dans votre trousseau de clé.\n"
                  "Soit la passphrase que vous avez renseigné est erronée.\n")
    else:
        well = True
        for finger in fing_recv:
            if str((gpg.delete_keys(finger))) != "ok":
                well = False

        if well == True:
            print("\nLes clés ne correspondant pas ont été bien supprimé\n")


# ************ Fonction pour lister les clés *********************

def list_key():
    print("\n################## LISTE DES CLÉS DE VOTRE TROUSSEAU ##################\n")
    public_keys = gpg.list_keys()  # same as gpg.list_keys(False)
    private_keys = gpg.list_keys(True)  # True => private keys

    print("PUBLIC KEYS\n")
    pprint(public_keys)
    print("\nPRIVATE KEYS\n")
    pprint(private_keys)


# *********** Fonction pour exporter une clé **********************

def export_key():
    print("\n################## EXPORTATION DE CLÉ ##################\n")
    print("Pour exporter votre clé, nous avons besoin d'un identifiant de ladite clé.\n"
          "Nous préconisons l'empreinte de la clé.\n")

    idget = get_key_id()

    ascii_armored_public_keys = gpg.export_keys(keyids=idget)

    for dico in gpg.list_keys():
        if dico["fingerprint"] == idget:
            chaine = dico["uids"][0]
            i = chaine.index('<')
            chaine = chaine[0:i -1]

            with open(home + 'DataShareSecure/Exported/' + chaine + '_publickeyfile', 'w') as f:
                f.write(ascii_armored_public_keys)

            print("\nVotre clé a été exporté dans le repertoire \"/Exported\".\n")


# ************ Fonction pour importer une clé ****************************

def import_key(chiffre = False):
    print("\n################## IMPORTATION DE CLÉ ##################\n")

    confirm = False
    choix = 0

    if chiffre == False:
        while confirm is not True:
            print("Vous désirez importer les clés depuis des fichiers reçus ou depuis un serveur\n"
                  "1- Depuis les fichiers reçus\n"
                  "2- Depuis un serveur\n")
            # choix = input("Faites votre choix: ")

            try:
                choix = input("Faites votre choix: ")
                choix = int(choix)
            except ValueError:
                print("Vous n'avez pas saisi un entier. Reprenez\n")
                continue

            if choix != 1 and choix != 2:
                print("Vous n'avez pas fait un bon choix. Reprenez\n")
                continue
            else:
                confirm = True
    else:
        choix = 2

    if choix == 1:
        # Importer la clé publique depuis un fichier

        os.chdir(home + "DataShareSecure/ToImport")

        files_dir = []

        files = [f for f in os.listdir(home + "DataShareSecure/ToImport") if os.path.isfile(f)]
        for f in files:
            files_dir.append(f)

        for x in files_dir:
            with open(home + "DataShareSecure/ToImport/" + x, "rb") as f:
                key_data = f.read()
                imported = gpg.import_keys(key_data)

                if imported != []:
                    print("\nLa clé du fichier \"", x, "\" a bien été exporté. \n")

    elif choix == 2:
        # Importer la clé publique du destinataire depuis un serveur de clé

        print("Vous vous apprêtez à importer une clé depuis un serveur")
        print("Vous devriez en premier lieu chercher la clé sur le serveur et confirmer qu'il s'agit bien de celui "
              "de votre correspondant.")
        print("Pour ce, renseignez le mail de votre correspondant\n")

        other_mail = ""
        confirmed = False

        while confirmed is not True:
            other_mail = input("Renseignez le mail : ")
            other_mail_conf = input("Confirmez le mail : ")
            print()

            if other_mail == other_mail_conf:
                if '<' in other_mail or '>' in other_mail:
                    print("Le mail renseigné contient l'un des symboles que voici: '<' ou '>' "
                          "Entrer un mail qui ne contient aucun de ces symboles. Reprenez\n")
                    continue
                else:
                    confirmed = True
                    print("Les mails renseignés correspondent.\n")
            else:
                print("Les entrées ne correspondent pas. Reprenez\n")

        other_key = gpg.search_keys(other_mail, "keyserver.ubuntu.com")
        taille = len(other_key)

        if taille == 0:
            count = 0

            while taille == 0 and count <= 5:
                time.sleep(2)
                other_key = gpg.search_keys(other_mail, "keyserver.ubuntu.com")
                taille = len(other_key)
                count += 1

        if taille == 0:
            print("Nous ne parvenons pas à trouver votre clé sur le serveur. Soit elle ne s'y trouve pas.\n"
                  "Soit vous avez un souci de connexion. Veuillez ressayer ultérieurement.\n")
            sys.exit()

        elif taille == 1:
            keyid = other_key[0]["keyid"]
            print("L'Id de la clé trouvée est : ", keyid)

            other_public = gpg.recv_keys("keyserver.ubuntu.com", keyid)

            count = 0

            while len(other_public.fingerprints) == 0 and count <= 5:
                time.sleep(2)
                other_public = gpg.recv_keys("keyserver.ubuntu.com", keyid)
                count += 1

            if len(other_public.fingerprints) == 0:
                print("Vous rencontrez un souci de connexion. Veuillez verifier et reprendre plus tard.\n")

            else:
                finger = other_public.fingerprints[0]
                print("L'empreinte de la clé importé est : ", finger)

                print("\nVeuillez contacter votre correspondant.\n"
                      "Confirme t-il être le propriétaire de la clé sur base des empreintes identiques ?\n")
                choix = input("(O)ui ou (N)on : ")

                if choix == 'O ' or choix == 'o':
                    print("\nLa clé importé peut donc ainsi être utilisé.\n")
                    gpg.trust_keys(finger, 'TRUST_ULTIMATE')
                    return finger
                else:
                    print("\nMerci pour cette notification. La clé importé sera supprimée\n")
                    list_del = []
                    list_del.append(finger)
                    delete_key(list_del)  
                    print("\nVeuillez contacter votre correspondant pour vous assurer de la présence effective de sa"
                          "clé sur le serveur.\n"
                          "Et ressayer ultérieurement. MERCI ET À BIENTÔT. \n")

        elif taille > 1:
            list_del = []
            dico = []

            for key in other_key:
                keyid = key["keyid"]
                other_public = gpg.recv_keys("keyserver.ubuntu.com", keyid)

                if other_public.fingerprints == []:
                    count = 0

                    while other_public.fingerprints == [] and count <= 5:
                        time.sleep(2)
                        other_public = gpg.recv_keys("keyserver.ubuntu.com", keyid)
                        count += 1

                    if other_public.fingerprints == []:
                        print("Nous ne parvenons pas à trouver l'empreinte de la clé ayant pour ID : ",keyid)
                        continue
                    else:
                        finger = other_public.fingerprints[0]
                else:
                    finger = other_public.fingerprints[0]

                name = key["uids"]

                if name == []:
                    nom = " "
                else:
                    nom = name[0]

                user = (nom, finger)
                dico.append(user)

                list_del.append(finger)

            print("Nous avons trouvé plus d'une clé appartenant au mail : ", other_mail, " que voici :\n")

            for valeur in dico:
                print(valeur)

            print()
            print("\nContactez votre correspondant\n")

            finger = input("Lequel lui appartient : ")

            if finger in list_del:
                print("\nNous notons que l'empreinte : ", finger, " est celui de votre correspondant.")
                choix = input("Vous confirmez : (O)ui ou (N)on : ")

                if choix == 'O' or choix == 'o':
                    print("\nLa clé correspondant sera donc utilisé. Les autres clés seront supprimés.")
                    list_del.remove(finger)
                    delete_key(list_del)
                    gpg.trust_keys(finger, 'TRUST_ULTIMATE')
                    return finger
                else:
                    print("Vous ne confirmez pas. Nous ne pouvons donc pas continuer.\n")
                    delete_key(list_del)
                    sys.exit()
            else:
                print("L'empreinte que vous avez saisi ne figurent pas parmi ceux reçues depuis le serveur.\n"
                      "Contactez votre correspondant pour vous assurer de la présence effective de sa clé sur le "
                      "serveur.\n"
                      "Et ressayer ultérieurement.\n")
                delete_key(list_del)
                sys.exit()

    else:
        print("Vous n'avez pas fait un choix correct.\n")


# ************ Fonction pour envoyer une clé sur un serveur **************

def send_key():
    print("\n################## ENVOI DE CLÉ SUR UN SERVEUR DE CLÉ ##################\n")
    print("Pour envoyer votre clé sur le serveur, nous avons besoin d'un identifiant de ladite clé.\n"
          "Nous préconisons l'empreinte de la clé.\n")

    idget = get_key_id()
    gpg.send_keys('keyserver.ubuntu.com', idget)

    print("Pour confirmer que votre clé a bien été envoyé, nous pouvons la rechercher sur le serveur.\n")

    key_send = gpg.search_keys(idget, "keyserver.ubuntu.com")

    if key_send == []:
        print("La clé n'a pas été retrouvé. Soit l'envoi a échoué dû à une mauvaise connexion,"
              "Soit la clé n'a pas encore été synchronisé sur le serveur."
              "Veuillez ressayer ultérieurement.")
    else:
        print(key_send)
        print("\nVoilà qui confirme la présence de votre clé sur le serveur.\n")

# ************ Fonction pour renseigner l'empreinte d'une clé ************

def get_key_id():
    ids = ""
    confirmed = False

    while confirmed is not True:
        ids = input("Entrer l'empreinte de votre clé: ")
        ids_conf = input("Confirmer l'empreinte: ")
        print()

        if ids == ids_conf:
            confirmed = True
        else:
            print("Les entrées ne correspondent pas. Reprenez\n")
            print()

    return ids

# ********* Fonction pour recuperer la passphrase de l'utilisateur *******

def get_pass_user():
    print()
    pasph = ""
    confirmed = False

    while confirmed is not True:
        pasph = getpass.getpass(prompt=("Entrer votre passphrase: "))
        pasph_conf = getpass.getpass(prompt=("Confirmer la passphrase: "))
        print()

        if pasph == pasph_conf:
            confirmed = True
        else:
            print("Les entrées ne correspondent pas. Reprenez\n")

    return pasph


# ********* Fonction permettant la génération de clés publiques ************

def key_generator():
    print("\nVOUS VOUS APPRETEZ A GENERER UNE PAIRE DE CLÉ RSA\n")

    # Definir la longueur de la clé

    keylenght = 0
    confirmed = False

    while confirmed is not True:
        print("Quel longueur de clé voulez vous utilisez: 1024 ou 2048\n")

        keylenght = input("Faites un choix: ")
        try:
            keylenght = int(keylenght)
        except ValueError:
            print("Vous n'avez pas saisi un entier. Reprenez\n")
            continue

        if keylenght != 1024 and keylenght != 2048:
            print("Vous n'avez pas fait un choix correct. Reprenez\n")
            continue

        keylenght_conf = input("Confirmer votre choix: ")
        try:
            keylenght_conf = int(keylenght_conf)
        except ValueError:
            print("Vous n'avez pas saisi un entier. Reprenez\n")
            continue

        if keylenght == keylenght_conf:
            confirmed = True
            print("Votre choix de la longueur de clé a été bien enrégistré\n")
        else:
            print("Les entrées ne correspondent pas. Reprenez\n")
            print()

    #Definir le nom d'utilisateur

    print()
    name = ""
    confirmed = False

    while confirmed is not True:
        name = input("Entrer votre vrai nom: ")
        name_conf = input("Confirmer votre nom: ")

        if name == name_conf:
            confirmed = True
            print("Votre nom est bien enregistre\n")
            print()
        else:
            print("Les entrées ne correspondent pas. Reprenez\n")
            print()

    # Definir le mail de l'utilisateur

    mail = ""
    confirmed = False

    while confirmed is not True:
        mail = input("Entrer votre vrai mail: ")
        mail_conf = input("Confirmer votre mail: ")

        if mail == mail_conf:
            if '<' in mail or '>' in mail:
                print("\nVotre mail contient l'un des symboles que voici: '<' ou '>' "
                      "\nEntrer un mail qui ne contient aucun de ces symboles. Reprenez\n")
                continue
            else:
                if mail in mail_list():
                    print("Le mail que vous avez renseigné existe déjà. Donner un autre mail. Reprenez.\n")
                    continue
                else:
                    confirmed = True
                    print("Votre mail est bien enregistre\n")
                    print()
        else:
            print("Les entrées ne correspondent pas. Reprenez\n")
            print()

    # Definir la passphrase pour l'utilisateur

    passph = ""
    confirmed = False

    print("Vous avez besoin de renseigner une passphrase. \n"
          "Elle servira à débloquer votre clé quand vous en aurez besoin.\n"
          "Et elle permettra surtout de prévenir son utilisation par un tiers\n")

    while confirmed is not True:
        passph = getpass.getpass(prompt=("Entrer votre passphrase et tenez le secret: "))
        passph_conf = getpass.getpass(prompt=("Confirmer votre passphrase: "))

        if passph == passph_conf:
            confirmed = True
            print("Votre passphrase est bien enregistre\n")
        else:
            print("Les entrées ne correspondent pas. Reprenez\n")

    input_data = gpg.gen_key_input(key_type="RSA", key_length=keylenght, name_real=name, name_email=mail,
                                   passphrase =passph, no_protection = False)
    key = gpg.gen_key(input_data)

    if key.fingerprint is not None:
        print("Votre clé a été générée avec succès.\n")
        print("L'empreinte de votre clé est ", key.fingerprint,
              ".\nNotez la quelque part ou mémoriser la si vous pouvez.\n"
              "Elle vous servira pour divers opérations\n")


# *********** Fonctions permettant la generation de clé AES **************

def aes_key_gen():
    print("\n############ GENERATION DE CLES AES ###############\n")

    print("DataShareSecure vous permet d'utiliser une clé unique par correspondance.\n")
    print("Cette clé,  est générée de manière totalement aléatoire, en utilisant une chaine de caractère\n"
          "qu'il vous sera demandé de renseigner et une suite aléatoire.\n")

    confirmed = False
    while confirmed is not True:
        salt = get_random_bytes(32)
        password = input("Entrer une chaine de caractères : ")

        # Generate the key
        aes_key = PBKDF2(password, salt, dkLen=32)  # Your key that you can encrypt with
        use = hashlib.sha512()
        use.update(aes_key)
        key_hash = use.hexdigest()
        key_hash += "\n"

        ### Faudrait-il chiffrer le fichier AESHash ?! (NON)

        with open(home + 'DataShareSecure/AESHash', 'a+') as hash_file:
            hash_file.seek(0)
            hash = hash_file.readlines()
            if (len(hash) == 0):
                hash_file.write(key_hash)
                confirmed = True
                print("\nVotre clé a bien été généré.\n")
            else:
                if key_hash in hash:
                    print("\nCette clé est déjà utilisé. Veuillez reprendre le processus s'il vous plait.\n")
                    continue
                else:
                    hash_file.write(key_hash)
                    confirmed = True
                    print("\nVotre clé a bien été généré.\n")

    return aes_key

# *********** Fonctions permettant de chiffrer avec une clé publique **********

def chiffrer(str_unencrypted):         
    print("\n###### CHIFFREMENT ET SIGNATURE DE LA CLÉ UTILISÉ ##########\n\n"
          "Nous avons donc besoin de la clé de votre correspondant.\n"
          "Afin que seul lui puisse déchiffrer la clé utilisé.\n")

    finger = import_key(True)

    print("############# RETOUR DANS LA FONCTION DE CHIFFREMENT ########\n")

    print("La clé du destinataire a bien été reçue depuis le serveur.\n"
          "Elle servira à chiffrer la clé AES.\n")
    print("La clé AES devra être signer pour plus de sécurité\n"
          "Nous aurons besoin de l'empreinte de la clé signatrice (la votre) et de votre passphrase\n")

    id = get_key_id()
    phrase = get_pass_user()

    encrypted_data = gpg.encrypt(str_unencrypted, recipients=finger, sign = id, passphrase = phrase)
    encrypted_string = str(encrypted_data)
    print('ok: ', encrypted_data.ok)
    print('status: ', encrypted_data.status)
    print('stderr: ', encrypted_data.stderr)

    path = home + 'DataShareSecure/ToSend/key_used'

    with open(path, "w") as file:
        file.write(encrypted_string)
        file.close()

    print("\nLa clé utilisé a été chiffré et signé sous le nom \"key_used\" et enregistré dans "
          "le répertoire \"/ToSend\". \n")

# *********** Fonctions permettant de dechiffrer avec une clé privée **********

def dechiffrer(str_encrypted):      
    print("\n###### DECHIFFREMENT ET VERIFICATION DE LA CLÉ UTILISÉ ##########\n\n"
          "Nous avons donc besoin de la clé de votre correspondant.\n"
          "Afin de vérifier la signature du fichier de la clé pour attester que ça vient de lui.\n")

    finger = import_key(True)

    print("##### RETOUR DANS LA FONCTION DE DECHIFFREMENT ############ \n")

    print("La clé de votre emetteur a bien été reçue depuis le serveur.\n"
          "Elle servira à vérifier la signature de la clé AES.\n")
    print("Nous avons besoin de votre passphrase pour déchiffrer la clé.")
    my_pass = get_pass_user()

    decrypted_data = gpg.decrypt(str_encrypted, passphrase = my_pass)
    print('ok: ', decrypted_data.ok)
    print('status: ', decrypted_data.status)
    print('stderr: ', decrypted_data.stderr)

    print("\nLes informations du signataire sont: \n\n"
          "USERNAME : ", decrypted_data.username + "\n"
          "KEY_ID : ", decrypted_data.key_id + "\n"
          "FINGERPRINT : ", decrypted_data.fingerprint + "\n"
          "SIGNATURE_ID : ", decrypted_data.signature_id + "\n"
          "TRUST_LEVEL : ", str(decrypted_data.trust_level) + "\n"
          "TRUST_TEST : ", decrypted_data.trust_text + "\n")

    trust = input("Confirmez vous qu'il s'agit de votre correspondant (O)ui ou (N)on : ")

    if trust == 'O' or trust == 'o':
        print("\nNous pouvons poursuivre donc avec le déchiffrement des fichiers en utilisant cette clé\n")
        return decrypted_data.data
    else:
        print("\nNous sommes donc dans l'obligation de ne pas poursuivre\n")
        sys.exit()


if __name__ == '__main__':
    #aes_key_gen()
    #key_generator()
    #delete_key()
    #export_key()
    #send_key()
    #import_key()
    none = 2
