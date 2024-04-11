from itertools import zip_longest

DEFAULT_PRICE = 110  # Prix par défaut si le carnet d'ordres est vide
FIXING_DURATION = 2  # Durée du fixing en minutes / le temps pour l'utilisateur de rentrer des ordres d'achat ou de vente en pré-clôture

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

class CarnetOrdres:
    def __init__(self):
        self.ventes = []
        self.achats = []

    def ajouter_ordre(self, ordre):
        if ordre.type_ordre.lower() == "vente":
            self.ventes.append(ordre)
            self.ventes.sort(key=lambda x: x.prix, reverse=True)
        elif ordre.type_ordre.lower() == "achat":
            self.achats.append(ordre)
            self.achats.sort(key=lambda x: x.prix)

    def afficher_carnet(self):
        print("\nCarnet d'ordres :")
        print("--------------------------------------------------------------------------------------------------------------------")
        print("| Ventes | Quantité | Cumul Vente | Cours | Cumul Achat | Quantité | Achats | Écart de transaction |")
        print("--------------------------------------------------------------------------------------------------------------------")
        achats_inverse = sorted(self.achats, key=lambda x: x.prix, reverse=True)
        for vente, achat in zip_longest(self.ventes, achats_inverse, fillvalue=Ordre("", "", "")):
            cumul_vente = sum(v.quantite for v in self.ventes if v.prix >= vente.prix)
            cumul_achat = sum(a.quantite for a in achats_inverse if a.prix <= achat.prix)
            ecart = cumul_vente - cumul_achat
            print(f"| {vente.type_ordre.ljust(6)} | {str(vente.quantite).ljust(8)} | {str(cumul_vente).ljust(11)} | {str(vente.prix).ljust(5)} | {str(cumul_achat).ljust(11)} | {str(achat.quantite).ljust(8)} | {achat.type_ordre.ljust(6)} | {str(ecart).ljust(20)} |")
        print("--------------------------------------------------------------------------------------------------------------------")

    def trouver_prix_marche(self, type_ordre):
        if type_ordre.lower() == "achat":
            if self.ventes:
                prix_marche = min(vente.prix for vente in self.ventes)
            else:
                prix_marche = DEFAULT_PRICE
        elif type_ordre.lower() == "vente":
            if self.achats:
                prix_marche = max(achat.prix for achat in self.achats)
            else:
                prix_marche = DEFAULT_PRICE
        else:
            raise ValueError("Type d'ordre invalide")
        return prix_marche

    def creer_fixing(self, type_fixing, ordres_predefinis=None):
        print(f"Fixing de {type_fixing} en cours...")
        if ordres_predefinis is None:
            ordres_predefinis = []
        for ordre in ordres_predefinis:
            self.ajouter_ordre(ordre)
        if type_fixing.lower() == "ouverture":
            prix_fixing = self.trouver_prix_marche("achat")
            print(f"Prix de fixing de {type_fixing} : {prix_fixing}")
            self.afficher_carnet()

    def creer_fixing_cloture(self):
        print("Fixing de clôture en cours...")
        for _ in range(FIXING_DURATION):
            nouvel_ordre = saisir_nouvel_ordre()
            self.ajouter_ordre(nouvel_ordre)
        prix_fixing = self.trouver_prix_marche("vente")
        print(f"Prix de fixing de clôture : {prix_fixing}")


def creer_carnet_predefini():
    carnet = CarnetOrdres()
    ordres_predefinis = []
    for i in range(1, 11):
        ordres_predefinis.append(Ordre("Achat", i * 10, 100 + i))
        ordres_predefinis.append(Ordre("Vente", i * 10, 110 - i))
    return carnet, ordres_predefinis

def saisir_nouvel_ordre():
    type_ordre = input("Entrez le type d'ordre (Achat/Vente) : ").capitalize()
    quantite = int(input("Entrez la quantité : "))
    prix_de_marche = input("Voulez-vous réaliser votre ordre au prix de marché ? (Oui/Non) : ").lower()

    if prix_de_marche == "oui":
        prix = None
    else:
        prix = float(input("Entrez le prix : "))

    return Ordre(type_ordre, quantite, prix)

carnet, ordres_predefinis = creer_carnet_predefini()
carnet.afficher_carnet()

carnet.creer_fixing("ouverture", ordres_predefinis)  # Fixing d'ouverture

while True:
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
carnet.afficher_carnet()

carnet.creer_fixing_cloture()  # Fixing de clôture

carnet.afficher_carnet()
