import tkinter as tk
from PIL import Image, ImageTk
import os

class InterfaceDesign:
    def __init__(self, root):
        self.root = root
        self.root.title("HELP ME!")
        self.root.geometry("1024x768")

        dossier_actuel = os.path.dirname(os.path.abspath(__file__))

        # --- 1. CHARGEMENT FOND ET SPRITES ---
        self.bg_photo = None
        try:
            path_bg = os.path.join(dossier_actuel, "bg.png")
            if os.path.exists(path_bg):
                img_bg = Image.open(path_bg).resize((1024, 768))
                self.bg_photo = ImageTk.PhotoImage(img_bg)
        except Exception as e:
            print(f"Erreur chargement BG: {e}")

        self.frames = []
        for i in range(1, 7):
            try:
                path_img = os.path.join(dossier_actuel, f"r{i}.png")
                if os.path.exists(path_img):
                    img = Image.open(path_img).convert("RGBA")
                    self.frames.append(ImageTk.PhotoImage(img.resize((100, 100))))
            except Exception as e:
                print(f"Erreur frame {i}: {e}")

        # --- 2. CANVAS ---
        self.canvas = tk.Canvas(root, width=800, height=600, highlightthickness=0, bg="#222")
        self.canvas.pack(fill="both", expand=True)

        if self.bg_photo:
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # --- 3. DESIGN DE LA BARRE ---
        self.bar_x, self.bar_y = 200, 450
        self.bar_width, self.bar_height = 400, 25
        
        # Fond de la barre
        self.canvas.create_rectangle(self.bar_x-2, self.bar_y-2, self.bar_x+self.bar_width+2, 
                                     self.bar_y+self.bar_height+2, fill="#1a1a1a", outline="#3d3d3d")
        
        # Remplissage
        self.progress_fill = self.canvas.create_rectangle(self.bar_x, self.bar_y, self.bar_x, 
                                                          self.bar_y+self.bar_height, fill="#00ffcc", outline="")

        # --- 4. SPRITE ET BOUCLE ---
        # SÉCURITÉ : Si pas d'images, on crée un rectangle rouge à la place
        if self.frames:
            self.sprite_id = self.canvas.create_image(400, 400, image=self.frames[0])
        else:
            self.sprite_id = self.canvas.create_rectangle(350, 350, 450, 450, fill="red")
            print("Mode dégradé : Aucune image trouvée, utilisation d'un carré rouge.")

        self.progress_val = 0
        self.current_frame = 0
        self.update_loop()

    def update_loop(self):
        # Animation Sprite (seulement si images présentes)
        if self.frames:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.canvas.itemconfig(self.sprite_id, image=self.frames[self.current_frame])

        # Progression
        if self.progress_val < 100:
            self.progress_val += 0.4
            current_w = self.bar_x + (self.progress_val / 100 * self.bar_width)
            
            # Mise à jour de la barre
            self.canvas.coords(self.progress_fill, self.bar_x, self.bar_y, current_w, self.bar_y+self.bar_height)
            
            # Faire suivre le sprite (ou le carré rouge)
            # On ajuste le Y pour qu'il soit juste au-dessus de la barre
            self.canvas.coords(self.sprite_id, current_w, self.bar_y - 50)

        self.root.after(50, self.update_loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceDesign(root)
    root.mainloop()