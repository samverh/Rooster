"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

Program loads in the data for the schedule.
"""

class vak:
    def __init__(self,name,hoorcolleges,werkcolleges,max_werkcolleges,practica,\
    max_practica,e_students):
        self.name = name
        self.hoorcolleges = hoorcolleges
        self.werkcolleges = werkcolleges
        self.practica = practica
        self.max_werkcolleges = max_werkcolleges
        self.max_practica = max_practica
        self.e_students = e_students

class hour:
    scheduled = False
    courses = []

class day:
    hours = [hour(),hour(),hour(), hour(),hour()]

class room_info:
    def __init__(self,name,capaciteit):
        self.room = name
        self.cap = capaciteit

    days = [day(),day(),day(),day(),day()]

vakken = []
vakken.append(vak("Advanced Heuristics",1,0,None,1,10,22))
vakken.append(vak("Algorithmen en Complexiteit",1,1,25,1,25,47))
vakken.append(vak("Analysemethoden en -technieken",1,0,None,0,None,60))
vakken.append(vak("Architectuur en computerorganisatie",2,0,None,0,None,19))
vakken.append(vak("Autonomous Agents 2",2,1,10,1,10,19))
vakken.append(vak("Bioinformatica",3,1,20,1,20,40))
vakken.append(vak("Calculus 2",1,1,40,0,None,90))
vakken.append(vak("Collectieve Intelligentie",3,1,20,1,20,65))
vakken.append(vak("Compilerbouw",2,1,40,1,40,70))
vakken.append(vak("Compilerbouw (practium)",0,0,None,1,15,35))
vakken.append(vak("Data Mining",2,1,10,1,10,30))
vakken.append(vak("Databases 2",1,1,40,0,None,69))
vakken.append(vak("Heuristieken 1",1,1,25,0,None,44))
vakken.append(vak("Heuristieken 2",1,1,20,0,None,30))
vakken.append(vak("Informatie- en organisatieontwerp",2,1,15,1,15,40))
vakken.append(vak("Interactie-ontwerp",2,0,None,0,None,31))
vakken.append(vak("Kansrekenen 2",2,0,None,0,None,70))
vakken.append(vak("Lineaire Algebra",2,0,None,0,None,50))
vakken.append(vak("Machine Learning",2,0,None,0,None,25))
vakken.append(vak("Moderne Databases",1,1,20,1,20,60))
vakken.append(vak("Netwerken en systeembeveiliging",0,0,None,1,20,50))
vakken.append(vak("Programmeren in Java 2",0,0,None,1,20,95))
vakken.append(vak("Project Genetic Algorithms",0,0,None,1,15,40))
vakken.append(vak("Project Numerical Recipes",0,0,None,1,15,40))
vakken.append(vak("Reflectie op de digitale cultuur",2,1,20,0,None,53))
vakken.append(vak("Software engineering",1,1,40,1,40,75))
vakken.append(vak("Technology for games",2,1,20,0,None,50))
vakken.append(vak("Webprogrammeren en databases",2,1,20,1,20,46))
vakken.append(vak("Zoeken, sturen en bewegen",0,0,None,1,15,45))

lokalen = []
lokalen.append(room_info("A1.04",41))
lokalen.append(room_info("A1.06",22))
lokalen.append(room_info("A1.08",20))
lokalen.append(room_info("A1.10",56))
lokalen.append(room_info("B0.201",48))
lokalen.append(room_info("C0.110",117))
lokalen.append(room_info("C1.112",60))
