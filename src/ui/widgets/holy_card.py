import customtkinter as ctk

class HolyCard(ctk.CTkFrame):
    def __init__(self, master, icon_char, title, color, on_click=None, **kwargs):
        super().__init__(master, fg_color="white", corner_radius=15, border_width=1, border_color="#E0E0E0", **kwargs)
        self.on_click = on_click
        
        # --- Hover Effects ---
        self.default_color = "white"
        self.hover_color = "#F5F5F5" # Very light gray for hover

        # Bind click event to the frame
        self.bind("<Button-1>", self._handle_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
        # Icon
        self.icon_label = ctk.CTkLabel(self, text=icon_char, font=("Arial", 32), text_color=color)
        self.icon_label.pack(pady=(25, 5))
        self.icon_label.bind("<Button-1>", self._handle_click)
        self.icon_label.bind("<Enter>", self.on_enter)
        self.icon_label.bind("<Leave>", self.on_leave)

        # Title
        self.title_label = ctk.CTkLabel(self, text=title, font=("Times New Roman", 18, "bold"), text_color="#424242")
        self.title_label.pack(pady=(0, 25))
        self.title_label.bind("<Button-1>", self._handle_click)
        self.title_label.bind("<Enter>", self.on_enter)
        self.title_label.bind("<Leave>", self.on_leave)

    def _handle_click(self, event):
        if self.on_click: self.on_click()

    def on_enter(self, event):
        self.configure(fg_color=self.hover_color)

    def on_leave(self, event):
        self.configure(fg_color=self.default_color)