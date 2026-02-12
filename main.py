import customtkinter as ctk
from src.ui.dashboard import Dashboard
from src.ui.journal import JournalView
from src.ui.settings import SettingsView

# Visual Theology: Set the appearance mode
# "Light" represents clarity and truth.
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("dark-blue")

class SanctumApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. Window Config
        self.title("Sanctum")
        self.geometry("900x700") 
        
        # Grid Layout: 2 Columns (Sidebar | Main Content)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 2. Build Sidebar (Navigation)
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1) # Spacer at bottom

        # App Logo / Title
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="SANCTUM", 
            font=ctk.CTkFont(family="Times New Roman", size=24, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Nav Buttons
        self.btn_dashboard = self.create_nav_button("Dashboard", "🏠", 1, self.show_dashboard)
        self.btn_journal = self.create_nav_button("Journal", "📖", 2, self.show_journal)
        self.btn_community = self.create_nav_button("Community", "🔥", 3, self.show_community)
        self.btn_challenges = self.create_nav_button("Challenges", "⚔️", 4, self.show_challenges)
        self.btn_settings = self.create_nav_button("Settings", "⚙️", 5, self.show_settings)

        # 3. Initialize Views (The Rooms)
        self.dashboard_view = Dashboard(self)
        self.journal_view = JournalView(self)
        self.community_view = None # Lazy load
        self.challenge_view = None # Lazy load
        self.settings_view = SettingsView(self)

        # Show default view
        self.show_dashboard()

    def create_nav_button(self, text, icon, row, command):
        """Helper to create consistent sidebar buttons."""
        btn = ctk.CTkButton(
            self.sidebar_frame, 
            corner_radius=0, 
            height=40, 
            border_spacing=10, 
            text=f"{icon}  {text}",
            fg_color="transparent", 
            text_color=("gray10", "gray90"), 
            hover_color=("gray70", "gray30"),
            anchor="w", 
            command=command
        )
        btn.grid(row=row, column=0, sticky="ew")
        return btn

    def show_dashboard(self):
        self.select_view(self.dashboard_view)

    def show_journal(self):
        self.select_view(self.journal_view)

    def show_community(self):
        if not self.community_view:
            from src.ui.community import CommunityView
            self.community_view = CommunityView(self)
        self.select_view(self.community_view)

    def show_challenges(self):
        if not self.challenge_view:
            from src.ui.challenge_view import ChallengeView
            self.challenge_view = ChallengeView(self)
        else:
            # Refresh if already exists
            self.challenge_view.refresh_ui()
        self.select_view(self.challenge_view)

    def show_settings(self):
        self.select_view(self.settings_view)

    def select_view(self, view):
        # Hide all views first
        self.dashboard_view.grid_forget()
        self.journal_view.grid_forget()
        self.settings_view.grid_forget()
        if self.community_view: self.community_view.grid_forget()
        if self.challenge_view: self.challenge_view.grid_forget()
        
        # Show the selected one
        view.grid(row=0, column=1, sticky="nsew")

if __name__ == "__main__":
    app = SanctumApp()

    # --- Initialize Music Service (Safe) ---
    try:
        from src.core.music_service import MusicService
        MusicService().play_background_music("assets/background.mp3")
    except Exception as e:
        print(f"Music Init Disabled: {e}")

    app.mainloop()