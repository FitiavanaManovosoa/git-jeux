import tkinter as tk
from PIL import Image, ImageTk
import os
import importlib.util
import winsound
import ctypes
import math

class ApplicationComplete:
    def __init__(self, root):
        self.root = root
        self.root.title("HELP ME!")
        
        self.largeur_base = 1024
        self.hauteur_base = 768
        self.root.geometry(f"{self.largeur_base}x{self.hauteur_base}")
        self.root.resizable(True, True) 
        
        self.dossier = os.path.dirname(os.path.abspath(__file__))
        self.ecran_actuel = "chargement"
        
        self.lancer_musique_fond()

        self.val = 0
        self.f_idx = 0
        self.bg_tk = None
        self.frames = []
        self.sprite_img = None

        self.wave_phase = 0.0
        self.wave_speed = 0.08
        self.wave_amplitude = 6.0
        self.letter_ids = []
        self.texte_y_actuel = 0
        self.texte_y_cible = 0
        self.lettres_opacite = 0.0
        self.texte_en_mouvement = False
        
        self.root.bind("<Configure>", self.repositionner_tout)
        
        self.ecran_chargement()

    def lancer_musique_fond(self):
        chemin_bg = os.path.join(self.dossier, "assets", "background.mp3")
        if os.path.exists(chemin_bg):
            try:
                ctypes.windll.winmm.mciSendStringW(f'open "{chemin_bg}" alias bg_music', None, 0, None)
                ctypes.windll.winmm.mciSendStringW("play bg_music repeat", None, 0, None)
            except:
                pass

    def jouer_clic(self):
        chemin_clic = os.path.join(self.dossier, "assets", "click.wav")
        if os.path.exists(chemin_clic):
            winsound.PlaySound(chemin_clic, winsound.SND_FILENAME | winsound.SND_ASYNC)

    def nettoyer(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg="#121212")

    def ecran_chargement(self):
        self.nettoyer()
        self.ecran_actuel = "chargement"
        
        self.canvas = tk.Canvas(self.root, highlightthickness=0, bg="#121212")
        self.canvas.pack(fill="both", expand=True)

        try:
            self.bg_raw = Image.open(os.path.join(self.dossier, "bg.png"))
            self.bg_tk = ImageTk.PhotoImage(self.bg_raw)
            self.canvas.create_image(0, 0, anchor="nw", image=self.bg_tk, tags="fond")
        except:
            self.bg_raw = None
            print("bg.png introuvable")

        self.frames = []
        for i in range(1, 7):
            try:
                img_path = os.path.join(self.dossier, f"l{i}.png")
                img = Image.open(img_path).convert("RGBA").resize((100, 100))
                self.frames.append(ImageTk.PhotoImage(img))
            except Exception as e:
                print(f"Erreur chargement l{i}.png → {e}")

        # Texte
        texte = "HELP ME!"
        font_size = 80
        font = ("Impact", font_size, "bold")
        espacement = font_size * 0.85

        self.letter_ids = []
        x_courant = 0

        for char in texte:
            if char == " ":
                x_courant += espacement * 0.5
                continue
            lettre_id = self.canvas.create_text(
                x_courant, 0,
                text=char,
                font=font,
                fill="#ffffff",
                anchor="center",
                tags="vague_lettre"
            )
            self.letter_ids.append(lettre_id)
            x_courant += espacement

        self.root.after(300, self.lancer_apparition_texte)
        self.root.after(3200, self.demarrer_chargement)

    def lancer_apparition_texte(self):
        if self.ecran_actuel != "chargement":
            return

        W = self.root.winfo_width()
        H = self.root.winfo_height()
        by = H - 150
        self.texte_y_cible = by - 220

        if not self.texte_en_mouvement:
            self.texte_en_mouvement = True
            self.texte_y_actuel = H + 120
            self.lettres_opacite = 0.05

        self.texte_y_actuel -= 9.0
        self.lettres_opacite = min(1.0, self.lettres_opacite + 0.032)

        largeur_totale = (len(self.letter_ids) - 1) * (80 * 0.85) + 80
        x_debut = (W // 2) - (largeur_totale / 2) + 40   # ← +40 = vers la droite

        self.wave_phase += self.wave_speed

        x_courant = x_debut
        for i, lettre_id in enumerate(self.letter_ids):
            offset_y = math.sin(self.wave_phase + i * 1.3) * self.wave_amplitude
            alpha = int(255 * self.lettres_opacite)
            couleur = f'#{alpha:02x}{alpha:02x}{alpha:02x}'
            self.canvas.itemconfig(lettre_id, fill=couleur)
            self.canvas.coords(lettre_id, x_courant, self.texte_y_actuel + offset_y)
            x_courant += 80 * 0.85

        if self.texte_y_actuel > self.texte_y_cible + 5:
            self.root.after(28, self.lancer_apparition_texte)
        else:
            self.texte_y_actuel = self.texte_y_cible
            self.root.after(45, self.animer_vague_seul)

    def animer_vague_seul(self):
        if self.ecran_actuel != "chargement":
            return

        W = self.root.winfo_width()
        H = self.root.winfo_height()
        by = H - 150
        y_base = by - 220

        largeur_totale = (len(self.letter_ids) - 1) * (80 * 0.85) + 80
        x_debut = (W // 2) - (largeur_totale / 2) + 40   # ← +40 = vers la droite

        self.wave_phase += self.wave_speed

        x_courant = x_debut
        for i, lettre_id in enumerate(self.letter_ids):
            offset_y = math.sin(self.wave_phase + i * 1.3) * self.wave_amplitude
            self.canvas.coords(lettre_id, x_courant, y_base + offset_y)
            x_courant += 80 * 0.85

        self.root.after(45, self.animer_vague_seul)

    def demarrer_chargement(self):
        if self.ecran_actuel != "chargement":
            return

        self.canvas.create_rectangle(0, 0, 0, 0, fill="#222222", outline="#00ffcc", width=3, tags="barre_contour")
        self.canvas.create_rectangle(0, 0, 0, 0, fill="#00ffcc", outline="", tags="barre_plein")
        self.canvas.create_text(0, 0, text="0%", fill="#00ffcc", font=("Verdana", 14, "bold"), tags="txt_perc")

        if self.frames:
            self.sprite_img = self.frames[0]
            self.canvas.create_image(0, 0, image=self.sprite_img, tags="mon_sprite")

        self.boucle_chargement()

    def repositionner_tout(self, event=None):
        W = self.root.winfo_width()
        H = self.root.winfo_height()

        if self.bg_raw:
            self.bg_tk = ImageTk.PhotoImage(self.bg_raw.resize((W, H)))
            self.canvas.itemconfig("fond", image=self.bg_tk)

        if self.ecran_actuel == "chargement":
            bw, bh = 500, 18
            bx = (W // 2) - (bw // 2)
            by = H - 150

            x_progress = bx + (self.val / 100 * bw)

            self.canvas.coords("barre_contour", bx-5, by-5, bx+bw+5, by+bh+5)
            self.canvas.coords("barre_plein", bx, by, x_progress, by + bh)
            self.canvas.coords("txt_perc", W // 2, by + 45)

            if self.sprite_img:
                self.canvas.coords("mon_sprite", x_progress, by - 55)

        elif self.ecran_actuel == "menu":
            self.canvas.coords("titre", W // 2, H // 4)
            self.canvas.coords("win_play", W // 2, H // 2)
            self.canvas.coords("win_quit", W // 2, H // 2 + 120)

    def boucle_chargement(self):
        if self.val < 100:
            self.val += 0.5
            self.canvas.itemconfig("txt_perc", text=f"{int(self.val)}%")

            if self.frames and int(self.val * 10) % 4 == 0:
                self.f_idx = (self.f_idx + 1) % len(self.frames)
                self.sprite_img = self.frames[self.f_idx]
                self.canvas.itemconfig("mon_sprite", image=self.sprite_img)

            self.repositionner_tout()
            self.root.after(20, self.boucle_chargement)
        else:
            self.root.after(500, self.ecran_menu)

    def ecran_menu(self):
        self.nettoyer()
        self.ecran_actuel = "menu"
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        if self.bg_tk: 
            self.canvas.create_image(0, 0, image=self.bg_tk, anchor="nw", tags="fond")

        self.canvas.create_text(0, 0, text="MENU PRINCIPAL", font=("Impact", 65), fill="#00ffcc", tags="titre")

        btn_play = tk.Button(self.root, text="JOUER", font=("Arial", 16, "bold"), 
                             bg="#00ffcc", fg="black", width=25, height=2,
                             relief="flat", cursor="hand2", 
                             command=lambda: [self.jouer_clic(), self.lancer_idee_1()])
        self.canvas.create_window(0, 0, window=btn_play, tags="win_play")

        btn_quit = tk.Button(self.root, text="QUITTER", font=("Arial", 16, "bold"), 
                             bg="#e74c3c", fg="white", width=25, height=2,
                             relief="flat", cursor="hand2", 
                             command=lambda: [self.jouer_clic(), self.root.after(200, self.root.quit)])
        self.canvas.create_window(0, 0, window=btn_quit, tags="win_quit")
        
        self.repositionner_tout()

    def lancer_idee_1(self):
        nom_f = "interface idee1.py"
        chemin = os.path.join(self.dossier, nom_f)
        try:
            self.nettoyer()
            spec = importlib.util.spec_from_file_location("idee1", chemin)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.InterfaceDAccueil1(self.root)
        except Exception as e:
            print(f"Erreur lancement idee1 : {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ApplicationComplete(root)
    root.mainloop()