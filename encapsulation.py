import random
import base64


class Osienc:
    """
    c'est la classe principale genre une classe mere(abstrait) avec comme argument couche qui permet de
    passe d'une couche a une autre , le parametre couche va enregistrer l'objet de la classe qui le precede
    lorsqu'on l'appel
    dans le processus on verifie si la couche existe on lui passe l'information
    """
    def __init__(self,couche=None):
        self.couche = couche

    def processus(self,donne):
        if self.couche:
            return self.couche.processus(donne)
        return donne

class Application(Osienc):
    """
    Dans la couche application recuperer le message de l'expediteur et ajoute une en tete et herite de donne
    de la classe mere
    """
    def processus(self,donne):
        tete ="[L7: HTTP_GET]"
        message =f"[{tete} | \n {donne}] ]"
        return self.couche.processus(message)

class Presentation(Osienc):
    def processus(self,donne):
        """
        Dans la couche presentation recuperer les donnees de la couche app grace au return de la couche app
        et encode les message en base64
        :param donne:
        :return:
        """
        encode = base64.b64encode(donne).decode()
        return self.couche.processus(encode)

class SessionCouche(Osienc):
    def processus(self,donne):
        """
         Dans la couche session recuperer les donnees de la couche presentation grace au return de la couche app
        et ajoute les id de la session pour atablir la connexion

                """
        id_session = "denisnsa"
        ses =f"[{id_session} | \n {donne}]"
        return self.couche.processus(ses)

class Transport(Osienc):
    """
     Dans la couche presentation recuperer les donnees de la couche session grace au return de la couche app
    et ajoute les ports
            """
    def __init__(self,port_dst,couche=None):
        super().__init__(couche)
        self.port_dst = port_dst

    def processus(self,donne):
        port_src = random.randint(49152,65535)
        port =f'[{port_src} - {self.port_dst}]'
        proto =f'[{port} | \n {donne}]'
        return self.couche.processus(proto)

class Reseau(Osienc):
    """
    Dans la couche presentation recuperer les donnees de la couche transport grace au return de la couche app
    et qjoute les ip
            """
    def __init__(self,ip_src,ip_dst,couche=None):
        super().__init__(self,couche)
        self.ip_src = ip_src
        self.ip_dst = ip_dst

    def processus(self,donne):
        tete =f'[{self.ip_src} - {self.ip_dst}]'
        paquet = f'[{tete} |\n {donne}]'
        return self.couche.processus(paquet)

class Liaison(Osienc):
    """
            Dans la couche presentation recuperer les donnees de la couche reseau grace au return de la couche app
            et encode les message en base64
            """
    def __init__(self,mac_src,mac_dst,couche=None):
        super().__init__(couche)
        self.mac_dst = mac_dst
        self.mac_src = mac_src

    def processus(self,donne):
        en_tete =f'[{self.mac_src} - {self.mac_dst}]'
        pied ="[CRC_OK]"
        trames = f"| {en_tete} | \n{donne} |\n {pied} |"
        return self.couche.processus(trames)

class Physique(Osienc):
    """
    La classe physique herrite des methodes de la classe mere Osienc
    on utilise le parametre donne pour recuperer les trames et l'en encode en binaire
    """
    def processus(self,donne):
        bite = ''.join(format(ord(data), '08b') for data in donne)
        return bite
