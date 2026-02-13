import customtkinter as ctk
from src.core.challenge_service import ChallengeService

class ChallengeView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="white", **kwargs)
        self.service = ChallengeService()
        
        # Title
        ctk.CTkLabel(self, text="The Ascetic Path", font=("Times New Roman", 24, "bold"), text_color="#1A237E").pack(pady=(20, 5))
        ctk.CTkLabel(self, text="Spiritual Exercises tailored to your struggle.", font=("Arial", 12), text_color="gray").pack(pady=(0, 20))

        # Scrollable Area for Multiple Challenges
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(expand=True, fill="both", padx=20, pady=10)

        self.refresh_ui()

    def refresh_ui(self):
        # Clear existing
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        challenges = self.service.get_active_challenges()

        if not challenges:
            ctk.CTkLabel(self.scroll_frame, text="No immediate burdens today.", font=("Arial", 16)).pack(pady=40)
            ctk.CTkLabel(self.scroll_frame, text="Rest in Grace.", text_color="gray").pack(pady=(0, 40))
            return

        for c in challenges:
            self._render_challenge_card(c)

    def _render_challenge_card(self, challenge):
        card = ctk.CTkFrame(self.scroll_frame, fg_color="#F3E5F5", corner_radius=15, border_width=1, border_color="#E1BEE7")
        card.pack(fill="x", padx=10, pady=10)

        # Header
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 5))
        
        status = challenge.get("status", "active")
        icon = "✅" if status == "completed" else "⚔️"
        
        # Special Icon for System/Permission
        if challenge.get("id") == "permission_grant":
             icon = "🔒"

        ctk.CTkLabel(header, text=icon, font=("Arial", 24)).pack(side="left")
        ctk.CTkLabel(header, text=challenge["title"], font=("Arial", 18, "bold"), text_color="#4A148C").pack(side="left", padx=10)

        # Body
        ctk.CTkLabel(card, text=challenge["desc"], font=("Arial", 14), text_color="#424242", wraplength=350, justify="left").pack(fill="x", padx=15, pady=5)

        # Action / Status
        if status == "completed":
            ctk.CTkLabel(card, text="Completed", font=("Arial", 12, "bold"), text_color="#2E7D32").pack(pady=(10, 15))
        else:
            btn_text = "Mark as Complete"
            btn_color = "#AB47BC"
            
            if challenge.get("id") == "permission_grant":
                btn_text = "Grant Permission"
                btn_color = "#1565C0"

            ctk.CTkButton(
                card, 
                text=btn_text, 
                fg_color=btn_color,
                hover_color="#7B1FA2",
                height=32,
                command=lambda cid=challenge["id"]: self.on_complete(cid)
            ).pack(pady=(10, 15), padx=15, fill="x")

    def on_complete(self, challenge_id):
        if self.service.complete_challenge(challenge_id):
            self.refresh_ui()
