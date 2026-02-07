
# Fonction pour afficher le menu principal
def affiche_menu():
    print("************************** Systeme de gestion de commande *************************")
    print("1. Ajouter un produit a la commande courante")
    print("2. Supprimer un produit de la commande courante")
    print("3. Afficher la commande courante")
    print("4. Valider la commande courante")
    print("5. Consulter l'historique des commandes")
    print("6. Quitter")
    print()
# Fonction pour ajouter un produit au panier
def ajout_produit(df,panier):
    # saisie du code produit
    code = input("Saisir le code de l'article à ajouter: ").upper()
    # Controle de saisie c.a.d redmander la saisie jusqu a saisir un code existant  ou S pour sortir
    while (len(df.loc[df['asin'] == code]) == 0) and (code != 'S'):#Aucune valeur dans la colonne 'asin' ne correspond au code saisie
        print("Article inexistant!!")                              # et on a pas saisie S
        code = input("Merci de saisir un autre code ou S pour sortir: ").upper()
    # Ajout d'un produit dans le cas ou on a saisi un code valide et non pas S
    if code.upper() != 'S':
        produit = df.loc[df['asin'] == code].values #recuperer les details de produit corespendant au code saisie
        detail = []
        for ligne in produit:             #mettre les details ('asin', 'description', ...) corespondant au produit dans liste detail
            for element in ligne:
                detail.append(element)



        #afficher les details a partir de la liste
        print(f"Code              : {detail[0]}")
        print(f"Description       : {detail[1]}")
        print(f"Prix (Unité)      : {detail[3]}")
        print(f"Note              : {detail[2]}")
        qte = int(input(f"Saisir la quantité pour l'article {code}: "))
        #controle de saisie: accepter que valeur positive
        while qte <= 0:
            qte = int(input('Quantité invalide, veuiller corriger: '))

        if len(panier.loc[panier['code'] == code]) != 0: # verifier est ce que le produit existe dans le panier
            panier.loc[panier['code'] == code, 'quantite'] = qte # changer l'ancien qte par la nouvelle saisie
            print(f"La quantité de l'article {detail[0]} a été mise à jour.")
        else: #Si l'article n'existe pas
            nouvel_article = {     # creer un nouveau article (dictionnaire)
                'code': detail[0],
                'description': detail[1],
                'note': detail[2],
                'prix': detail[3],
                'quantite': qte
            }
            panier.loc[len(panier)] = nouvel_article#  ajouter un nouveau produit a la fin du panier

            print("L'article a été ajouté a votre panier")
    #afficher le menu principal
    affiche_menu()
    return panier
#fonction permettant de supprimer un produit du panier
def  supprimer_produit(panier):

    code = input("Saisir le code de l'article à supprimer du panier: ").upper()

    while (len(panier.loc[panier['code'] == code]) == 0) and (code != 'S'):
        code=input("Article inexistant!! Saisir un autre code ou S pour sortir:")

    produit = panier.loc[panier['code'] == code].values  # recuperer les details de produit corespendant au code saisie
    detail = []
    for ligne in produit:  # mettre les details ('code', 'description', ...) corespondant au produit dans liste detail
        for element in ligne:
            detail.append(element)

    # supprimer le produit  si le produit existe dans le panier et on n'a pas saisie S
    if code.upper() != 'S':
        qte_supp=int(input(f"Saisir la quantite a suprimer de l'article {code} : "))
        #Controle Saisie: la qte a supprimer doit etre entre 0 et la qte dans le panier
        while qte_supp<=0  or qte_supp > detail[4]:
            print("la quantite est incorect")
            qte_supp=int(input(f"Saisir la quantite a suprimer de l'article {code} : "))
        #Mise a jour de la nouvelle qte apres suppression
        panier.loc[panier['code']==code,'quantite'] -=qte_supp
        print("L'article est supprime")
    affiche_menu()
    return panier
