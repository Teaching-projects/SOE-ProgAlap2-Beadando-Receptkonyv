from datetime import date
import calendar,json
from tkinter.constants import NONE


class Naptar:
    _naptar_gui = dict()
    
    

    def __init__(self):
        self._naptar_gui = {"parent" : str(),
                   "honapok" : ["Januar", "Februar","Marcius","Aprilis","Majus","Junius","Julius","Augusztus","Szeptember","Oktober","November","December"],
                   "napok" : ["Hetfo","Kedd","Szerda","Csutortok","Pentek","Szombat", "Vasarnap"],
                   "naptar" : list(),
                   "datum" : list(),
                   "fejlec" : str(),
                   "today" : date.today().strftime("%d"),
                   "event" : dict()
                    }
        with open("event_db.json") as load:
            self._naptar_gui["event"] = json.load(load)
        


    def alap_setup(self):
        self._naptar_gui["naptar"].clear()
        today = date.today()
        year = int(today.strftime("%Y"))
        month = int(today.strftime("%m"))
        self._naptar_gui["date"] = [year,month]
        honap_kezdo_nap = date.today().replace(year=year, month=month, day=1).weekday()
        honap_utolso_nap = calendar.monthrange(year,month)
        nap = 0
        for i in range(42):
            if i < honap_kezdo_nap or nap >= honap_utolso_nap[1]:
                self._naptar_gui["naptar"].append(" ")
            else:
                nap +=1
                self._naptar_gui["naptar"].append(nap)
        self._naptar_gui["fejlec"] = ("{},   {}").format(year,self._naptar_gui["honapok"][month-1])
        return self._naptar_gui


    def date_setup(self,year,month):
        self._naptar_gui["naptar"].clear()
        self._naptar_gui["date"] = [year,month]
        honap_kezdo_nap = date.today().replace(year=year, month=month, day=1).weekday()
        honap_utolso_nap = calendar.monthrange(year,month)
        nap = 0
        for i in range(42):
            if i < honap_kezdo_nap or nap >= honap_utolso_nap[1]:
                self._naptar_gui["naptar"].append(" ")
            else:
                nap +=1
                self._naptar_gui["naptar"].append(nap)
        self._naptar_gui["fejlec"] = ("{},   {}").format(year,self._naptar_gui["honapok"][month-1])
        return self._naptar_gui

    def event(self,date,recept):
        with open("event_db.json","r") as file:
               self._naptar_gui["event"]=json.load(file)

        if recept == "delete":
            with open("event_db.json","w") as file:
               self._naptar_gui["event"].pop(date,NONE)
               json.dump(self._naptar_gui["event"], file)

        else:   
            event = {date : recept}
            with open("event_db.json","r+") as file:
                self._naptar_gui["event"].update(event)
                file.seek(0)
                json.dump(self._naptar_gui["event"], file)
            






#naptar = Naptar()

#print(naptar.date_setup(2011,10))