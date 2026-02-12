import customtkinter as ctk
from src.core.challenge_service import ChallengeService

class ChallengeView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="white", **kwargs)
        self.service = ChallengeService()
        
        # Title
        ctk.CTkLabel(self, text="The Ascetic Path", font=("Times New Roman", 24, "bold"), text_color="#1A237E").pack(pady=20)
        ctk.CTkLabel(self, text="Spiritual Exercises tailored to your struggle.", font=("Arial", 12), text_color="gray").pack(pady=(0, 20))

        # Challenge Card Area
        self.card_frame = ctk.CTkFrame(self, fg_color="#F3E5F5", corner_radius=15, border_width=1, border_color="#E1BEE7")
        self.card_frame.pack(fill="x", padx=40, pady=20)

        self.refresh_ui()

    def refresh_ui(self):
        # Clear card
        for widget in self.card_frame.winfo_children():
            widget.destroy()

        challenge = self.service.get_active_challenge()

        if not challenge:
            ctk.CTkLabel(self.card_frame, text="No active challenge today.", font=("Arial", 16)).pack(pady=40)
            ctk.CTkLabel(self.card_frame, text="Rest in Grace.", text_color="gray").pack(pady=(0, 40))
            return

        # Display Challenge
        status = challenge.get("status", "active")
        
        # Header (Icon + Title)
        header = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))
        
        icon = "✅" if status == "completed" else "⚔️"
        ctk.CTkLabel(header, text=icon, font=("Arial", 30)).pack(side="left")
        ctk.CTkLabel(header, text=challenge["title"], font=("Arial", 20, "bold"), text_color="#4A148C").pack(side="left", padx=15)

        # Description
        ctk.CTkLabel(self.card_frame, text=challenge["desc"], font=("Arial", 14), text_color="#424242", wraplength=400).pack(padx=20, pady=10)

        # Status / Action
        if status == "completed":
            ctk.CTkLabel(self.card_frame, text="Challenge Completed", font=("Arial", 16, "bold"), text_color="#2E7D32").pack(pady=(20, 10))
            
            # Completion Verse
            verse_text = "\"For the LORD sees not as man sees:\nman looks on the outward appearance,\nbut the LORD looks on the heart.\""
            ctk.CTkLabel(self.card_frame, text=verse_text, font=("Times New Roman", 16, "italic"), text_color="#4E342E").pack(pady=10)
            ctk.CTkLabel(self.card_frame, text="- 1 Samuel 16:7", font=("Arial", 12, "bold"), text_color="#5D4037").pack(pady=(0, 20))
        else:
            self.action_btn = ctk.CTkButton(
                self.card_frame, 
                text="Mark as Complete", 
                fg_color="#AB47BC", 
                hover_color="#8E24AA",
                command=self.on_complete
            )
            self.action_btn.pack(pady=20)

    def on_complete(self):
        if self.service.complete_challenge():
            self.refresh_ui()
