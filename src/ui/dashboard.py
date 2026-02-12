import customtkinter as ctk
import random
from datetime import datetime

# --- Imports: The Holy Vessels (Widgets) ---
from src.ui.widgets.holy_card import HolyCard
from src.ui.widgets.verse_display import VerseDisplay
from src.ui.widgets.prayer_button import PrayerButton

# --- Imports: The Arsenal (Modules) ---
from src.modules.pride.logic import PrideModule
from src.modules.anger.logic import AngerModule
from src.modules.lust.logic import LustModule
from src.modules.sloth.logic import SlothModule
from src.modules.greed.logic import GreedModule

from src.modules.gluttony.logic import GluttonyModule

class Dashboard(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        # White background for purity
        super().__init__(master, fg_color="#FAFAFA", **kwargs)

        # 1. Load the Active Battles
        self.active_modules = [
            PrideModule(),
            AngerModule(),
            LustModule(),
            SlothModule(),
            GreedModule(),
            GluttonyModule()
        ]

        # 2. Configure Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # Row 1 (Grid) takes expansion

        # 3. Build UI Sections
        self.build_header()
        self.build_module_grid()
        
        # 4. Trigger Daily Email Check
        self.after(2000, self.check_daily_email)

    def check_daily_email(self):
        """
        Checks if the user has opted into daily emails and if one has been sent today.
        If yes and no respectively, sends a curated scripture.
        """
        import json, os, threading
        from src.core.email_service import EmailService

        SETTINGS_FILE = "data/settings.json"
        LOG_FILE = "data/daily_log.json"
        
        # 1. Check Settings
        if not os.path.exists(SETTINGS_FILE):
            return
        
        try:
            with open(SETTINGS_FILE, "r") as f:
                settings = json.load(f)
                if not settings.get("daily_email_enabled", False):
                    return
                
                target = settings.get("target_email", "")
                sender = settings.get("sender_email", "")
                pwd = settings.get("sender_password", "")
                
                if not target: return
        except:
            return

        # 2. Check Log
        today_str = datetime.now().strftime("%Y-%m-%d")
        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, "r") as f:
                    log = json.load(f)
                    if log.get("last_sent") == today_str:
                        print("Daily email already sent today.")
                        return
            except:
                pass

        # 3. Send Email (Background)
        def send_task():
            manna = self.get_curated_manna()
            if not manna: return
            
            subject = f"Daily Manna - {datetime.now().strftime('%A, %B %d')}"
            body = f"\"{manna.text}\"\n\n{manna.reference}\n\n---\nSent from Sanctum"
            
            success = False
            msg = ""
            
            if sender and pwd:
                success, msg = EmailService.send_via_smtp(sender, pwd, target, subject, body)
            else:
                # If no SMTP creds but feature enabled, maybe just skip or warn?
                # The prompt implies "send a daily scripture", usually implies auto.
                # If only target is set, we can't auto-send without opening client which is disruptive on startup.
                # So we only proceed if SMTP is ready.
                print("Daily Email skipped: No SMTP credentials.")
                return

            if success:
                print("Daily email sent successfully.")
                # Update Log
                with open(LOG_FILE, "w") as f:
                    json.dump({"last_sent": today_str}, f)
            else:
                print(f"Daily email failed: {msg}")

        thread = threading.Thread(target=send_task)
        thread.start()

    def get_curated_manna(self):
        """
        The Shepherd Logic:
        Selects a random module from the active list, then asks that module 
        for a scripture. This ensures the verse matches a current struggle.
        """
        if not self.active_modules:
            return None
        
        # Pick a random module (e.g., Anger) and get its specific verse
        selected_module = random.choice(self.active_modules)
        return selected_module.get_daily_manna()

    def build_header(self):
        """Creates the top section with Date and Verse."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(40, 20))

        # Date Display
        date_label = ctk.CTkLabel(
            header_frame, 
            text=f"{datetime.now().strftime('%A, %B %d')}".upper(),
            font=("Arial", 12, "bold"),
            text_color="gray"
        )
        date_label.pack(pady=(0, 10))

        # Verse Display Widget
        # We initialize it here, then update it with data
        self.verse_display = VerseDisplay(header_frame)
        self.verse_display.pack()
        
        # Load the curated verse
        manna = self.get_curated_manna()
        self.verse_display.update_verse(manna)

        # Prayer Button (Call to Action)
        self.prayer_btn = PrayerButton(
            header_frame,
            text="Enter Prayer Mode",
            command=self.master.show_journal
        )
        self.prayer_btn.pack(pady=(15, 0))

    def build_module_grid(self):
        """Creates the grid of module cards."""
        grid_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        grid_frame.grid(row=1, column=0, sticky="nsew", padx=40)
        grid_frame.grid_columnconfigure((0, 1), weight=1) # 2 Equal Columns

        # Loop through modules and create HolyCards
        for i, module in enumerate(self.active_modules):
            card = HolyCard(
                master=grid_frame,
                icon_char=module.icon_char,
                title=module.title,
                color=module.theme_color,
                # on_click triggers open_module
                on_click=lambda m=module: self.open_module(m)
            )
            card.grid(row=i // 2, column=i % 2, padx=15, pady=15, sticky="ew")

        # Create the "Add New" button (Styled as a ghost card)
        idx = len(self.active_modules)
        self.create_add_button(grid_frame, idx)

    def create_add_button(self, parent, index):
        """Helper to create the 'Add New' placeholder button."""
        add_btn = ctk.CTkButton(
            parent,
            text="+ Add New",
            fg_color="#EEEEEE",
            text_color="gray",
            hover_color="#E0E0E0",
            corner_radius=15,
            height=120, 
            font=("Arial", 16),
            command=lambda: print("Add Clicked")
        )
        add_btn.grid(row=index // 2, column=index % 2, padx=15, pady=15, sticky="ew")

    def open_module(self, module):
        print(f"Opening {module.title}...")
        
        # Hide standard Dashboard content
        for child in self.winfo_children():
            child.pack_forget() if hasattr(child, 'pack_forget') else child.grid_forget()

        # Load Module View
        if module.id == "sin_lust":
            from src.modules.lust.view import LustView
            self.current_view = LustView(self, module, on_back=self.restore_dashboard)
            self.current_view.grid(row=0, column=0, rowspan=2, sticky="nsew")
        elif module.id == "sin_anger":
            from src.modules.anger.view import AngerView
            self.current_view = AngerView(self, module, on_back=self.restore_dashboard)
            self.current_view.grid(row=0, column=0, rowspan=2, sticky="nsew")
        elif module.id == "sin_sloth":
            from src.modules.sloth.view import SlothView
            self.current_view = SlothView(self, module, on_back=self.restore_dashboard)
            self.current_view.grid(row=0, column=0, rowspan=2, sticky="nsew")
        elif module.id == "sin_greed":
            from src.modules.greed.view import GreedView
            self.current_view = GreedView(self, module, on_back=self.restore_dashboard)
            self.current_view.grid(row=0, column=0, rowspan=2, sticky="nsew")
        elif module.id == "sin_pride":
            from src.modules.pride.view import PrideView
            self.current_view = PrideView(self, module, on_back=self.restore_dashboard)
            self.current_view.grid(row=0, column=0, rowspan=2, sticky="nsew")
        elif module.id == "sin_gluttony":
            from src.modules.gluttony.view import GluttonyView
            self.current_view = GluttonyView(self, module, on_back=self.restore_dashboard)
            self.current_view.grid(row=0, column=0, rowspan=2, sticky="nsew")
        # Add other modules here as we implement them
        else:
            # Placeholder for others
            frame = ctk.CTkFrame(self)
            frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
            ctk.CTkButton(frame, text="Back", command=self.restore_dashboard).pack(pady=20)
            ctk.CTkLabel(frame, text=f"Work in Progress: {module.title}").pack(expand=True)
            self.current_view = frame

    def restore_dashboard(self):
        if hasattr(self, 'current_view') and self.current_view:
            self.current_view.destroy()
        
        # Re-build/Re-show dashboard
        # Since we used grid/pack forget, we can just re-run init logic or simply re-grid.
        # But our init builds them fresh. Let's just rebuild for simplicity to ensure state reset.
        for child in self.winfo_children():
            child.destroy()
            
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.build_header()
        self.build_module_grid()