import os

def user_home():
    test = os.getcwd()
    count = 0
    directory = ""

    for i in test:
        if i == '/':
            count += 1

        directory += i

        if count == 3:
            return directory

if __name__ == '__main__':
    print("\n############# CREATION DES REPERTOIRES #####################\n")
    home = user_home()

    os.chdir(home)

    if os.path.exists("DataShareSecure/") == False:
        os.makedirs(u"DataShareSecure/")
        print(" Le repertoire DataShareSecure/ a été créé dans votre dossier personnel.")
    else:
        print("Le repertoire DataShareSecure/ existe déjà dans votre dossier personnel")

    os.chdir(home + "DataShareSecure/")

    if os.path.exists("Received/") == False:
        os.makedirs(u"Received")
        print(" Le repertoire Reveived/ a été créé dans le repertoire DataShareSecure/.")
    else:
        print("Le repertoire Received/ existe déjà.")

    if os.path.exists("Encrypted/") == False:
        os.makedirs(u"Encrypted")
        print(" Le repertoire Encrypted/ a été créé dans le repertoire DataShareSecure/.")
    else:
        print("Le repertoire Encrypted/ existe déjà.")

    if os.path.exists("Decrypted/") == False:
        os.makedirs(u"Decrypted")
        print(" Le repertoire Decrypted/ a été créé dans le repertoire DataShareSecure/.")
    else:
        print("Le repertoire Decrypted/ existe déjà.")

    if os.path.exists("ToEncrypt/") == False:
        os.makedirs(u"ToEncrypt")
        print(" Le repertoire ToEncrypt/ a été créé dans le repertoire DataShareSecure/.")
    else:
        print("Le repertoire ToEncrypt/ existe déjà.")

    if os.path.exists("ToSend/") == False:
        os.makedirs(u"ToSend")
        print(" Le repertoire ToSend/ a été créé dans le repertoire DataShareSecure/.")
    else:
        print("Le repertoire ToSend/ existe déjà.")

    if os.path.exists("ToImport/") == False:
        os.makedirs(u"ToImport")
        print(" Le repertoire ToImport/ a été créé dans le repertoire DataShareSecure/.")
    else:
        print("Le repertoire ToImport/ existe déjà.")

    if os.path.exists("Exported/") == False:
        os.makedirs(u"Exported")
        print(" Le repertoire Exported/ a été créé dans le repertoire DataShareSecure/.")
    else:
        print("Le repertoire Exported/ existe déjà.")

    print("\n           *************** THANKS **************           \n")
