import tkinter as tk
import os
from PIL import Image, ImageTk

# Configuration du dossier
BASE_DIR = os.path.dirname(__file__)

root = tk.Tk()
root.title("Animation avec Fond - Correction")

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# 1. Chargement du FOND
try:
    # Vérifie bien que le nom est exactement "bg accuiel.png" (avec l'espace)
    bg_path = os.path.join(BASE_DIR, "bg accuiel.png")
    bg_image_raw = Image.open(bg_path)
    bg_image_resized = bg_image_raw.resize((1203, 473), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image_resized)
    
    # CRUCIAL : On attache l'image au canvas pour éviter qu'elle soit supprimée de la mémoire
    canvas.bg_photo = bg_photo 
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
except Exception as e:
    print(f"Erreur fond : {e}")
    canvas.configure(bg="lightblue")

# 2. Chargement des frames du SPRITE
frames = []
for i in range(1, 9):
    # ATTENTION : vérifie si tes fichiers s'appellent "r1.png" ou "r (1).png"
    # Ici j'utilise "r (i).png" comme dans ton premier message
    path = os.path.join(BASE_DIR, f"r{i}.png")
    
    if os.path.exists(path):
        img = Image.open(path).resize((150, 150), Image.Resampling.LANCZOS)
        frames.append(ImageTk.PhotoImage(img))
    else:
        print(f"Fichier manquant : {path}")

# Sécurité : on vérifie si la liste n'est pas vide
if not frames:
    print("Erreur : Aucune frame chargée. Vérifiez les noms de fichiers.")
    root.destroy()
    exit()

# 3. Création du personnage
current_frame = 0
sprite = canvas.create_image(200, 200, image=frames[0])

# 4. Fonction d'animation
def animate():
    global current_frame
    current_frame = (current_frame + 1) % len(frames)
    canvas.itemconfig(sprite, image=frames[current_frame])
    root.after(150, animate)

animate()
root.mainloop()