# interface_proposee.py
import tkinter as tk
from tkinter import ttk

class GameInterface:
    """Interface graphique améliorée pour le jeu HELP ME !"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HELP ME ! - Jeu de Quiz")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1a2634")
        
        # Couleurs principales
        self.colors = {
            "primary": "#06E659",      # Vert néon
            "secondary": "#FF6B6B",     # Rouge corail
            "background": "#1a2634",    # Bleu nuit
            "surface": "#2c3e50",        # Gris bleuté
            "text": "#ecf0f1",           # Blanc cassé
            "accent": "#f39c12"          # Orange
        }
        
        # Variables de jeu
        self.chances = 4
        self.niveau = 1
        self.score = 0
        self.question_actuelle = 0
        self.total_questions = 8
        
        # Création des frames principales
        self.create_frames()
        
        # Affichage de l'accueil par défaut
        self.show_frame(self.accueil_frame)
    
    def create_frames(self):
        """Création de toutes les frames de l'application"""
        
        # Frame d'accueil
        self.accueil_frame = tk.Frame(self.root, bg=self.colors["background"])
        
        # Frame de jeu principal
        self.jeu_frame = tk.Frame(self.root, bg=self.colors["background"])
        
        # Frame de pause
        self.pause_frame = tk.Frame(self.root, bg=self.colors["background"])
        
        # Frame des paramètres
        self.parametres_frame = tk.Frame(self.root, bg=self.colors["background"])
        
        # Configuration de l'accueil
        self.setup_accueil()
        
        # Configuration du jeu
        self.setup_jeu()
        
        # Configuration de la pause
        self.setup_pause()
        
        # Configuration des paramètres
        self.setup_parametres()
    
    def setup_accueil(self):
        """Configuration de l'écran d'accueil"""
        # Titre principal
        title_frame = tk.Frame(self.accueil_frame, bg=self.colors["background"])
        title_frame.pack(pady=100)
        
        # Texte "HELP ME !"
        help_label = tk.Label(
            title_frame,
            text="HELP",
            font=("Arial", 80, "bold"),
            fg=self.colors["primary"],
            bg=self.colors["background"]
        )
        help_label.pack(side="left")
        
        me_label = tk.Label(
            title_frame,
            text=" ME !",
            font=("Arial", 80, "bold"),
            fg=self.colors["secondary"],
            bg=self.colors["background"]
        )
        me_label.pack(side="left")
        
        # Sous-titre
        subtitle = tk.Label(
            self.accueil_frame,
            text="Le jeu de culture générale qui vous aidera !",
            font=("Arial", 18, "italic"),
            fg=self.colors["text"],
            bg=self.colors["background"]
        )
        subtitle.pack(pady=20)
        
        # Frame pour les boutons
        buttons_frame = tk.Frame(self.accueil_frame, bg=self.colors["background"])
        buttons_frame.pack(pady=50)
        
        # Boutons de navigation
        jouer_btn = tk.Button(
            buttons_frame,
            text="JOUER",
            font=("Arial", 24, "bold"),
            fg="white",
            bg=self.colors["primary"],
            activebackground=self.colors["primary"],
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            width=15,
            height=2,
            command=self.start_game
        )
        jouer_btn.pack(pady=10)
        
        parametres_btn = tk.Button(
            buttons_frame,
            text="PARAMÈTRES",
            font=("Arial", 24, "bold"),
            fg="white",
            bg=self.colors["accent"],
            activebackground=self.colors["accent"],
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            width=15,
            height=2,
            command=self.show_parametres
        )
        parametres_btn.pack(pady=10)
        
        quitter_btn = tk.Button(
            buttons_frame,
            text="QUITTER",
            font=("Arial", 24, "bold"),
            fg="white",
            bg=self.colors["secondary"],
            activebackground=self.colors["secondary"],
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            width=15,
            height=2,
            command=self.root.quit
        )
        quitter_btn.pack(pady=10)
    
    def setup_jeu(self):
        """Configuration de l'interface de jeu principale"""
        
        # Barre supérieure
        top_bar = tk.Frame(self.jeu_frame, bg=self.colors["surface"], height=80)
        top_bar.pack(fill="x", padx=20, pady=20)
        top_bar.pack_propagate(False)
        
        # Bouton pause
        pause_btn = tk.Button(
            top_bar,
            text="⏸",
            font=("Arial", 20),
            fg="white",
            bg=self.colors["accent"],
            relief="flat",
            cursor="hand2",
            command=self.show_pause
        )
        pause_btn.pack(side="left", padx=20, pady=10)
        
        # Niveau et score
        info_frame = tk.Frame(top_bar, bg=self.colors["surface"])
        info_frame.pack(side="right", padx=20)
        
        self.niveau_label = tk.Label(
            info_frame,
            text=f"NIVEAU {self.niveau}",
            font=("Arial", 18, "bold"),
            fg=self.colors["primary"],
            bg=self.colors["surface"]
        )
        self.niveau_label.pack(side="left", padx=20)
        
        self.score_label = tk.Label(
            info_frame,
            text=f"🏆 {self.score}",
            font=("Arial", 18, "bold"),
            fg=self.colors["accent"],
            bg=self.colors["surface"]
        )
        self.score_label.pack(side="left", padx=20)
        
        # Indicateur de progression (cercles)
        progress_frame = tk.Frame(self.jeu_frame, bg=self.colors["background"])
        progress_frame.pack(pady=20)
        
        self.progress_circles = []
        for i in range(self.total_questions):
            canvas = tk.Canvas(
                progress_frame,
                width=40,
                height=40,
                bg=self.colors["background"],
                highlightthickness=0
            )
            canvas.pack(side="left", padx=5)
            
            # Dessiner le cercle
            canvas.create_oval(
                5, 5, 35, 35,
                fill=self.colors["surface"],
                outline=self.colors["primary"],
                width=2
            )
            self.progress_circles.append(canvas)
        
        # Carte de thème
        theme_card = tk.Frame(
            self.jeu_frame,
            bg=self.colors["surface"],
            relief="raised",
            bd=2
        )
        theme_card.pack(pady=20, padx=200, fill="x")
        
        self.theme_label = tk.Label(
            theme_card,
            text="THÈME : HISTOIRE",
            font=("Arial", 24, "bold"),
            fg=self.colors["primary"],
            bg=self.colors["surface"]
        )
        self.theme_label.pack(pady=15)
        
        # Carte de question
        question_card = tk.Frame(
            self.jeu_frame,
            bg=self.colors["surface"],
            relief="raised",
            bd=2
        )
        question_card.pack(pady=20, padx=100, fill="both", expand=True)
        
        self.question_label = tk.Label(
            question_card,
            text="Quel traité a mis fin à la Première Guerre mondiale ?",
            font=("Arial", 20),
            fg=self.colors["text"],
            bg=self.colors["surface"],
            wraplength=800
        )
        self.question_label.pack(pady=40, padx=40)
        
        # Zone de réponse
        answer_frame = tk.Frame(self.jeu_frame, bg=self.colors["background"])
        answer_frame.pack(pady=30)
        
        self.answer_labels = []
        reponse = ["V", "_", "_", "_", "_", "_", "_", "_", "_"]
        for char in reponse:
            label = tk.Label(
                answer_frame,
                text=char,
                font=("Courier", 32, "bold"),
                fg=self.colors["primary"],
                bg=self.colors["background"],
                width=2
            )
            label.pack(side="left")
            self.answer_labels.append(label)
        
        # Indicateur de chances
        chances_frame = tk.Frame(self.jeu_frame, bg=self.colors["background"])
        chances_frame.pack(pady=20)
        
        tk.Label(
            chances_frame,
            text="CHANCES RESTANTES :",
            font=("Arial", 14),
            fg=self.colors["text"],
            bg=self.colors["background"]
        ).pack(side="left", padx=10)
        
        self.chances_labels = []
        for i in range(4):
            label = tk.Label(
                chances_frame,
                text="❤",
                font=("Arial", 20),
                fg=self.colors["secondary"],
                bg=self.colors["background"]
            )
            label.pack(side="left", padx=5)
            self.chances_labels.append(label)
        
        # Zone de saisie
        input_frame = tk.Frame(self.jeu_frame, bg=self.colors["background"])
        input_frame.pack(pady=20)
        
        tk.Label(
            input_frame,
            text="Entrez une lettre :",
            font=("Arial", 14),
            fg=self.colors["text"],
            bg=self.colors["background"]
        ).pack(side="left", padx=10)
        
        self.input_entry = tk.Entry(
            input_frame,
            font=("Arial", 18),
            width=5,
            justify="center",
            relief="solid",
            bd=2
        )
        self.input_entry.pack(side="left", padx=10)
        self.input_entry.bind("<Return>", self.check_answer)
        
        submit_btn = tk.Button(
            input_frame,
            text="VALIDER",
            font=("Arial", 14, "bold"),
            fg="white",
            bg=self.colors["primary"],
            relief="flat",
            cursor="hand2",
            command=lambda: self.check_answer()
        )
        submit_btn.pack(side="left", padx=10)
    
    def setup_pause(self):
        """Configuration de l'écran de pause"""
        # Cadre de pause
        pause_box = tk.Frame(
            self.pause_frame,
            bg=self.colors["surface"],
            relief="raised",
            bd=3
        )
        pause_box.place(relx=0.5, rely=0.5, anchor="center", width=400, height=300)
        
        tk.Label(
            pause_box,
            text="⏸ PAUSE",
            font=("Arial", 36, "bold"),
            fg=self.colors["primary"],
            bg=self.colors["surface"]
        ).pack(pady=30)
        
        # Boutons de pause
        btn_frame = tk.Frame(pause_box, bg=self.colors["surface"])
        btn_frame.pack(expand=True)
        
        continuer_btn = tk.Button(
            btn_frame,
            text="CONTINUER",
            font=("Arial", 16, "bold"),
            fg="white",
            bg=self.colors["primary"],
            relief="flat",
            cursor="hand2",
            width=15,
            command=lambda: self.show_frame(self.jeu_frame)
        )
        continuer_btn.pack(pady=10)
        
        accueil_btn = tk.Button(
            btn_frame,
            text="ACCUEIL",
            font=("Arial", 16, "bold"),
            fg="white",
            bg=self.colors["accent"],
            relief="flat",
            cursor="hand2",
            width=15,
            command=lambda: self.show_frame(self.accueil_frame)
        )
        accueil_btn.pack(pady=10)
    
    def setup_parametres(self):
        """Configuration de l'écran des paramètres"""
        # Titre
        tk.Label(
            self.parametres_frame,
            text="PARAMÈTRES",
            font=("Arial", 48, "bold"),
            fg=self.colors["primary"],
            bg=self.colors["background"]
        ).pack(pady=50)
        
        # Options
        options_frame = tk.Frame(self.parametres_frame, bg=self.colors["surface"])
        options_frame.pack(pady=30, padx=200, fill="both", expand=True)
        
        # Mode nuit
        night_frame = tk.Frame(options_frame, bg=self.colors["surface"])
        night_frame.pack(pady=20, padx=50, fill="x")
        
        tk.Label(
            night_frame,
            text="Mode nuit",
            font=("Arial", 18),
            fg=self.colors["text"],
            bg=self.colors["surface"]
        ).pack(side="left")
        
        self.night_mode_var = tk.BooleanVar(value=True)
        night_check = tk.Checkbutton(
            night_frame,
            variable=self.night_mode_var,
            bg=self.colors["surface"],
            activebackground=self.colors["surface"],
            selectcolor=self.colors["primary"]
        )
        night_check.pack(side="right")
        
        # Volume
        volume_frame = tk.Frame(options_frame, bg=self.colors["surface"])
        volume_frame.pack(pady=20, padx=50, fill="x")
        
        tk.Label(
            volume_frame,
            text="Volume",
            font=("Arial", 18),
            fg=self.colors["text"],
            bg=self.colors["surface"]
        ).pack(side="left")
        
        self.volume_var = tk.DoubleVar(value=50)
        volume_scale = tk.Scale(
            volume_frame,
            from_=0,
            to=100,
            orient="horizontal",
            variable=self.volume_var,
            bg=self.colors["surface"],
            fg=self.colors["text"],
            highlightbackground=self.colors["primary"],
            troughcolor=self.colors["background"]
        )
        volume_scale.pack(side="right", padx=20)
        
        # Difficulté
        difficulte_frame = tk.Frame(options_frame, bg=self.colors["surface"])
        difficulte_frame.pack(pady=20, padx=50, fill="x")
        
        tk.Label(
            difficulte_frame,
            text="Difficulté",
            font=("Arial", 18),
            fg=self.colors["text"],
            bg=self.colors["surface"]
        ).pack(side="left")
        
        self.difficulte_var = tk.StringVar(value="Moyen")
        difficulte_combo = ttk.Combobox(
            difficulte_frame,
            textvariable=self.difficulte_var,
            values=["Facile", "Moyen", "Difficile"],
            state="readonly",
            font=("Arial", 14),
            width=10
        )
        difficulte_combo.pack(side="right", padx=20)
        
        # Bouton retour
        retour_btn = tk.Button(
            self.parametres_frame,
            text="← RETOUR",
            font=("Arial", 16, "bold"),
            fg="white",
            bg=self.colors["secondary"],
            relief="flat",
            cursor="hand2",
            command=lambda: self.show_frame(self.accueil_frame)
        )
        retour_btn.pack(pady=30)
    
    def show_frame(self, frame):
        """Affiche la frame spécifiée et cache les autres"""
        self.accueil_frame.pack_forget()
        self.jeu_frame.pack_forget()
        self.pause_frame.pack_forget()
        self.parametres_frame.pack_forget()
        frame.pack(fill="both", expand=True)
    
    def start_game(self):
        """Démarre le jeu"""
        self.show_frame(self.jeu_frame)
        self.input_entry.focus()
    
    def show_pause(self):
        """Affiche l'écran de pause"""
        self.show_frame(self.pause_frame)
    
    def show_parametres(self):
        """Affiche l'écran des paramètres"""
        self.show_frame(self.parametres_frame)
    
    def check_answer(self, event=None):
        """Vérifie la réponse de l'utilisateur"""
        lettre = self.input_entry.get().upper()
        if lettre and len(lettre) == 1 and lettre.isalpha():
            # Simulation d'une réponse correcte
            self.input_entry.delete(0, tk.END)
            self.score += 10
            self.score_label.config(text=f"🏆 {self.score}")
            
            # Mise à jour des cercles de progression
            if self.question_actuelle < self.total_questions:
                self.progress_circles[self.question_actuelle].itemconfig(1, fill=self.colors["primary"])
                self.question_actuelle += 1
    
    def run(self):
        """Lance l'application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = GameInterface()
    app.run()