#affiche le contenu du panier
def afficher_commande(panier):
    print('#######################################################################################')
    print('################################ Visualiser le panier #################################')
    print('#######################################################################################')
    print()
    nb = 0 #Nombre d'article
    montant_total = 0
    commande = panier.values
    #parcourir les articles pour afficher leur detail et calculer le nombre d'article ainsi que le montant total
    for ligne in commande:
        nb += 1
        montant_total += ligne[3] * ligne[4]
        print(f"Article {nb} :")
        print(f"Code                            : {ligne[0]}")
        print(f"Description                     : {ligne[1]}")
        print(f"Prix (Unité)                    : {ligne[3]}")
        print(f"Note                            : {ligne[2]}")
        print(f"Quantité commandée              : {ligne[4]}")
        print("-------------------------------------------------------------------------------------")
        print()

    print(f'Vous avez commandé {nb} article(s)')
    print(f'Le montant totalde la commande est {montant_total}')
    print()
    print('#######################################################################################')
    print('############################ Fin de visualization du panier ###########################')
    print('#######################################################################################')
    print()
    affiche_menu()

 #Enregistrer la commande dans le fichier texte
def valider_commande(panier):
    client = input('Saisir le nom du client:')
    #recuperer le contenu du panier
    commande = panier.values
    nb_articles = 0
    montant_total = 0
    #ouvrir le fichier historique en mode ecriture (ajout a la fin)
    historique = open("historique.txt", "a")
    historique.write(f'\n Le client est : {client}')
    #parcourir les valeurs du panier pour calculer le nombre total d'article, montant total du panier et afficher la qte par article cmder
    for ligne in commande:
        nb_articles += ligne[4]
        montant_total += ligne[3] * ligne[4]
        historique.write(f'\n     -Code article : {ligne[0]} **** Quantité commandée : {ligne[4]}')
    #afficher le nombre d'article et le montant total du panier
    historique.write(f'\n Nombre d\'articles : {nb_articles}')
    historique.write(f'\n Montant de la commande : {montant_total}')

    historique.close()
    #reinitialisation du panier
    data = {
        'code': [],
        'description': [],
        'note': [],
        'prix': [],
        'quantite': []

    }
    panier = pd.DataFrame(data)
    print('Commande validée et enregistrée...')
    affiche_menu()
    return panier
#afficher le contenu de l'historique
def historique_commande():
    print('#######################################################################################')
    print('################### Consultation de l\'historique des commandes ########################')
    print('#######################################################################################')
    #ouvrir le fichier de l'historique en mode lecture
    historique = open('historique.txt', 'r')
    #lire le contenu du fichier
    donnees = historique.read()
    #afficher le contenu du fichier
    print(donnees)
    historique.close()
    print()
    print('#######################################################################################')
    print('######################### Fin de Consultation de l\'historique #########################')
    print('#######################################################################################')
    print()
    affiche_menu()
import pandas as pd
# Chargement des données de produits à partir du fichier CSV
df=pd.read_csv("produits_amazon (1).csv", sep=",")
# Initialisation du dictionnaire
data={
    'code':[],
    'description':[],
    'note':[],
    'prix':[],
    'quantite':[]

}
#Creation DataFrame panier (panier vide)
panier=pd.DataFrame(data) #il faut dire que la panier est intialement vide
#Appele de la fonction afficher menu pour donner la main a l'utilisateur pour fair son choix
affiche_menu()
choix =input("saisir le choix : ")
#Utilisation du boucle while afin de controler le choix d'utilisateur
while choix!="6":
    if choix=="1":
        ajout_produit(df,panier)
    elif choix=="2":
        supprimer_produit(panier)
    elif choix=="3":
        afficher_commande(panier)
    elif choix=="4":
        valider_commande(panier)
    elif choix=="5":
        historique_commande()
    else:
        print("choix incorrect")
        choix=input("saisir le choix entre 1 et 6 :")

    choix= input("saisir le choix : ")


