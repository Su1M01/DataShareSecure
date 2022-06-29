#!/usr/bin/python3

from functions import *
from create_directory import *
import gnupg

home = user_home()

if os.path.exists(home + "DataShareSecure") == False:
    print("\nNous vous prions de lire le fichier \"Readme.txt\" et de suivre ces consignes.\n")
    sys.exit()

gpg = gnupg.GPG(gnupghome= home + 'DataShareSecure/', gpgbinary='/usr/bin/gpg')

print("\nBIENVENUE DANS CE PROGRAMME DE GESTION DE CLES PUBLIQUES\n")

confirm = False
choix = 0

while confirm is not True:
    print("Que voulez vous faire ?\n")
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
        print("Vous n'avez pas saisi un entier. Reprenez\n")
        continue

    if choix != 1 and choix != 2 and choix != 3 and choix != 4 and choix != 5 and choix != 6:
        print("Vous n'avez pas fait un bon choix. Reprenez\n")
        continue
    else:
        confirm = True

while choix:
    if choix == 1:
        key_generator()
        choix = menu()

    if choix == 2:
        list_key()
        choix = menu()

    if choix == 3:
        export_key()
        choix = menu()

    if choix == 4:
        send_key()
        choix = menu()

    if choix == 5:
        import_key()
        choix = menu()

    if choix == 6:
        delete_key()
        choix = menu()
