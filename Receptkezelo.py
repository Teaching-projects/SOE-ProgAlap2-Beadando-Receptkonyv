import json,os

class Receptkezelo:
    _receptlist = dict()

    def __init__(self):
        source = os.listdir("./Receptek")
        for i in range(len(source)):
            receptnev = {(source[i].replace("_"," ")) : str(source[i])}
            self._receptlist.update(receptnev) 

        with open("hozzavalok_db.json") as load:
            self._hozzavalok = json.load(load)

        with open("mertekegysegek_db.json") as load:
            self._mertekegysegek = json.load(load)


    def loadRecept(self,nev):
        recept= dict()
        filename= ("./Receptek/{}").format(str(self._receptlist[nev]))
        with open(filename) as load:
            recept = json.load(load)
        return recept

    def ujrecept(self,recept):
        self.recept = recept
        filename = ("./{}/{}").format(self.recept["Mappa"],self.recept["Fname"])
        with open(filename, 'w') as save:
            json.dump(self.recept, save)
        
        

        

#if __name__ == "__main__":
    #nev = "Zoldbabos Rizs"
    #akcio = Receptkezelo()
    #print(akcio.loadRecept(nev))

    #start = Receptkezelo()
    #print(start._receptlist)