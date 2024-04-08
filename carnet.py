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
            self.achats.append(ordre)
            self.achats.sort(key=lambda x: -x.prix if x.prix else float('-inf'))  # on trie par prix décroissant
        elif ordre.type_ordre.lower() == "vente":
            self.ventes.append(ordre)
            self.ventes.sort(key=lambda x: x.prix if x.prix else float('inf'))  # on trie par prix croissant

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
