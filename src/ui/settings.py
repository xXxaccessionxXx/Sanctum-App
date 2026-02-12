import customtkinter as ctk

class SettingsView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="white", **kwargs)
        
        self.label = ctk.CTkLabel(
            self, 
            text="Settings", 
            font=("Times New Roman", 24, "bold"),
            text_color="#1A237E"
        )
        self.label.pack(pady=20, padx=20, anchor="w")

        # Example Toggle: Notifications
        self.switch_notif = ctk.CTkSwitch(self, text="Discrete Notifications")
        self.switch_notif.pack(pady=10, padx=20, anchor="w")
        
        # Example Toggle: Dark Mode (For late night prayer)
        self.switch_theme = ctk.CTkSwitch(
            self, 
            text="Dark Mode (Night Vigil)", 
            command=self.toggle_theme
        )
        self.switch_theme.pack(pady=10, padx=20, anchor="w")

        # --- Email Automation Settings ---
        self.email_frame = ctk.CTkFrame(self, fg_color="#F5F5F5")
        self.email_frame.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(self.email_frame, text="Email Automation", font=("Arial", 16, "bold"), text_color="#1A237E").pack(anchor="w", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(self.email_frame, text="Target Email (Receive Prayers Here):", text_color="gray").pack(anchor="w", padx=10)
        self.target_email = ctk.CTkEntry(self.email_frame, width=300, placeholder_text="e.g. my.email@example.com")
        self.target_email.pack(anchor="w", padx=10, pady=(0, 10))

        # Advanced
        ctk.CTkLabel(self.email_frame, text="sender Settings (Optional - For Auto-Send):", text_color="gray", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
        
        ctk.CTkLabel(self.email_frame, text="Your Gmail:", text_color="gray").pack(anchor="w", padx=10)
        self.sender_email = ctk.CTkEntry(self.email_frame, width=300, placeholder_text="your.gmail@gmail.com")
        self.sender_email.pack(anchor="w", padx=10, pady=(0, 5))

        ctk.CTkLabel(self.email_frame, text="App Password:", text_color="gray").pack(anchor="w", padx=10)
        self.sender_password = ctk.CTkEntry(self.email_frame, width=300, placeholder_text="Google App Password", show="*")
        self.sender_password.pack(anchor="w", padx=10, pady=(0, 10))

        # Daily Email Toggle
        self.daily_switch = ctk.CTkSwitch(self.email_frame, text="Receive Daily Scripture Email")
        # --- Audio Settings ---
        audio_label = ctk.CTkLabel(self.email_frame, text="Audio & Atmosphere", font=("Arial", 14, "bold"), text_color="gray")
        audio_label.pack(anchor="w", padx=10, pady=(20, 5))

        self.mute_switch = ctk.CTkSwitch(self.email_frame, text="Mute Background Music", command=self.toggle_mute)
        self.mute_switch.pack(anchor="w", padx=10, pady=(0, 10))

        self.daily_switch.pack(anchor="w", padx=10, pady=(10, 0))

        self.save_btn = ctk.CTkButton(self.email_frame, text="Save Settings", command=self.save_settings)
        self.save_btn.pack(anchor="e", padx=10, pady=10)

        self.load_settings()

    def toggle_mute(self):
        try:
            from src.core.music_service import MusicService
            ms = MusicService()
            is_muted = ms.toggle_mute()
            # Identify: Update UI text if needed? 'Muted' vs 'Playing'
        except ImportError:
            pass

    def load_settings(self):
        import json, os
        if os.path.exists("data/settings.json"):
            with open("data/settings.json", "r") as f:
                data = json.load(f)
                self.target_email.insert(0, data.get("target_email", ""))
                self.sender_email.insert(0, data.get("sender_email", ""))
                self.sender_password.insert(0, data.get("sender_password", ""))
                if data.get("daily_email_enabled", False):
                    self.daily_switch.select()
                else:
                    self.daily_switch.deselect()

                # Sync Mute State if persisted (Optional)
                # For now, just sync with Service if running
                try:
                    from src.core.music_service import MusicService
                    ms = MusicService()
                    if ms.is_muted:
                        self.mute_switch.select()
                    else:
                        self.mute_switch.deselect()
                except:
                    pass

    def save_settings(self):
        import json
        data = {
            "target_email": self.target_email.get(),
            "sender_email": self.sender_email.get(),
            "sender_password": self.sender_password.get(),
            "daily_email_enabled": bool(self.daily_switch.get())
        }
        with open("data/settings.json", "w") as f:
            json.dump(data, f, indent=4)
        print("Settings Saved")

    def toggle_theme(self):
        if self.switch_theme.get() == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")