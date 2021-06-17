import json,os

class DB_Manager:
    _hozzavalok = dict()
    _mertekegysegek = dict()

    def __init__(self):
        with open("hozzavalok_db.json") as load:
            self._hozzavalok = json.load(load)

        with open("mertekegysegek_db.json") as load:
            self._mertekegysegek = json.load(load)

    def db_update(self,db_nev,db):
        if db_nev == "hozzavalok":
            filename = "hozzavalok_db.json"
            with open(filename, 'w') as save:
                json.dump(db, save)
        print("OK")
