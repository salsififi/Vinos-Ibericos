"""
VINOS IBERICOS
Réponse au challenge "Vinos ibericos" proposé sur le serveur Discord "Doctring"
"""

import tkinter as tk

from PIL import Image, ImageTk

from constants import *


class VinosIbericosApp:
    """Crée l'interface graphique de l'application"""

    def __init__(self, ctx: tk.Tk) -> None:
        self.root = ctx
        self.map = self.get_map_image()
        self.tinto = ImageTk.PhotoImage(Image.open(TINTO_PATH))
        self.blanco = ImageTk.PhotoImage(Image.open(BLANCO_PATH))
        self.bottle_labels = {}

        self.create_ui()

    @staticmethod
    def get_map_image() -> tk.PhotoImage:
        """Charge et redimensionne la carte"""
        original_map = Image.open(MAP_PATH)
        map_resized = original_map.resize((int(original_map.width * RESIZE_MAP_RATE),
                                           int(original_map.height * RESIZE_MAP_RATE)))
        return ImageTk.PhotoImage(map_resized)

    def create_ui(self):
        """Crée l'interface graphique"""
        # Fenêtre principale
        self.root.title("Vinos ibericos")

        # Création des cadres
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        self.left_frame = tk.Frame(self.main_frame, height=self.map.height())
        self.left_frame.grid(row=0, column=0, sticky="ns")
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        # Création des boutons
        for region in DO_VINOS:
            button = tk.Button(self.left_frame, text=region, command=lambda r=region: self.toggle_bottle(r))
            button.pack()

        # Intégration de la carte
        self.map_label = tk.Label(self.right_frame, image=self.map)
        self.map_label.grid(row=0, column=0)

        # Limitation de la taille de la fenêtre principale
        self.root.geometry(f"1000x{self.map.height() + 10}")

    def toggle_bottle(self, region):
        # Vérifie si l'image de la bouteille est déjà affichée
        if region in self.bottle_labels:
            # Masque et supprime l'image de la bouteille
            self.bottle_labels[region].destroy()
            del self.bottle_labels[region]
        else:
            # Affiche l'image de la bouteille
            coords, wine_type = DO_VINOS[region]
            x, y = gps_to_px(coords, self.map.width(), self.map.height())
            x = int(x * RESIZE_MAP_RATE)  # Ajuste les coordonnées pour l'image redimensionnée
            y = int(y * RESIZE_MAP_RATE)

            if wine_type == "Tinto":
                bottle_img = self.tinto
            else:
                bottle_img = self.blanco

            label = tk.Label(self.map_label, image=bottle_img)
            label.place(x=x, y=y)


def gps_to_px(yx_gps: tuple[float, float], img_width: int, img_height: int):
    """Convertit les coordonnées GPS en position en pixels sur l'image"""
    latitude, longitude = yx_gps
    lat_span = GPS["N"] - GPS["S"]
    lon_span = GPS["E"] - GPS["W"]
    x = (longitude - GPS["W"]) / lon_span * img_width
    y = (GPS["N"] - latitude) / lat_span * img_height
    return int(x), int(y)


if __name__ == '__main__':
    root = tk.Tk()
    app = VinosIbericosApp(root)
    root.mainloop()
