import customtkinter as ctk

class PrayerButton(ctk.CTkButton):
    def __init__(self, master, text, command, **kwargs):
        super().__init__(
            master, text=text, command=command, corner_radius=20, height=45,
            font=("Arial", 14, "bold"), fg_color="#ECEFF1", text_color="#455A64",
            hover_color="#CFD8DC", **kwargs
        )