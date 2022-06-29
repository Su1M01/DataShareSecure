from functions import *
from Crypto.Cipher import AES
import os

home = user_home()

if os.path.exists(home + "DataShareSecure") == False:
    print("\nNous vous prions de lire le fichier \"Readme.txt\" et de suivre ces consignes.\n")
    sys.exit()

print("\nBIENVENUE DANS CE PROGRAMME D'ENVOI DE FICHIERS SÉCURISÉ\n")

print("######### BON À SAVOIR ##########\n")

print("Vous exécutez ce programme stipule que:\n\n"
      "1- Vous avez pris connaissance du fonctionnement de DataShareSecure grâce au \"Readme.txt\" \n"
      "2- Vous avez exécuté le programme \"Public_Key_Manage.py\" au moins une fois et disposer donc d'une "
                                                        "paire de clés\n"
      "3- Vous désirez chiffrer des fichiers à envoyer à un correspondant\n")

print("Si vous ne remplissez pas toutes les conditions du \"BON À SAVOIR\", je vous invite à fermer ce programme.\n"
      "Et à prendre le temps de remplir ces conditions.\n")

choix = input("Remplissez-vous les conditions sus-cités ? (O)ui ou (N)on : ")

if choix == 'O' or choix =='o':
    print("\nBien. Nous pouvons donc commencer par générer la clé AES à utiliser.\n")
    key = aes_key_gen()
    buffer_size = 65536  # 64kb

    os.chdir(home + "DataShareSecure/")

    print("############## CHIFFREMENT ET SIGNATURE DES FICHIERS ##############\n")

    print("Vous serez amener à signer les fichiers à envoyer.\n"
          "Et pour ce faire, nous aurons besoin de l'empreinte de la clé de l'emetteur (vous)\n"
          "Et nous avons aussi besoin de votre passphrase.\n")

    id = get_key_id()
    phrase = get_pass_user()

    vide_directory(home + "DataShareSecure/ToSend")

    os.chdir(home + "DataShareSecure/ToEncrypt")
    files_dir = []

    files = [f for f in os.listdir(home + "DataShareSecure/ToEncrypt") if os.path.isfile(f)]
    for f in files:
        files_dir.append(f)

    for x in files_dir:
        with open(home + "DataShareSecure/ToEncrypt/" + x, "rb") as f:
            path = home + 'DataShareSecure/ToSend/' + x + ".dss"
            output_file = open(path, "wb")
            cipher_encrypt = AES.new(key, AES.MODE_CFB)
            output_file.write(cipher_encrypt.iv)
            buffer = f.read(buffer_size)
            while len(buffer) > 0:
                ciphered_bytes = cipher_encrypt.encrypt(buffer)
                output_file.write(ciphered_bytes)
                buffer = f.read(buffer_size)
            output_file.close()
            f.seek(0)
            stream = gpg.sign_file(f, keyid=id, passphrase=phrase, detach=True,
                                   output=home + 'DataShareSecure/ToSend/' + x + ".asc")
            print(x + " ", stream.status)

    print("\nVos fichiers chiffrés (.dss) et leurs signature (.asc) sont enregistrés dans "
          "le repertoire \"ToSend\". \n")

    # ********************* Chiffrer la clé AES avec la clé publique du destinataire ******************

    chiffrer(key)

