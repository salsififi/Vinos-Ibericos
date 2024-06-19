"""
VINOS IBERICOS
Answer to the "Vinos ibericos" challenge proposed on "Doctring" Discord server
Date: 2024-06-19
"""
import tkinter as tk

from PIL import Image, ImageTk
from tkintermapview import TkinterMapView
from tkintermapview.canvas_position_marker import CanvasPositionMarker

from constants import *


class VinosIbericosApp:
    """Crée l'interface graphique de l'application"""

    def __init__(self, ctx: tk.Tk) -> None:
        self.root = ctx
        self.root.title("VINOS IBERICOS")
        self.tinto = ImageTk.PhotoImage(Image.open(TINTO_PATH))
        self.blanco = ImageTk.PhotoImage(Image.open(BLANCO_PATH))
        self.buttons_by_region: dict[str, tk.Button] = {}
        self.markers_by_region: dict[str, CanvasPositionMarker] = {}

        self.create_ui()

    # region UI
    def create_ui(self) -> None:
        """Creates application user interface"""
        self.create_frames()
        self.modify_frames()
        self.create_widgets()

    def create_frames(self) -> None:
        """Creates UI frames"""
        self.main_frame = tk.Frame(self.root)
        self.regions_frame = tk.Frame(self.main_frame)
        self.map_frame = tk.Frame(self.main_frame)
        self.filters_frame = tk.Frame(self.main_frame)

    def modify_frames(self) -> None:
        """Modifies UI frames"""
        self.main_frame.pack(fill="both", expand=True)
        self.map_frame.grid(row=0, column=1, sticky="nsew")
        self.regions_frame.grid(row=0, column=0, sticky="ns")
        self.filters_frame.grid(row=1, column=1, sticky="ew")

        self.filters_frame.columnconfigure(0, weight=1)
        self.filters_frame.columnconfigure(1, weight=1)
        self.filters_frame.columnconfigure(2, weight=1)
        self.filters_frame.columnconfigure(3, weight=1)

    def create_widgets(self) -> None:
        """Creates all UI widgets"""
        # Boutons de filtre par région
        for region in DO_VINOS:
            button = tk.Button(self.regions_frame, text=region, bg="white",
                               command=lambda r=region: self.toggle_bottle(r))
            button.pack(pady=1)
            self.buttons_by_region[region] = button

        # Autres boutons d'affichage et de filtre
        self.btn_show_tinto = tk.Button(self.filters_frame, text="Du rouge!", bg="red",
                                        command=lambda: self.show_wine("Tinto"))
        self.btn_show_tinto.grid(row=0, column=0, padx=10, pady=5)
        self.btn_show_blanco = tk.Button(self.filters_frame, text="Du blanc!", bg="yellow",
                                         command=lambda: self.show_wine("Blanco"))
        self.btn_show_blanco.grid(row=0, column=1, padx=10, pady=5)
        self.btn_show_all = tk.Button(self.filters_frame, text="À BOIRE!!!",
                                      bg="blue", fg="white", font=("Helvetica", 16),
                                      command=self.show_all)
        self.btn_show_all.grid(row=0, column=2, padx=10, pady=5)
        self.btn_delete_all = tk.Button(self.filters_frame, text="Plus soif...",
                                        bg="black", fg="white",
                                        command=self.delete_all_markers)
        self.btn_delete_all.grid(row=0, column=3, padx=10, pady=5)

        # Carte
        self.map = TkinterMapView(self.map_frame, width=1000)
        self.map.pack(fill="both", expand=True)
        self.map.set_position(40.416775, -3.703790)  # centre géographique de l'Espagne
        self.map.set_zoom(5)
    # endregion

    # region Methods in alphabetical order
    def delete_all_markers(self) -> None:
        """Deletes all markers from the map"""
        for region in DO_VINOS:
            self.delete_marker(region)

    def delete_marker(self, region: str) -> None:
        """Delete a region marker from the map"""
        if self.markers_by_region.get(region):
            self.markers_by_region[region].delete()
            del self.markers_by_region[region]

    def show_region(self, region: str) -> None:
        """Places bottle icon of the region on the map"""
        if not self.markers_by_region.get(region):
            (deg_x, deg_y), wine = DO_VINOS[region]
            marker = self.map.set_marker(deg_x, deg_y,
                                         icon=self.tinto if wine == "Tinto" else self.blanco)
            self.markers_by_region[region] = marker

    def show_wine(self, chosen_wine: str) -> None:
        """Shows only bottles of selected wine"""
        self.delete_all_markers()
        for region, (_, wine) in DO_VINOS.items():
            if wine == chosen_wine:
                self.show_region(region)

    def show_all(self) -> None:
        """Shows all bottle icons"""
        for region in DO_VINOS:
            self.show_region(region)

    def toggle_bottle(self, region: str) -> None:
        """Displays or hides bottle icon for a given region"""
        if self.markers_by_region.get(region):
            self.delete_marker(region)
            self.buttons_by_region[region].config(bg="white")
        else:
            self.show_region(region)
            self.buttons_by_region[region].config(bg="green")
    # endregion


if __name__ == '__main__':
    root = tk.Tk()
    app = VinosIbericosApp(root)
    root.mainloop()
