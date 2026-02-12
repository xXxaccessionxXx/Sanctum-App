import customtkinter as ctk

class VerseDisplay(ctk.CTkFrame):
    def __init__(self, master, scripture=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.text_label = ctk.CTkLabel(
            self, text="", font=("Times New Roman", 22, "italic"),
            text_color="#1A237E", wraplength=500, justify="center"
        )
        self.text_label.pack(pady=(10, 5))

        self.ref_label = ctk.CTkLabel(self, text="", font=("Arial", 11, "bold"), text_color="#F57F17")
        self.ref_label.pack()

        if scripture: self.update_verse(scripture)

    def update_verse(self, scripture):
        if scripture:
            self.text_label.configure(text=f'"{scripture.text}"')
            self.ref_label.configure(text=scripture.reference.upper())
        else:
            self.text_label.configure(text="Select a module to begin.")