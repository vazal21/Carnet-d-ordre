
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
        self.achats = []
        self.ventes = []

    def ajouter_ordre(self, ordre):
        if ordre.type_ordre.lower() == "achat":
            for vente in self.ventes:
                if vente.prix == ordre.prix:
                    quantite_exec = min(ordre.quantite, vente.quantite)
                    print(f"L'ordre d'achat de {ordre.quantite} au prix de {ordre.prix} a été exécuté "
                          f"avec {quantite_exec} du côté vente au prix de {vente.prix}.")
                    vente.quantite -= quantite_exec
                    ordre.quantite -= quantite_exec
                    if vente.quantite == 0:
                        self.ventes.remove(vente)
                    if ordre.quantite == 0:
                        return
            if ordre.quantite > 0:
                self.achats.append(ordre)
                self.achats = [achat for achat in self.achats if achat.prix is not None]
                self.achats.sort(key=lambda x: x.prix)
        elif ordre.type_ordre.lower() == "vente":
            for achat in self.achats:
                if achat.prix == ordre.prix:
                    quantite_exec = min(ordre.quantite, achat.quantite)
                    print(f"L'ordre de vente de {ordre.quantite} au prix de {ordre.prix} a été exécuté "
                          f"avec {quantite_exec} du côté achat au prix de {achat.prix}.")
                    achat.quantite -= quantite_exec
                    ordre.quantite -= quantite_exec
                    if achat.quantite == 0:
                        self.achats.remove(achat)
                    if ordre.quantite == 0:
                        return
            if ordre.quantite > 0:
                self.ventes.append(ordre)
                self.ventes = [vente for vente in self.ventes if vente.prix is not None]
                self.ventes.sort(key=lambda x: x.prix, reverse=True)

    def afficher_carnet(self):
        print("\nCarnet d'ordres :")
        print("---------------------------------------------------------------------")
        print("|  Achat  |  Quantité  |  Prix  |  Vente  |  Quantité  |  Prix  |")
        print("---------------------------------------------------------------------")
        for i in range(max(len(self.achats), len(self.ventes))):
            if i < len(self.achats):
                print(f"| {self.achats[i].type_ordre.ljust(7)} | {str(self.achats[i].quantite).ljust(10)} | {str(self.achats[i].prix).ljust(6)} |", end="")
            else:
                print(" "*29, end="")
            if i < len(self.ventes):
                print(f" {self.ventes[i].type_ordre.ljust(7)} | {str(self.ventes[i].quantite).ljust(10)} | {str(self.ventes[i].prix).ljust(6)} |")
            else:
                print()

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

