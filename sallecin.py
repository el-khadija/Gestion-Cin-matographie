from tkinter import StringVar, Tk, Event, messagebox, BooleanVar,ttk,END
from tkinter.ttk import Combobox, Label, Entry, Radiobutton, Button
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.messagebox import showinfo
import json


class SalleCine(object):
    def __init__(self, film: str, nbp: int, prix: float):
        self.film=film.title()
        self.nbp = nbp
        self.prix = prix
        self.nbp_v_normal = 0
        self.nbp_v_rd = 0

    def dispo(self):
        return self.nbp - (self.nbp_v_normal + self.nbp_v_rd)

    def vendre(self, nb, tr: bool):
        prix=0.0
        if self.dispo() < nb:
            raise Exception("nombre de place dispo insufisant")
        if tr:
            prix = self.prix * nb
            self.nbp_v_normal += nb
        else:
            prix = self.prix * nb * 0.8
            self.nbp_v_rd += nb
        return prix

    #def annuler(self, nb, tr: bool):
        #if tr:
            #self.nbp_v_normal -= nb
        #else:
            #self.nbp_v_rd -= nb

    def recette(self):
        return self.prix * (self.nbp_v_rd * 0.8 + self.nbp_v_normal)

    def taux(self):
        return round((self.nbp_v_normal + self.nbp_v_rd) / self.nbp, 2) * 100

    def raz(self):
        self.nbp_v_normal = 0
        self.nbp_v_rd = 0

num_séance=0
class Application(Tk):
    def __init__(self):
        super().__init__()
        self.films = self.nv_seance()
        self.current_film = None
        self.add_widgets()
        self.add_events()

    def add_widgets(self):
        self.lbl_fil = Label(self , text="Film")
        self.lbl_fil.grid(row=1 , column=1)

        self.cmb = Combobox(self , values=self.load_lst() )
        self.cmb.grid(row=1 , column=2)

        self.lbl_prix = Label(self, text="Prix")
        self.lbl_prix.grid(row=2, column=1)

        self.var_txt_prix = StringVar()
        self.var_txt_prix.set("")

        self.txt_prix = Entry(self , textvariable=self.var_txt_prix , state="disable")
        self.txt_prix.grid(row=2 , column=2)

        self.lbl_nbp = Label(self , text="Nombre de place")
        self.lbl_nbp.grid(row=3 , column=1)

        self.var_txt_nbp = StringVar()
        self.var_txt_nbp.set("")

        self.txt_nbp = Entry(self , textvariable=self.var_txt_nbp)
        self.txt_nbp.grid(row=3 , column=2)

        self.rd_tarif = BooleanVar()
        self.rd_tarif.set(True)

        self.rd_tarif_normal = Radiobutton(self, text="tarif normale", variable=self.rd_tarif, value=True)
        self.rd_tarif_normal.grid(row=4, column=2)

        self.rd_tarif_reduit = Radiobutton(self, text="tarif reduit", variable=self.rd_tarif, value=False)
        self.rd_tarif_reduit.grid(row=5, column=2)

        self.btn_calculer = Button(self, text="Calculer", command=self.calculer)
        self.btn_calculer.grid(row=2, column=3, padx=20, pady=20)

        self.btn_annuler = Button(self, text="Annuler", command=self.annuler)
        self.btn_annuler.grid(row=3, column=3, padx=20, pady=20)

        self.btn_valider = Button(self, text="Valider", command=self.valider)
        self.btn_valider.grid(row=4, column=3, padx=20, pady=20)

        self.tab = ttk.Treeview ( self, columns=("_film" , "_taux" , "_recette") , show="headings")
        self.tab.heading("_film" , text=" Film")
        self.tab.heading("_taux", text=" Taux_de_remplissage")
        self.tab.heading("_recette", text="Recette")
        self.tab.grid(row=6, column=4)

    def calculer(self):
        # try:
        #     if self.current_film: 'SalleCine' == None:
        #         raise Exception("Vous devez choisir un film.")
            
        # except Exception as err:
        #     # messagebox.showerror("Error", err)
        #     print(err)
        try:
            if self.current_film == None:
                raise Exception("Vous devez choisir un film.")
            nb=int(self.var_txt_nbp.get()) 
            prix_payer=self.current_film.vendre(nb,self.rd_tarif.get())  
            self.var_txt_prix.set(prix_payer)
            print(self.current_film.recette)
        except Exception as err:
            print(err) 

    def annuler(self):
        self.current_film.annuler(int(self.var_txt_nbp.get()), self.rd_tarif.get())

    def valider(self): #nchoufo les informations f triv you key:film
        self.tab.delete(*self.tab.get_children())
        for film in self.films.values():
            self.tab.insert('' , END , values=( film.film , film.taux() , film.recette()))


         
    def add_events(self):
        self.cmb.bind("<<ComboboxSelected>>", self.load_cmb)
        
    
    def load_cmb(self, event: Event):
        film = self.cmb.get()
        self.current_film: 'SalleCine' = self.films[film]

        self.var_txt_prix.set(self.current_film.prix)

        
    def nv_seance(self):
        dic = {}
        dic = {"CasaNegra": SalleCine('CasaNegra', 20, 100),\
                "qism 8": SalleCine('qism 8', 10, 150),\
                "casa del papel": SalleCine("casa del papel", 10, 200)}
        return dic

    def load_lst(self):
        lst = []
        for key in self.films.keys():
            lst.append(key)
        return lst
    def enregistrer(self):
        with open("séance_"+str(Application,num_séance).json) as f:
            for film in self.films.values:
                lst=[lst.append(film.film)]
                lst=[lst.append(film.film)]
                lst=[lst.append(film.film)]
        num_séance+=1

app=Application()
app.title("nv seance")
app.mainloop()

