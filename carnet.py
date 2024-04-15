from itertools import zip_longest

DEFAULT_PRICE = 110  # Prix par défaut si le carnet d'ordres est vide
FIXING_DURATION = 2  # Durée du fixing en minutes / le temps pour l'utilisateur de rentrer des ordres d'achat ou de vente en pré-clôture

#on définit la classe ordre avec les attributs : type_ordre, quantite et prix
class Ordre:
    def __init__(self, type_ordre, quantite, prix=None):
        self.type_ordre = type_ordre
        self.quantite = quantite
        self.prix = prix

    def afficher_ordre(self):
        print("Type d'ordre:", self.type_ordre)
        print("Quantité:", self.quantite)
        if self.prix is not None:
            print("Prix: ", self.prix)
        else:
            print("Prix: Au prix de marché")

# on définit la classe CarnetOrdres avec comme liste : ventes / achats
class CarnetOrdres:
    def __init__(self):
        self.ventes = []
        self.achats = []

    #ajoute un nouvel ordre à la liste (soit ventes ou achats)
    def ajouter_ordre(self, ordre):
        if ordre.type_ordre.lower() == "vente":
            self.ventes.append(ordre) #ajoute
            self.ventes.sort(key=lambda x: x.prix, reverse=True) # trie par ordre décroissant
        elif ordre.type_ordre.lower() == "achat":
            self.achats.append(ordre) #ajoute
            self.achats.sort(key=lambda x: x.prix) #trie par ordre croissant

    #affiche le carnet sous la forme d'un tableau
    def afficher_carnet(self):
        print("\nCarnet d'ordres :")
        print("--------------------------------------------------------------------------------------------------------------------")
        print("| Ventes | Quantité | Cumul Vente | Cours | Cumul Achat | Quantité | Achats | Écart de transaction |")
        print("--------------------------------------------------------------------------------------------------------------------")
        achats_inverse = sorted(self.achats, key=lambda x: x.prix, reverse=True)
        for vente, achat in zip_longest(self.ventes, achats_inverse, fillvalue=Ordre("", "", 0)):
            cumul_vente = sum(v.quantite for v in self.ventes if v.prix >= vente.prix) # cumul vente
            cumul_achat = sum(a.quantite for a in achats_inverse if a.prix <= achat.prix) # cumul achat
            ecart = cumul_vente - cumul_achat # écart = cumul vente - cumul achat
            print(f"| {vente.type_ordre.ljust(6)} | {str(vente.quantite).ljust(8)} | {str(cumul_vente).ljust(11)} | {str(vente.prix).ljust(5)} | {str(cumul_achat).ljust(11)} | {str(achat.quantite).ljust(8)} | {achat.type_ordre.ljust(6)} | {str(ecart).ljust(20)} |")
        print("--------------------------------------------------------------------------------------------------------------------")

    #détermine le prix de marché
    def trouver_prix_marche(self, type_ordre):
        #si on souhaite acheter :
        if type_ordre.lower() == "achat": # convertit en minuscule, sinon fonctionne pas
            if self.ventes: # on recherche dans la colonne vente si des ordres de ventes existent à ce prix
                prix_marche = min(vente.prix for vente in self.ventes) # si oui, on renvoit le prix le plus bas
            else:
                prix_marche = DEFAULT_PRICE # si il n'y a pas d'ordre de vente à ce prix, on renvoit le prix par défaut (110)
        elif type_ordre.lower() == "vente":
            if self.achats:
                prix_marche = max(achat.prix for achat in self.achats)
            else:
                prix_marche = DEFAULT_PRICE
        else:
            raise ValueError("Type d'ordre invalide")
        return prix_marche # le prix du marché est stocké

    #calcule le prix de fixing (ouverture et cloture)
    def creer_fixing(self, type_fixing, ordres_predefinis=None):
        print(f"Fixing de {type_fixing} en cours...")
        if ordres_predefinis is not None:
            for ordre in ordres_predefinis:
                self.ajouter_ordre(ordre)
        if type_fixing.lower() == "ouverture":
            prix_fixing = self.trouver_fixing_ouverture()
            self.afficher_carnet()
            print(f"Prix de fixing de {type_fixing} : {prix_fixing}")
        if type_fixing.lower() == "cloture":
            prix_fixing = self.trouver_fixing_cloture()
            self.afficher_carnet()
            print(f"Prix de fixing de {type_fixing} : {prix_fixing}")

    def trouver_fixing_ouverture(self):
        prix_fixing = DEFAULT_PRICE
        for vente in self.ventes:
            cumul_vente = sum(v.quantite for v in self.ventes if v.prix >= vente.prix)
            cumul_achat = sum(a.quantite for a in self.achats if a.prix <= vente.prix)
            ecart = cumul_vente - cumul_achat
            if ecart > 0:
                prix_fixing = vente.prix #prix fixing correspond au prix auquel l'écart de transaction devient positif
                break
        return prix_fixing

    def trouver_fixing_cloture(self):
        prix_fixing = DEFAULT_PRICE
        for _ in range(FIXING_DURATION):
            for vente in self.ventes:
                cumul_vente = sum(v.quantite for v in self.ventes if v.prix >= vente.prix)
                cumul_achat = sum(a.quantite for a in self.achats if a.prix <= vente.prix)
                ecart = cumul_vente - cumul_achat
                if ecart > 0:
                    prix_fixing = vente.prix
                    break
            return prix_fixing

# on créer un carnet déja prédéfini
def creer_carnet_predefini():
    carnet = CarnetOrdres()
    ordres_predefinis = []
    for i in range(1, 11): # à chaque iténiration on ajoute 2 ordres
        ordres_predefinis.append(Ordre("Achat", i * 10, 100 + i))
        ordres_predefinis.append(Ordre("Vente", i * 10, 110 - i))
    return carnet, ordres_predefinis # on stocke ce carnet prédéfini

#on insère les ordres dans le carnet
def saisir_nouvel_ordre():
    type_ordre = input("Entrez le type d'ordre (Achat/Vente) : ").capitalize()
    quantite = int(input("Entrez la quantité : "))
    prix_de_marche = input("Voulez-vous réaliser votre ordre au prix de marché ? (Oui/Non) : ").lower()

    if prix_de_marche == "oui":
        prix = None
    else:
        prix = float(input("Entrez le prix : "))

    return Ordre(type_ordre, quantite, prix) # on stocke l'ordre (type, quantité, prix)


#PROGRAMME PRINCIPAL
carnet, ordres_predefinis = creer_carnet_predefini() # on stocke les 2 valeurs retournées dans 2 variables (carnet et ordres_prédéfinis)
carnet.afficher_carnet()  # on affiche la carnet créer au préalable

carnet.creer_fixing("ouverture", ordres_predefinis)  # Fixing d'ouverture

while True: #on insère de nouveaux ordres apres le calcul de fixing effectué => cotation en continu
    choix = input("Voulez-vous saisir un nouvel ordre ? (Oui/Non) : ").lower()
    if choix == "oui":
        nouvel_ordre = saisir_nouvel_ordre()
        if nouvel_ordre.prix is None:
            nouvel_ordre.prix = carnet.trouver_prix_marche(nouvel_ordre.type_ordre)
        carnet.ajouter_ordre(nouvel_ordre)
    elif choix == "non":
        break
    else:
        print("Veuillez répondre par 'Oui' ou 'Non'.")

carnet.afficher_carnet() #on affiche le carnet avec ces nouvelles ordres

carnet.creer_fixing("cloture")  # Fixing d'ouverture

