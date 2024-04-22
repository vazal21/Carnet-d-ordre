from itertools import zip_longest

DEFAULT_PRICE = 110  # Prix par défaut si le carnet d'ordres est vide
FIXING_DURATION = 2  # Durée du fixing en minutes / le temps pour l'utilisateur de rentrer des ordres d'achat ou de vente en pré-clôture

# Définition de la classe Ordre avec les attributs : type_ordre, quantite et prix
class Ordre:
    def __init__(self, type_ordre, quantite, prix=None):
        self.type_ordre = type_ordre
        self.quantite = quantite
        self.prix = prix

    def afficher_ordre(self):
        print("Type d'ordre:", self.type_ordre)
        print("Quantité:", self.quantite)
        if self.prix is not None:
            print("Prix:", self.prix)
        else:
            print("Prix: Au prix de marché")

# On définit de la classe CarnetOrdres avec comme listes : ventes / achats
class CarnetOrdres:
    def __init__(self):
        self.ventes = []
        self.achats = []

    # Ajoute un nouvel ordre à la liste (soit ventes ou achats)
    def ajouter_ordre(self, ordre):
        if ordre.type_ordre.lower() == "vente":
            self.ventes.append(ordre)
            self.ventes.sort(key=lambda x: x.prix, reverse=True)  # Trie par ordre décroissant
        elif ordre.type_ordre.lower() == "achat":
            self.achats.append(ordre)
            self.achats.sort(key=lambda x: x.prix)  # Trie par ordre croissant

    # Affiche le carnet sous la forme d'un tableau
    def afficher_carnet(self):
        print("\nCarnet d'ordres :")
        print("--------------------------------------------------------------------------------------------------------------------")
        print("| Ventes | Quantité | Cumul Vente | Cours | Cumul Achat | Quantité | Achats | Écart de transaction |")
        print("--------------------------------------------------------------------------------------------------------------------")
        ventes_triees = sorted(self.ventes, key=lambda x: x.prix)  # Tri des ordres de vente par prix croissant
        achats_inverse = sorted(self.achats, key=lambda x: x.prix)  # Tri des ordres d'achat par prix croissant
        for vente, achat in zip_longest(ventes_triees, achats_inverse, fillvalue=Ordre("", "", 0)):
            cumul_vente = sum(v.quantite for v in self.ventes if v.prix <= vente.prix)  # cumul vente
            cumul_achat = sum(a.quantite for a in achats_inverse if a.prix >= achat.prix)
            ecart = cumul_vente - cumul_achat  # écart = cumul vente - cumul achat
            print(f"| {vente.type_ordre.ljust(6)} | {str(vente.quantite).ljust(8)} | {str(cumul_vente).ljust(11)} | {str(vente.prix).ljust(5)} | {str(cumul_achat).ljust(11)} | {str(achat.quantite).ljust(8)} | {achat.type_ordre.ljust(6)} | {str(ecart).ljust(20)} |")
        print("--------------------------------------------------------------------------------------------------------------------")

    # Détermine le prix de marché
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

    # Calcule le prix de fixing (ouverture et cloture)
    def creer_fixing(self, type_fixing, ordres_predefinis=None):
        print(f"Fixing de {type_fixing} en cours...")
        if ordres_predefinis is not None:
            for ordre in ordres_predefinis:
                self.ajouter_ordre(ordre)
        if type_fixing.lower() == "ouverture":
            prix_fixing = self.trouver_fixing_ouverture()
            self.afficher_carnet()
            print(f"Prix de fixing de {type_fixing} : {prix_fixing}")
        elif type_fixing.lower() == "cloture":
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
                prix_fixing = vente.prix
                break
        return prix_fixing

    def trouver_fixing_cloture(self):
        for _ in range(FIXING_DURATION):
            nouvel_ordre = saisir_nouvel_ordre()  # On saisit de nouveaux ordres pendant la période de fixing
            self.ajouter_ordre(nouvel_ordre)

        # Une fois la période de fixing terminée, on détermine le prix de fixing
        prix_fixing = DEFAULT_PRICE
        cumul_vente_initial = sum(vente.quantite for vente in self.ventes)
        cumul_achat_initial = sum(achat.quantite for achat in self.achats)

        for vente in self.ventes:
            cumul_vente = sum(v.quantite for v in self.ventes if v.prix >= vente.prix)
            cumul_achat = sum(a.quantite for a in self.achats if a.prix <= vente.prix)
            ecart = cumul_vente - cumul_achat

            if ecart > 0:
                prix_fixing = vente.prix
                break

        # Vérifier si le fixing a été trouvé et ajuster les quantités en conséquence
        if prix_fixing != DEFAULT_PRICE:
            for vente in self.ventes:
                vente.quantite -= min(vente.quantite, cumul_vente_initial - cumul_achat_initial)
                if vente.quantite <= 0:
                    self.ventes.remove(vente)

            for achat in self.achats:
                achat.quantite -= min(achat.quantite, cumul_vente_initial - cumul_achat_initial)
                if achat.quantite <= 0:
                    self.achats.remove(achat)

        return prix_fixing

    #excécution des ordres
    def executer_ordres(self):
        for vente in self.ventes:
             # Recherche d'un ordre d'achat correspondant à l'ordre de vente
            for achat in self.achats:
                if vente.prix <= achat.prix and vente.quantite > 0 and achat.quantite > 0:
                    # Calculer la quantité à échanger
                    quantite_echangee = min(vente.quantite, achat.quantite)
                    vente.quantite -= quantite_echangee
                    achat.quantite -= quantite_echangee
                    print(f"Ordre exécuté : Vente de {quantite_echangee} actions à {achat.prix} € chacune.")
                    # Si l'un des ordres est complètement exécuté, le retirer du carnet
                    if vente.quantite == 0:
                        self.ventes.remove(vente)
                    if achat.quantite == 0:
                        self.achats.remove(achat)
        # Afficher un message si des ordres restent non exécutés
        for vente in self.ventes:
            if vente.quantite > 0:
                print(f"Ordre de vente partiellement exécuté : {vente.quantite} actions restantes.")
        for achat in self.achats:
            if achat.quantite > 0:
                print(f"Ordre d'achat partiellement exécuté : {achat.quantite} actions restantes.")

# Création d'un carnet pré-défini
def creer_carnet_predefini():
    carnet = CarnetOrdres()
    ordres_predefinis = []
    for i in range(1, 11):
        ordres_predefinis.append(Ordre("Achat", i * 10, 100 + i))
        ordres_predefinis.append(Ordre("Vente", i * 10, 110 - i))
    return carnet, ordres_predefinis

# Saisie d'un nouvel ordre
def saisir_nouvel_ordre():
    type_ordre = input("Entrez le type d'ordre (Achat/Vente) : ").capitalize()
    quantite = int(input("Entrez la quantité : "))
    prix_de_marche = input("Voulez-vous réaliser votre ordre au prix de marché ? (Oui/Non) : ").lower()

    if prix_de_marche == "oui":
        prix = None
    else:
        prix = float(input("Entrez le prix : "))

    return Ordre(type_ordre, quantite, prix)

# PROGRAMME PRINCIPAL
carnet, ordres_predefinis = creer_carnet_predefini()
carnet.afficher_carnet()

carnet.creer_fixing("ouverture", ordres_predefinis)

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

carnet.executer_ordres()

carnet.afficher_carnet()

carnet.creer_fixing("cloture")
