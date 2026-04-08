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
    encode = None
    def processus(self,donne):
        """
        Dans la couche presentation recuperer les donnees de la couche app grace au return de la couche app
        et encode les message en base64
        :param donne:
        :return:
        """
        Presentation.encode = base64.b64encode(donne).decode()
        return self.couche.processus(Presentation.encode)

class SessionCouche(Osienc):
    session_et =[]
    def processus(self,donne):
        """
         Dans la couche session recuperer les donnees de la couche presentation grace au return de la couche app
        et ajoute les id de la session pour atablir la connexion

                """
        id_session = "denisnsa"
        SessionCouche.session_et.append(id_session)
        SessionCouche.session_et.append(donne)
        return self.couche.processus(SessionCouche.session_et)

class Transport(Osienc):
    """
     Dans la couche presentation recuperer les donnees de la couche session grace au return de la couche app
    et ajoute les ports
            """
    segment = {}
    def __init__(self,port_dst,couche=None):
        super().__init__(couche)
        self.port_dst = port_dst

    def processus(self,donne):
        port_src = random.randint(49152,65535)
        port =f'[{port_src} - {self.port_dst}]'
        Transport.segment["header"] = port
        Transport.segment["body"] = donne
        return self.couche.processus(Transport.segment)

class Reseau(Osienc):
    """
    Dans la couche presentation recuperer les donnees de la couche transport grace au return de la couche app
    et qjoute les ip
            """
    paquet = {}
    def __init__(self,ip_src,ip_dst,couche=None):
        super().__init__(self,couche)
        self.ip_src = ip_src
        self.ip_dst = ip_dst

    def processus(self,donne):
        tete =f'[{self.ip_src} - {self.ip_dst}]'
        Reseau.paquet["header"] = tete
        Reseau.paquet["body"] = donne
        return self.couche.processus(Reseau.paquet)

class Liaison(Osienc):
    """
            Dans la couche presentation recuperer les donnees de la couche reseau grace au return de la couche app
            et encode les message en base64
            """
    Trames = {}
    def __init__(self,mac_src,mac_dst,couche=None):
        super().__init__(couche)
        self.mac_dst = mac_dst
        self.mac_src = mac_src

    def processus(self,donne):
        en_tete =f'[{self.mac_src} - {self.mac_dst}]'
        pied ="[CRC_OK]"
        Liaison.Trames["header"] = en_tete
        Liaison.Trames["body"] = donne
        Liaison.Trames["pied"] = pied
        return self.couche.processus(Liaison.Trames)

class Physique(Osienc):
    """
    La classe physique herrite des methodes de la classe mere Osienc
    on utilise le parametre donne pour recuperer les trames et l'en encode en binaire
    """
    bite = None
    def processus(self,donne):
        bite = ''.join(format(ord(data), '08b') for data in donne)
        return bite
