import tkinter as tk
from random import choice
import winsound
import ctypes

class Logic:
    def __init__(self):
        self.data = {
            "HISTOIRE": {1: ("Qui a découvert l'Amérique ?", "CHRISTOPHE COLOMB")},
            "INFORMATIQUE": {
                1: ("Père de l'informatique ?", "ALAN TURING"),
                2: ("Premier ordinateur ?", "ENIAC")
            },
            "PHILOSOPHIE": {1: ("Qu'a dit René Descartes ?", "JE PENSE DONC JE SUIS")},
            "ACTUALITE": {1: ("Le président de Madagascar ?", "ANDRY RAJOELINA")},
            "GEOGRAPHIE": {1: ("Capitale de Madagascar ?", "ANTANANARIVO")}
        }
        self.themes = list(self.data.keys())
        self.nouvelle_question()

    def nouvelle_question(self):
        self.theme = choice(self.themes)
        id_q = choice(list(self.data[self.theme].keys()))
        self.question, self.reponse = self.data[self.theme][id_q]
        self.reponse = self.reponse.upper()
        self.affichage = [c if c in " ,/!?'" else "_" for c in self.reponse]

class InterfaceDAccueil1:
    def __init__(self, root):
        self.root = root
        self.root.title("HELP ME!")
        self.root.minsize(800, 600)
        
        self.game = Logic()
        self.mode_nuit = False
        self.volume_audio = 50
        self.difficulte_actuelle = "Normal"
        self.nb_chances = 5
        self.etats_questions = [1, 0, 0, 0, 0, 0, 0] 

        self.colors_light = {
            "bg_main": "#4DA6FF", "container": "#424242", "card": "#FFF9C4",
            "text": "black", "search": "#72B7FB", "popup_bg": "#FFFFFF",
            "accent": "#D8BA11", "btn_inactive": "#E0E0E0"
        }
        self.colors_dark = {
            "bg_main": "#121212", "container": "#1E1E1E", "card": "#2C2C2C",
            "text": "#E0E0E0", "search": "#333333", "popup_bg": "#1E1E1E",
            "accent": "#00E5FF", "btn_inactive": "#333333"
        }
        self.current_colors = self.colors_light
        self.overlay = self.popup_fenetre = None
        
        self.setup_ui()
        self.root.bind("<Key>", self.gerer_clavier)
        self.root.bind("<Configure>", self.redimensionner_auto)

        self.lancer_musique_fond("audios/background.mp3")
    def lancer_musique_fond(self, fichier_mp3):
        try:
            # On ouvre le fichier avec un alias pour le contrôler plus tard
            cmd = f'open "{fichier_mp3}" alias bg_music'
            ctypes.windll.winmm.mciSendStringW(cmd, None, 0, None)
            # On joue en boucle (repeat)
            ctypes.windll.winmm.mciSendStringW("play bg_music repeat", None, 0, None)
        except:
            print("Musique introuvable")

    def jouer_effet(self, type_effet):
        """ Joue un son .wav de façon asynchrone (ne bloque pas le jeu) """
        fichiers = {
            "ok": "audios/lettre_ok.wav",
            "erreur": "audios/erreur.wav",
            "victoire": "audios/victoire.wav"
        }
        try:
            # SND_ASYNC permet de continuer à jouer pendant que le son retentit
            winsound.PlaySound(fichiers[type_effet], winsound.SND_FILENAME | winsound.SND_ASYNC)
        except:
            pass

    def setup_ui(self):
        self.nettoyer_popups()
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg=self.current_colors["bg_main"])
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        self.header = tk.Frame(self.root, bg=self.current_colors["bg_main"])
        self.header.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        
        tk.Button(self.header, text="| | PAUSE", bg=self.current_colors["accent"], 
                  font=("Arial", 11, "bold"), relief="flat", command=self.afficher_pause).pack(side="left")
        
        self.score_canvas = tk.Canvas(self.header, width=200, height=40, bg=self.current_colors["bg_main"], highlightthickness=0)
        self.score_canvas.pack(side="right")
        self.dessiner_progression()

        self.main_container = tk.Frame(self.root, bg=self.current_colors["container"], bd=2, relief="solid")
        self.main_container.grid(row=1, column=0, sticky="nsew", padx=30, pady=10)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)

        self.lbl_theme = tk.Label(self.main_container, text=f" THÈME : {self.game.theme} ", bg="#333", fg="white", 
                                  font=("Arial", 10, "bold"), bd=1, relief="solid")
        self.lbl_theme.grid(row=0, column=0, sticky="nw", padx=15, pady=10)

        self.card = tk.Frame(self.main_container, bg=self.current_colors["card"], bd=2, relief="solid")
        self.card.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        
        self.lbl_question = tk.Label(self.card, text=self.game.question, bg=self.current_colors["card"], 
                                     fg=self.current_colors["text"], font=("Arial", 20, "bold"), justify="center")
        self.lbl_question.pack(expand=True, fill="both", padx=20)
        
        self.ans_f = tk.Frame(self.card, bg="black")
        self.ans_f.pack(fill="x", side="bottom")
        self.lbl_reponse = tk.Label(self.ans_f, text=" ".join(self.game.affichage), fg="#FF8A65", 
                                     bg="black", font=("Courier", 30, "bold"))
        self.lbl_reponse.pack(pady=15)

        self.footer = tk.Frame(self.root, bg=self.current_colors["bg_main"])
        self.footer.grid(row=2, column=0, sticky="ew", pady=10)
        self.vies_canvas = tk.Canvas(self.footer, width=180, height=40, bg=self.current_colors["bg_main"], highlightthickness=0)
        self.vies_canvas.pack(side="right", padx=30)
        self.dessiner_vies()

    def redimensionner_auto(self, event):
        largeur = self.root.winfo_width()
        taille_q = max(14, int(largeur / 45))
        taille_r = max(18, int(largeur / 35))
        self.lbl_question.config(font=("Arial", taille_q, "bold"), wraplength=int(largeur * 0.7))
        self.lbl_reponse.config(font=("Courier", taille_r, "bold"), wraplength=int(largeur * 0.8))

    def gerer_clavier(self, event):
        if self.popup_fenetre: return
        lettre = event.char.upper()
        if lettre.isalpha() and len(lettre) == 1:
            if lettre in self.game.reponse:
                self.jouer_effet("ok") # <--- SON SUCCÈS
                for i, c in enumerate(self.game.reponse):
                    if c == lettre: self.game.affichage[i] = lettre
                self.lbl_reponse.config(text=" ".join(self.game.affichage))
                if "_" not in self.game.affichage: self.victoire()
            else:
                self.jouer_effet("erreur") # <--- SON ERREUR
                self.nb_chances -= 1
                self.dessiner_vies()
                if self.nb_chances <= 0: self.recommencer_jeu()

    def victoire(self):
        self.jouer_effet("victoire") # <--- SON VICTOIRE
        try:
            idx = self.etats_questions.index(1)
            self.etats_questions[idx] = 2
            if idx + 1 < len(self.etats_questions):
                self.etats_questions[idx+1] = 1
        except ValueError: pass
        self.nb_chances = 5
        self.game.nouvelle_question()
        self.setup_ui()

    def dessiner_progression(self):
        self.score_canvas.delete("all")
        for i, etat in enumerate(self.etats_questions):
            color = "#66BB6A" if etat == 2 else "#FFA726" if etat == 1 else "#FFFFFF"
            self.score_canvas.create_oval(5 + (i*25), 10, 25 + (i*25), 30, fill=color, outline="black")

    def dessiner_vies(self):
        self.vies_canvas.delete("all")
        for i in range(5):
            x = 10 + (i * 35)
            color = "#FF0000" if i < self.nb_chances else "#581B1B"
            self.vies_canvas.create_polygon([x+10, 5, x+30, 5, x+20, 35, x, 35], fill=color, outline="black")
    

    # --- NOUVEAU DESIGN VOLUME ---
    def update_vol(self, valeur):
        self.volume_audio = int(valeur)
        # MCI utilise une échelle de 0 à 1000 pour le volume
        volume_mci = self.volume_audio * 10 
        cmd = f"setaudio bg_music volume to {volume_mci}"
        ctypes.windll.winmm.mciSendStringW(cmd, None, 0, None)
        
        self.rafraichir_vumetre()

    def rafraichir_vumetre(self):
        seuil = self.volume_audio / 10
        for i in range(10):
            if i < seuil:
                couleur = "#00E5FF"if i<3 else"#28C22F" if i < 6 else "#FFD54F" if i < 8 else "#FF5252"
                self.canvas_vol.itemconfig(self.blocs[i], fill=couleur, outline=couleur)
            else:
                self.canvas_vol.itemconfig(self.blocs[i], fill="#333333", outline="#222222")

    def afficher_pause(self):
        self.nettoyer_popups()
        self.overlay = tk.Frame(self.root, bg="black")
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.popup_fenetre = tk.Frame(self.root, bg=self.current_colors["popup_bg"], bd=3, relief="solid")
        self.popup_fenetre.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.45, relheight=0.75)

        tk.Label(self.popup_fenetre, text="RÉGLAGES", font=("Impact", 24), 
                 bg=self.current_colors["popup_bg"], fg=self.current_colors["text"]).pack(pady=10)

        # --- BLOC VOLUME MODERNE ---
        vol_container = tk.Frame(self.popup_fenetre, bg=self.current_colors["popup_bg"])
        vol_container.pack(fill="x", padx=40, pady=10)

        tk.Label(vol_container, text="🔊 MASTER VOLUME", font=("Courier", 10, "bold"), 
                 bg=self.current_colors["popup_bg"], fg=self.current_colors["text"]).pack(anchor="w")

        self.canvas_vol = tk.Canvas(vol_container, height=35, bg=self.current_colors["popup_bg"], highlightthickness=0)
        self.canvas_vol.pack(fill="x", pady=5)
        
        self.blocs = []
        for i in range(10):
            x0 = i * 32
            b = self.canvas_vol.create_rectangle(x0, 5, x0+28, 25, fill="#333", outline="#222", width=2)
            self.blocs.append(b)
        
        self.vol_control = tk.Scale(vol_container, from_=0, to=100, orient="horizontal", showvalue=False,
                                    troughcolor="#1A1A1A", bg=self.current_colors["popup_bg"],
                                    highlightthickness=0, command=self.update_vol, sliderlength=20)
        self.vol_control.set(self.volume_audio)
        self.vol_control.pack(fill="x")
        self.rafraichir_vumetre()

        # --- RESTE DU MENU ---
        icon = "🌙" if self.mode_nuit else "☀️"
        tk.Button(self.popup_fenetre, text=f"{icon} THÈME", font=("Arial", 10, "bold"),
                  bg=self.current_colors["accent"], relief="flat", command=self.basculer_mode).pack(fill="x", padx=40, pady=10)

        tk.Label(self.popup_fenetre, text="DIFFICULTÉ", font=("Arial", 9, "bold"), bg=self.current_colors["popup_bg"]).pack()
        df = tk.Frame(self.popup_fenetre, bg=self.current_colors["popup_bg"])
        df.pack()
        for d in ["Facile", "Normal", "Expert"]:
            c = self.current_colors["accent"] if self.difficulte_actuelle == d else self.current_colors["btn_inactive"]
            tk.Button(df, text=d.upper(), bg=c, font=("Arial", 8, "bold"), width=9,
                      command=lambda v=d: self.changer_diff(v)).pack(side="left", padx=3)

        tk.Button(self.popup_fenetre, text="CONTINUER", bg="#1B9C22", font=("Arial", 11, "bold"),
                  command=self.nettoyer_popups).pack(fill="x", padx=40, pady=(20, 10))
        tk.Button(self.popup_fenetre, text="REJOUER", bg="#DFE22D", font=("Arial", 11, "bold"),
                  command=self.recommencer_jeu).pack(fill="x", padx=40)

    def basculer_mode(self):
        self.mode_nuit = not self.mode_nuit
        self.current_colors = self.colors_dark if self.mode_nuit else self.colors_light
        self.setup_ui()
        self.afficher_pause()

    def changer_diff(self, d):
        self.difficulte_actuelle = d
        self.afficher_pause()

    def recommencer_jeu(self):
        self.nb_chances = 5
        self.etats_questions = [1] + [0]*6
        self.game.nouvelle_question()
        self.setup_ui()

    def nettoyer_popups(self):
        if self.overlay: self.overlay.destroy()
        if self.popup_fenetre: self.popup_fenetre.destroy()
        self.overlay = self.popup_fenetre = None

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceDAccueil1(root)
    root.mainloop()