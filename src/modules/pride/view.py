import customtkinter as ctk

class PrideView(ctk.CTkFrame):
    def __init__(self, master, module, on_back=None, **kwargs):
        super().__init__(master, fg_color="#F3E5F5", **kwargs) # Light Purple
        self.module = module
        self.on_back = on_back

        # --- Header ---
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=20)
        
        back_btn = ctk.CTkButton(self.header, text="← Back", width=60, fg_color="transparent", text_color="gray", hover_color="#E1BEE7", command=self.on_back)
        back_btn.pack(side="left")
        
        title = ctk.CTkLabel(self.header, text=f"{module.icon_char} {module.title}", font=("Arial", 24, "bold"), text_color="#4A148C")
        title.pack(side="left", padx=20)

        # --- The Hidden Intercessor ---
        self.intercessor_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        self.intercessor_frame.pack(expand=True, fill="both", padx=40, pady=20)

        ctk.CTkLabel(self.intercessor_frame, text="The Hidden Intercessor", font=("Arial", 16, "bold"), text_color="#4A148C").pack(pady=(20, 5))
        ctk.CTkLabel(self.intercessor_frame, text="Who do you feel superior to? Who are you in conflict with?", font=("Arial", 12), text_color="gray").pack(pady=(0, 20))

        # Initial Input
        self.input_frame = ctk.CTkFrame(self.intercessor_frame, fg_color="transparent")
        self.input_frame.pack(pady=10)
        
        ctk.CTkLabel(self.input_frame, text="Initials:", font=("Arial", 14)).pack(side="left", padx=10)
        self.initials_entry = ctk.CTkEntry(self.input_frame, width=60, font=("Arial", 14), justify="center")
        self.initials_entry.pack(side="left", padx=10)

        self.pray_btn = ctk.CTkButton(
            self.intercessor_frame, 
            text="Begin Intercession", 
            fg_color="#4A148C", 
            hover_color="#6A1B9A",
            command=self.show_prayer_prompt
        )
        self.pray_btn.pack(pady=20)
        
        # Prayer Prompt (Hidden initially)
        self.prayer_display = ctk.CTkLabel(self.intercessor_frame, text="", font=("Times New Roman", 18, "italic"), wraplength=400, text_color="gray")
        self.prayer_display.pack(pady=20)
        
        self.finish_btn = ctk.CTkButton(self.intercessor_frame, text="I have prayed this.", state="disabled", fg_color="gray", command=self.finish_prayer)
        self.finish_btn.pack(pady=(0, 20))

    def show_prayer_prompt(self):
        initials = self.initials_entry.get().upper()
        if not initials: return
        
        self.initials_entry.configure(state="disabled")
        self.pray_btn.configure(state="disabled", text="Praying...")
        
        prayer = f"\"Lord, I lift up {initials} to You.\nBless them with the success I desire for myself.\nGrant them peace, joy, and prosperity.\nGuard them from the very pride I struggle with.\nAmen.\""
        
        self.prayer_display.configure(text=prayer, text_color="#4A148C")
        self.finish_btn.configure(state="normal", fg_color="#2E7D32")

    def finish_prayer(self):
        self.prayer_display.configure(text="Your heart is softer now.", text_color="#2E7D32")
        self.finish_btn.configure(state="disabled", text="Amen")
