import random

class Personnage:2
    def __init__(self, nom, vie):
        self.__nom = nom
        self.__vie = vie

    def attaquer(self, adversaire):
        degats = random.randint(5, 15)
        adversaire.__vie -= degats
        print(f"{self.__nom} attaque {adversaire.__nom} et inflige {degats} dégâts !")
        adversaire.verifierVie()

    def estVivant(self):
        return self.__vie > 0

    def verifierVie(self):
        if self.__vie <= 0:
            print(f"{self.__nom} est mort !")
        else:
            print(f"{self.__nom} a {self.__vie} PV restants.")

    def getNom(self):
        return self.__nom

    def getVie(self):
        return self.__vie


class Jeu:
    def __init__(self):
        self.niveau = None

    def choisirNiveau(self):
        print("\nChoisissez un niveau de difficulté :")
        print("1 - Facile (100 PV chacun)")
        print("2 - Normal (75 PV chacun)")
        print("3 - Difficile (50 PV chacun)")
        choix = input("Votre choix : ")
        
        if choix == "1":
            self.niveau = 100
        elif choix == "2":
            self.niveau = 75
        else:
            self.niveau = 50
        
        print(f"\nNiveau choisi : {self.niveau} PV pour chaque combattant.")

    def lancerJeu(self):
        self.choisirNiveau()
        
        joueur = Personnage("Mario", self.niveau)
        ennemi = Personnage("Bowser", self.niveau)

        print("\nLe combat commence !")

        while joueur.estVivant() and ennemi.estVivant():
            input("\nAppuyez sur Entrée pour attaquer !")
            joueur.attaquer(ennemi)

            if ennemi.estVivant():
                ennemi.attaquer(joueur)

        self.verifierGagnant(joueur, ennemi)

    def verifierGagnant(self, joueur, ennemi):
        if joueur.estVivant():
            print(f"\n{joueur.getNom()} a gagné le combat !")
        else:
            print(f"\n{ennemi.getNom()} a triomphé...")

jeu = Jeu()
jeu.lancerJeu()
