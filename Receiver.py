from functions import *
from create_directory import *
from Crypto.Cipher import AES
import os
import shutil
import time


home = user_home()

if os.path.exists(home + "DataShareSecure") == False:
    print("\nNous vous prions de lire le fichier \"Readme.txt\" et de suivre ces consignes.\n")
    sys.exit()

print("BIENVENUE DANS CE PROGRAMME DE DECHIFFREMENT DE FICHIERS\n")

print("######### BON À SAVOIR ##########\n")

print("Vous exécutez ce programme stipule que:\n\n"
      "1- Vous avez pris connaissance du fonctionnement de DataShareSecure grâce au \"Readme.txt\" \n"
      "2- Vous avez exécuté le programme \"Public_Key_Manage.py\" au moins une fois et disposer donc d'une "
                                                        "paire de clés\n"
      "3- Vous désirez déchiffrer des fichiers que vous avez reçus d'un correspondant\n")

print("Si vous ne remplissez pas toutes les conditions du \"BON À SAVOIR\", je vous invite à fermer ce programme.\n"
      "Et à prendre le temps de remplir ces conditions.\n")

choix = input("Remplissez-vous les conditions sus-cités ? (O)ui ou (N)on : ")

if choix == 'O' or choix =='o':
    print("\nBien. Nous pouvons donc continuer\n")

    vide_directory(home + "DataShareSecure/Encrypted")
    vide_directory(home + "DataShareSecure/Decrypted")

    os.chdir(home + "DataShareSecure/Received")

    path = home + 'DataShareSecure/Received/key_used'

    with open(path, "r") as file:
        key_encrypted = file.read()

    key = dechiffrer(key_encrypted)
    buffer_size = 65536  # 64kb

    ########## MOVE FILE ############

    print("######## DECHIFFREMENT DES FICHIERS ET VERIFIVATION DES SIGNATURES ######## \n")

    file_dir = []

    file = [f for f in os.listdir(home + "DataShareSecure/Received") if os.path.isfile(f)]
    for f in file:
        if ".dss" in f:
            shutil.copy(f, home + "DataShareSecure/Encrypted")
        elif ".asc" in f:
            shutil.copy(f, home + "DataShareSecure/Decrypted")

    ########## DECRYPT ###############

    print("\n############# DECHIFFREMENT DES FICHIERS REÇUES ############\n")

    os.chdir(home + "DataShareSecure/Encrypted")

    files_dir = []

    files = [f for f in os.listdir(home + "DataShareSecure/Encrypted") if os.path.isfile(f)]
    for f in files:
        files_dir.append(f)

    for x in files_dir:
        with open(home + "DataShareSecure/Encrypted/" + x, "rb") as f:
            f.seek(0)
            path = home + 'DataShareSecure/Decrypted/' + x
            output_file = open(path[:-4], "wb")
            iv = f.read(16)
            cipher_encrypt = AES.new(key, AES.MODE_CFB, iv=iv)
            buffer = f.read(buffer_size)
            while len(buffer) > 0:
                decrypted_bytes = cipher_encrypt.decrypt(buffer)
                output_file.write(decrypted_bytes)
                buffer = f.read(buffer_size)

    print("Vos fichiers déchiffrés sont enregistrés dans le repertoire \"Decrypted\". \n")

    ########## VERIFY SIGNATURE ###############

    print("\n############ VERIFICATION DES FICHERS REÇUES #################\n")

    os.chdir(home + "DataShareSecure/Decrypted/")

    files_dir = []

    files = [f for f in os.listdir(home + "DataShareSecure/Decrypted/") if os.path.isfile(f)]
    for f in files:
        if ".asc" in f:
            files_dir.append(f)

    for x in files_dir:
        with open(home + "DataShareSecure/Decrypted/" + x, "rb") as f:
            file = x[:-4]
            verified = gpg.verify_file(f, file)
            print(file + " : ", verified.status + "")

    print("\nNOUS VOICI À LA FIN\n")

