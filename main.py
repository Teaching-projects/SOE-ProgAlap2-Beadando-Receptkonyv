from tkinter.ttk import *
import tkinter as tk
from tkinter.constants import *
from tkinter.font import *
from Receptkezelo import Receptkezelo
from DB_Manager import DB_Manager
from Naptar import Naptar
from datetime import date
from PIL import ImageTk, Image
import os


class SzakacskonyvGUI(tk.Tk):
    
    "Ez az osztály a receptkezelő program megjelenítéséért felelős."

    rK = Receptkezelo()
    dbM = DB_Manager()
    naptar = Naptar()
    _guiConfiguration = dict()

    def __init__(self ):
        super().__init__()
        self._guiConfiguration = {"s_w" : int(self.winfo_screenwidth()), 
                                 "s_h" : int(self.winfo_screenheight()),
                                 "page_w": int(self.winfo_screenwidth()*0.80),
                                 "page_h": int(self.winfo_screenheight()*0.63),
                                 "textb_w" : int(self.winfo_screenwidth()*0.5),
                                 "textb_h": int(self.winfo_screenheight()*0.5),
                                } 
        self.__setup_ui()


    def __setup_ui(self):

        "Ez a függvény hozza létre a naptár, a receptkezelő, valamint az exit gombot."

        self.title("Szakacskonyv")
        self.config(background="gray20")
        self.overrideredirect(True)
        self.geometry("{}x{}".format(self._guiConfiguration["s_w"],self._guiConfiguration["s_h"]))
        self.resizable(False,False)

        self.main_frame = tk.Frame(self, width=self._guiConfiguration["s_w"], height=self._guiConfiguration["s_h"], bg="lightblue",relief=tk.SUNKEN)

        self.menu_frame = tk.Frame(self.main_frame, width=150, bg="lightblue")
        
        self.page_frame = tk.LabelFrame(self.main_frame, relief=FLAT, bg="lightblue")

        self.button1 = tk.Button(self.menu_frame,text="NAPTAR",  relief=tk.RAISED, width= 20, height= 3, bg= "gray20", command= lambda: self.page("NAPTAR"),foreground="cyan")
        self.button3 = tk.Button(self.menu_frame,text="Receptkezelo",  relief=tk.RAISED, width= 20, height= 3, bg= "gray20", command= lambda: self.page("Receptkezelo"),foreground="cyan")
        self.buttonX = tk.Button(self.menu_frame,text="EXIT",  relief=tk.RAISED, width= 20, height= 3, bg= "gray20", command= self.destroy ,foreground="cyan")
        
        self.button1.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)
        self.button3.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)
        self.buttonX.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)
        self.menu_frame.pack(side=LEFT,fill=Y, pady=10, padx=10, expand=0)
        self.page_frame.pack(side=RIGHT, fill=BOTH, pady=10, padx=10,expand=1 )
        self.main_frame.pack(fill=tk.BOTH, pady=10, padx=10, expand=1)

        self.page("NAPTAR")


    def page(self,page):

        "Ez a függvény hozza létre a naptár felületet."

        for widget in self.page_frame.winfo_children():
            widget.destroy()
        parent = self.page_frame

        if page == "NAPTAR":
            self.events = list()
            self.page_frame.config(text=page)
            config = self.naptar.alap_setup()
            self.event = config["event"]
            for key in (config["event"]):
                self.events.append(key)


            def next_month(config):

                "Ez a függvény teszi lehetőve, hogy a következő hónapra lapozhassunk."

                month = config["date"][1] + 1
                if month > 12:
                    month = 1
                    year = config["date"][0] + 1
                else:
                    year = config["date"][0]
                config = self.naptar.date_setup(year,month)
                spawn_naptar(config)


            def prev_month(config):

                "Ez a függvény teszi lehetőve, hogy az előző hónapra lapozhassunk."

                month = config["date"][1] - 1
                if month < 1:
                    month = 12
                    year = config["date"][0] - 1
                else:
                    year = config["date"][0]
                config = self.naptar.date_setup(year,month)
                spawn_naptar(config)
            

            def button_press(text):

                for widget in self.layer["Group0Buttons"]:
                    widget.destroy()
                self.b_datum = (("{}-{}-{}").format(config["date"][0],config["date"][1],text))
                self.layer["Labels"][-1].config(text = self.b_datum, bg="gray20",foreground="magenta")
                self.layer["Group0Buttons"].append(tk.Button(self.layer["Group"][2],text="Uj Event",bg="gray20", foreground="magenta", command= lambda: event_letrehozasa(self.b_datum)))
                self.layer["Group0Buttons"][-1].pack(side=TOP,fill=X)
                if self.b_datum in self.event:
                    for i in range(len(self.event[self.b_datum])):
                        self.layer["Group0Buttons"].append(tk.Button(self.layer["Group"][2],text=self.event[self.b_datum][i],bg="gray", foreground="cyan"))
                        self.layer["Group0Buttons"][-1].config(command= lambda text=self.event[self.b_datum][i]: recept_nyitas(text))
                        self.layer["Group0Buttons"][-1].pack(side=TOP,fill=X, pady=2)
                
            def recept_nyitas(nev):

                "Ez a függvény lehetővé teszi, hogy az egyik napra rákattintva megjelenik a dátum, valamint az ételek neve, amit főzni szeretnék aznap. Az étel nevére rákattintva pedig megjelenik az étel képe, hozzávalói, valamint az elkészítésének a menete."

                recept = self.rK.loadRecept(nev)
                self.recept_gui = tk.Toplevel()
                self.recept_gui.title(recept["Title"])
                path = ("./Kepek/{}").format(recept["Kep"])
                self.r_image = Image.open(path,mode='r')
                self.r_image = self.r_image.resize((1200, 800))
                self.r_img = ImageTk.PhotoImage(self.r_image)
                self.background_label = Label(self.recept_gui,image=self.r_img)
                self.background_label.pack()
                hozzavalotext = tk.Label(self.recept_gui, text="Hozzavalok:",font=("Arial",10),)
                hozzavalopage = tk.Listbox(self.recept_gui, width=25, font=("Arial",10), bg="white", foreground="black")
                hozzavalopage.place(x=10, y=110)
                hozzavalotext.place(x=10, y=30)
                for i in recept["Hozzavalok"]:
                    ujlistaelem = ("{} {} {}").format(recept["Hozzavalok"][i][0],recept["Hozzavalok"][i][1],i)
                    hozzavalopage.insert(END,ujlistaelem)
                elkeszitesetext = tk.Label(self.recept_gui, text="Elkeszitese:",font=("Arial",10))
                elkeszitesetext.place(x=300, y=30)
                r_elkeszitese = tk.Text(self.recept_gui, state=NORMAL, padx= 10, pady= 10, wrap= WORD, font=("Helvetica",12,BOLD), height= 10)
                r_elkeszitese.place(x=300, y=90)
                r_elkeszitese.insert(END,recept["Elkeszitese"])
                r_elkeszitese.config(state=DISABLED)
                
                
            def event_letrehozasa(datum):

                "Ez a függvény teszi lehetővé, hogy be tudjam írni a naptárba azoknak az ételeknek a nevét, amelyeket el szeretnék készíteni az adott napon."

                n_event = self.naptar._naptar_gui["event"]

                self.event_manager_gui = tk.Toplevel()
                self.event_manager_gui.title("Event Manager")
                main = Label(self.event_manager_gui)
                main.pack()
                frame1 = tk.Frame(main)
                frame1.pack(side=TOP, padx=10, ipadx=10, ipady=10)
                frame2 = tk.Frame(main)
                frame2.pack(side=TOP, ipadx=10, ipady=10)
                frame3 = tk.Frame(main, width=100)
                frame3.pack(side=BOTTOM, ipadx=10, ipady=10)
            
                label1 = tk.Label(frame1,text=datum, bg="gray20", foreground="cyan",  width= 15, height=2)
                label1.grid(column=0,row=0, pady=10, padx=3)

                self.e_recept_list = tk.Listbox(frame2)
                self.e_recept_list.pack(side=LEFT)
                add_button = tk.Button(frame2, text= " + ", command= addtolist)
                add_button.pack(side=LEFT, fill=Y, pady=10, padx=3)
                self.event_list = tk.Listbox(frame2)
                self.event_list.pack(side=LEFT)
                del_button = tk.Button(frame2, text= " - ", command= lambda: self.event_list.delete(ANCHOR))
                del_button.pack(side=LEFT, fill=Y, pady=10, padx=3)

                save_button = tk.Button(frame3, width=20, text= "SAVE", command= lambda: save_event(datum))
                save_button.pack(side=BOTTOM, padx=10, fill=X)

                if datum in self.event:
                    for i in range(len(n_event[datum])):
                        l_in = str(n_event[datum][i])
                        self.event_list.insert(END,l_in)
                receptek = (self.rK._receptlist)
                for keys in receptek:
                    self.e_recept_list.insert(END,keys)

            def addtolist():

                item=str((self.e_recept_list.get(self.e_recept_list.curselection())))
                self.event_list.insert(END,item)

            def save_event(datum):

                events = (self.event_list.get(0,END))
                self.naptar.event(datum, events)
                self.event_manager_gui.destroy()
                self.page("NAPTAR") 

            def spawn_naptar(config):

                for widget in self.page_frame.winfo_children():
                    widget.destroy()
                self.layer = {"Parent" : self.page_frame,
                         "Labels" : list(),
                         "Buttons" : list(),
                         "command" : list(),
                         "Group" : list(),
                         "Group0Buttons" : list()
                         }

                self.layer["Group"].append(tk.Frame(self.layer["Parent"], height=12, padx=50, pady=20, bg= "lightblue"))
                self.layer["Group"].append(tk.Frame(self.layer["Parent"], height=200, padx=50, pady=20, bg= "lightblue"))
                self.layer["Group"].append(tk.Frame(self.layer["Parent"], height=700, width=300, bg= "lightblue"))
                self.layer["Group"][0].pack(side = TOP)
                self.layer["Group"][1].pack(side = TOP)
                self.layer["Group"][2].place(x=10, y=100)
                
                self.layer["Buttons"].append(tk.Button(self.layer["Group"][0], text= " < ", bg="gray20", foreground="cyan", command= lambda: prev_month(config)))
                self.layer["Labels"].append(tk.Label(self.layer["Group"][0], text=config["fejlec"], bg="gray20", font=("Arial",20,BOLD), width=20, foreground="cyan"))
                self.layer["Buttons"].append(tk.Button(self.layer["Group"][0], text= " > ", bg="gray20", foreground="cyan", command= lambda: next_month(config)))
                self.layer["Buttons"][-2].pack(side=LEFT, fill=Y, padx=2)
                self.layer["Labels"][-1].pack(side=LEFT)
                self.layer["Buttons"][-1].pack(side=LEFT, fill=Y, padx =2)  

                grid_x = 0
                grid_y = 0
                for i in range(len(config["napok"])):
                    self.layer["Labels"].append(tk.Label(self.layer["Group"][1], text=config["napok"][i], bg="gray20", foreground="cyan", relief=tk.RAISED, width= 15, height=2))
                    self.layer["Labels"][-1].grid(column= grid_x, row= grid_y, padx=2, pady=2)
                    grid_x +=1

                grid_x = 0
                grid_y = 1
                self.image = Image.open("./Kepek/event.png",mode='r').resize((20,20))
                self.image = ImageTk.PhotoImage(self.image)
                for i in range(len(config["naptar"])):
                    self.layer["Buttons"].append(tk.Button(self.layer["Group"][1], text=config["naptar"][i], height=5 , width=15, bg="gray20", foreground="cyan", relief=RAISED, anchor=tk.NW, font=("Arial",10,BOLD)))
                    event_day =(("{}-{}-{}").format(config["date"][0],config["date"][1],config["naptar"][i]))
                    if config["naptar"][i] == " ":
                        self.layer["Buttons"][-1].config(state= DISABLED, bg= "Lightblue",relief=FLAT)
                    else:
                        self.layer["Buttons"][-1].config(command= lambda text=config["naptar"][i]: button_press(text))
                        

                    if int(date.today().strftime("%Y")) == config["date"][0] and int(date.today().strftime("%m")) == config["date"][1] and config["naptar"][i] == int(config["today"]):
                        self.layer["Buttons"][-1].configure(foreground="magenta" )


                    if event_day in self.events:
                        self.layer["Buttons"][-1].configure(image=self.image, compound="right", height=84, width=120)
                        

                    if grid_x >= 7: 
                        grid_y += 1
                        grid_x = 0
                    self.layer["Buttons"][-1].grid(column= grid_x, row= grid_y, padx=2, pady=2)
                    grid_x +=1

                
                self.layer["Labels"].append(tk.Label(self.layer["Group"][2], font=("Arial",20,BOLD), foreground="cyan", bg="lightblue"))
                self.layer["Labels"][-1].pack(side=TOP, fill=X)
                                

            spawn_naptar(config)


        elif page == "Receptkezelo":
            receptek = (self.rK._receptlist)
            self.page_frame.config(text=page)
            self.ujrecept_gomb = tk.Button(parent,text="UJ RECEPT", command= self.recept_letrehozasa)
            self.ujrecept_gomb.place(x=10,y=50)

            self.recept_lista = tk.Listbox(parent)
            self.recept_lista.place(x=300, y=20)
            for keys in receptek:
                self.recept_lista.insert(END,keys)
            self.recept_lista.bind("<<ListboxSelect>>", self.recept_kivalaszt)

            self.receptpage = tk.LabelFrame(parent, height=self._guiConfiguration["page_h"], width=self._guiConfiguration["page_w"], font=("Arial",12,BOLD),bg="lightblue",relief=RAISED)
            self.receptpage.place(x=10, y=280)


    def recept_kivalaszt(self,evt):

        "Ez a függvény teszi lehetővé, hogy a megadott receptek közül ki lehessen választani egyet. Ezután láthatóvá válik a kiválasztott recept képe, hozzávalói, valamint az elkészítésének menete."


        for widget in self.receptpage.winfo_children():
            widget.destroy()
        parent = self.receptpage
        value=str((self.recept_lista.get(self.recept_lista.curselection())))
        recept = self.rK.loadRecept(value)

        path = ("./Kepek/{}").format(recept["Kep"])
        self.image = Image.open(path,mode='r')
        self.image = self.image.resize((200, 200))
        self.img = ImageTk.PhotoImage(self.image)
        self.my_img = Button(self.page_frame,image = self.img, text = "Almas Kevert", command= lambda: self.nagykep(path))
        self.my_img.place(x=500, y=50, height=210, width=210)
        
        self.receptpage.config(text=recept["Title"])
        hozzavalotext = tk.Label(parent, text="Hozzavalok:",font=("Arial",10),bg = "lightblue")
        hozzavalopage = tk.Listbox(parent, width=25, font=("Arial",10),selectmode=NONE, bg="white", foreground="black")
        hozzavalopage.place(x=10, y=110, height=self._guiConfiguration["textb_h"])
        hozzavalotext.place(x=10, y=30)
        for i in recept["Hozzavalok"]:
                ujlistaelem = ("{} {} {}").format(recept["Hozzavalok"][i][0],recept["Hozzavalok"][i][1],i)
                hozzavalopage.insert(END,ujlistaelem)
        hozzavalopage.config(state=DISABLED)
        elkeszitesetext = tk.Label(parent, text="Elkeszitese:",font=("Arial",10), bg= "lightblue")
        elkeszitesetext.place(x=300, y=30)
        elkeszitese = tk.Text(parent, state=NORMAL, padx= 10, pady= 10, wrap= WORD, font=("Helvetica",12,BOLD))
        elkeszitese.place(x=300, y=90, width=self._guiConfiguration["textb_w"], height=self._guiConfiguration["textb_h"])
        elkeszitese.insert(END,recept["Elkeszitese"])
        elkeszitese.config(state=DISABLED)


    def recept_letrehozasa(self):

        "Ez a függvény hozza létre a receptkezelőben lévő új recept gombot."
        "Meg lehet adni az étel nevét, a hozzávalóit, valamint az elkészítését."
        "Az előre megadott hozzávalók részben szereplő hozzávalók közül lehet kiválasztani a recept elkészítéséhez szükséges alapanyagokat, ki lehet választani, hogy miből, mennyi szükséges. A Kesz vagyok, Mentes! gombbal lehet elmenteni az új recepteket."

        self.kepnev=str()

        def kep_kivalaszt(event):
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                self.kepnev =event.widget.get(index)

        for widget in self.receptpage.winfo_children():
            widget.destroy()
        self.recept_lista.destroy()
        parent = self.receptpage
        self.receptpage.config(text="")
        kep_lista = tk.Listbox(self.page_frame)
        kep_lista.place(x=300, y=20)
        k_list = os.listdir("./Kepek")
        for filenev in k_list:
            kep_lista.insert(END,filenev)
        hozzavalotext = tk.Label(parent, text="Hozzavalok:",font=("Arial",10), bg= "lightblue")
        receptnev_text = tk.Label(parent, text="Recept nev: ",font=("Arial",10), bg= "lightblue")
        self.recept_nev = tk.Entry(parent,font=("Arial",10))
        self.hozzavalopage = tk.Listbox(parent, width=25, font=("Arial",10),selectmode=NONE, bg="white", foreground="black")
        self.hozzavalopage.place(x=10, y=110, height=self._guiConfiguration["textb_h"])
        hozzavalotext.place(x=10, y=30)
        receptnev_text.place(x=10, y=10)
        self.recept_nev.place(x=100, y=10)
        elkeszitesetext = tk.Label(parent, text="Elkeszitese:",font=("Arial",10), bg= "lightblue")
        elkeszitesetext.place(x=300, y=30)
        self.elkeszitese = tk.Text(parent, padx= 10, pady= 10, wrap= WORD, font=("Helvetica",12,BOLD))
        self.elkeszitese.place(x=300, y=110, width=self._guiConfiguration["textb_w"], height=self._guiConfiguration["textb_h"])
        addhozzavalo_button = tk.Button(parent, width=10, text="+", bg="gray", command= lambda: self.hozzavaloszerkeszto("uj"))
        delhozzavalo_button = tk.Button(parent, width=10, text="-", bg="gray")
        addhozzavalo_button.place(x=10, y=80)
        delhozzavalo_button.place(x=105, y=80)
        mentes_button = tk.Button(parent, width=60, text="Kesz vagyok, Mentes!", bg="gray", command= self.create_save)
        mentes_button.place(x= 500, y=20)

        kep_lista.bind("<<ListboxSelect>>", kep_kivalaszt)


    def create_save(self):

        recept = {"Mappa" : str("Receptek"),
                  "Title" : str(self.recept_nev.get()),
                  "Fname" : str(self.recept_nev.get().replace(" ","_")),
                  "Hozzavalok" : dict(),
                  "Elkeszitese" : self.elkeszitese.get("1.0","end-1c"),
                  "cimke" : list(),
                  "Kep" : self.kepnev,
                  }

        for i in range(self.hozzavalopage.index(END)):
                process = self.hozzavalopage.get(i).split(" ")
                process = {process[2] : [process[0],process[1]]}
                recept["Hozzavalok"].update(process)

        self.rK.ujrecept(recept)
        self.dbM.db_update("hozzavalok",self.hozzavalok)

    def nagykep(self,path):
        self.nagykep = tk.Toplevel()
        self.img = ImageTk.PhotoImage(Image.open(path))
        self.background_label = Label(self.nagykep,image=self.img).pack()

    def hozzavaloszerkeszto(self,mode):

        hozzavaloszerkeszto_ablak = tk.Toplevel()
        hozzavaloszerkeszto_ablak.title("Hozzavaloszerkeszto")
        self.hozzavalok = self.dbM._hozzavalok
        self.mertekegysegek = self.dbM._mertekegysegek
        parent = hozzavaloszerkeszto_ablak

        def hozzavalolista_refresh():

            hozzavalo_lista.delete(0,END)
            for keys in self.hozzavalok:
                hozzavalo_lista.insert(END,keys)
        
        def callback1(event):
            mertekegyseg_lista.delete(0,END)
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                data_h = event.widget.get(index)
                listabevitel_hozzavalo.config(state= NORMAL)
                listabevitel_hozzavalo.delete(0,"end")
                listabevitel_hozzavalo.insert(INSERT,data_h)
                listabevitel_hozzavalo.config(state= DISABLED)
                melista = self.mertekegysegek[self.hozzavalok[data_h]]
                for i in melista:
                    mertekegyseg_lista.insert("end", i)
        
        def callback2(event):
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                data_me = event.widget.get(index)
                listabevitel_mertekegyseg.config(state= NORMAL)
                listabevitel_mertekegyseg.delete(0,"end")
                listabevitel_mertekegyseg.insert(INSERT,data_me)
                listabevitel_mertekegyseg.config(state= DISABLED)

        def addToList():
            mennyiseg = listabevitel_mennyiseg.get()
            mertekegyseg = listabevitel_mertekegyseg.get()
            alapanyag = listabevitel_hozzavalo.get()
            listaelem = ("{} {} {}").format(mennyiseg,mertekegyseg,alapanyag)
            self.hozzavalopage.insert(END,listaelem)

        def db_hozzavalo():
            self.hozzavalok[hozzavalo_label.get()] =kategoria.get()
            hozzavalo_lista.delete(0,"end")
            hozzavalo = list(self.hozzavalok.keys())
            for i in range(len(hozzavalo)):
                hozzavalo_lista.insert(i+1, hozzavalo[i])
            hozzavalo_label.delete(0,"end")

        hozzavalo_lista = tk.Listbox(parent)
        addhhozzavalo_gomb = tk.Button(parent,text="+", command= db_hozzavalo)
        mertekegyseg_lista= tk.Listbox(parent)
        addmertekegyseg_gomb = tk.Button(parent,text="+", height=10, command= "")
        hozzavalo_label = tk.Entry(parent, width=20)
        hozzavalo_label.insert(0,"uj hozzavalo nev:")
        kategoria = tk.StringVar(parent)
        OPTIONS = list(self.mertekegysegek.keys())
        kategoria.set(OPTIONS[0]) 
        dropdown = tk.OptionMenu(parent, kategoria, *OPTIONS)
        listabevitel_mennyiseg = tk.Entry(parent, state=NORMAL, width=5)
        listabevitel_hozzavalo = tk.Entry(parent, state=DISABLED)
        listabevitel_mertekegyseg = tk.Entry(parent, state=DISABLED)
        addtolist= tk.Button(parent,text="+", command= addToList)
        
        dropdown.grid(columnspan=1)
        hozzavalo_label.grid(column=1,row=0,pady=5)
        hozzavalo_lista.grid(column=1, row=1)
        addhhozzavalo_gomb.grid(column=2,row=0)
        mertekegyseg_lista.grid(column=4, row=1)
        addmertekegyseg_gomb.grid(column=5,row=1)
        listabevitel_mennyiseg.grid(column=0, row=2, pady=20, padx=10)
        listabevitel_mertekegyseg.grid(column=1, row=2)
        listabevitel_hozzavalo.grid(column=4, row=2)
        addtolist.grid(column=5, row=2)

        hozzavalolista_refresh()

        hozzavalo_lista.bind("<<ListboxSelect>>", callback1)
        mertekegyseg_lista.bind("<<ListboxSelect>>", callback2)


        
        if mode == "uj":
            pass
            
        hozzavaloszerkeszto_ablak.mainloop()






if __name__ == "__main__":
  SzakacskonyvGUI().mainloop()