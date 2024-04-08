TICK_SIZE = 0,01 #on rajoute la notion de tick
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
            # on recherche les ordre de vente qui ont un prix supérieur ou égal au prix de l'ordre d'achat'
            for vente in self.ventes:
                if vente.prix >= ordre.prix:
                    quantite_exec = min(ordre.quantite, vente.quantite)
                    print(f"L'ordre d'achat de {ordre.quantite} au prix de {ordre.prix} a été exécuté "
                          f"avec {quantite_exec} du côté vente au prix de {vente.prix}.")
                    vente.quantite -= quantite_exec
                    ordre.quantite -= quantite_exec
                    if vente.quantite == 0:
                        self.ventes.remove(vente)
                    if ordre.quantite == 0:
                        return  # ordre d'achat excecuté
            # Si reste  des quantités non exécutées on ajoute l'ordre d'achat restant
            if ordre.quantite > 0:
                self.achats.append(ordre)
                self.achats.sort(key=lambda x: x.prix)  # Tri par prix croissant
        elif ordre.type_ordre.lower() == "vente":
            #on recherche les ordre d'achat qui ont un prix supérieur ou égal au prix de l'ordre de vente'
            for achat in self.achats:
                if achat.prix >= ordre.prix:
                    quantite_exec = min(ordre.quantite, achat.quantite)
                    print(f"L'ordre de vente de {ordre.quantite} au prix de {ordre.prix} a été exécuté "
                          f"avec {quantite_exec} du côté achat au prix de {achat.prix}.")
                    achat.quantite -= quantite_exec
                    ordre.quantite -= quantite_exec
                    if achat.quantite == 0:
                        self.achats.remove(achat)
                    if ordre.quantite == 0:
                        return  # ordre de vente exécuté
            # Si reste quantités non exécutées, ajouter l'ordre de vente restant
            if ordre.quantite > 0:
                self.ventes.append(ordre)
                self.ventes.sort(key=lambda x: x.prix, reverse=True)  # Tri par prix décroissant


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

#fonction permettant d'aligner le prix sur le tick
def aligner_tick(prix):
    return round(prix/TICK_SIZE)*TICK_SIZE
    
def creer_carnet_predefini():
    carnet = CarnetOrdres()
    # Ajout de 10 ordres d'achat et de vente prédéfinis
    for i in range(1, 11):
        carnet.ajouter_ordre(Ordre("Achat", i * 10, 100 + i))  
        carnet.ajouter_ordre(Ordre("Vente", i * 10, 110 - i)) 
    return carnet

#fonction permettant d'éxécuter l'ordre de l'utilisateur 
def saisir_nouvel_ordre():
    type_ordre = input("Entrez le type d'ordre (Achat/Vente) : ").capitalize()
    quantite = int(input("Entrez la quantité : "))
    #on va demander à l'utilisateru s'il souhaite vendre au prix de marché
    prix_de_marche = input("Voulez-vous réaliser votre ordre au prix de marché ? (Oui/Non) : ").lower()
    
    if prix_de_marche == "oui":
        prix = None  # Prix de marché
    else:
        prix = float(input("Entrez le prix : "))
    
    return Ordre(type_ordre, quantite, prix)
# Création du carnet d'ordres prédéfini
carnet = creer_carnet_predefini()

# Affichage du carnet d'ordres
carnet.afficher_carnet()

# on demande à l'utilisateur s'il souhaite effectuer un ordre 
while True:
    choix = input("Voulez-vous saisir un nouvel ordre ? (Oui/Non) : ").lower()
    if choix == "oui":
        nouvel_ordre = saisir_nouvel_ordre()
        carnet.ajouter_ordre(nouvel_ordre)
    elif choix == "non":
        break
    else:
        print("Veuillez répondre par 'Oui' ou 'Non'.")


carnet.afficher_carnet()
