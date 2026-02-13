import customtkinter as ctk
import time
import threading
from src.core.stats_service import StatsService

class GluttonyView(ctk.CTkFrame):
    def __init__(self, master, module, on_back=None, **kwargs):
        super().__init__(master, fg_color="#EFEBE9", **kwargs) # Light Brown
        self.module = module
        self.on_back = on_back
        self.wait_time = 60 # Default, will change per activity
        self.is_active = False
        self.current_activity = None

        # Log Usage
        StatsService().log_module_entry("gluttony")

        # --- Header ---
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=20)
        
        # Back Button (starts enabled, disabled during activity)
        self.back_btn = ctk.CTkButton(self.header, text="← Back", width=60, fg_color="transparent", text_color="gray", hover_color="#D7CCC8", command=self.on_back)
        self.back_btn.pack(side="left")
        
        title = ctk.CTkLabel(self.header, text=f"{module.icon_char} {module.title}", font=("Arial", 24, "bold"), text_color="#5D4037")
        title.pack(side="left", padx=20)

        # --- Content Area ---
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))

        # Show Menu Initially
        self.show_activity_menu()

    def show_activity_menu(self):
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.back_btn.configure(state="normal", text="← Back", fg_color="transparent")

        # Instructions
        ctk.CTkLabel(self.content_frame, text="Choose your discipline:", font=("Arial", 18, "bold"), text_color="#5D4037").pack(pady=(10, 20))

        # List Activities
        for activity in self.module.get_activities():
            btn = ctk.CTkButton(
                self.content_frame, 
                text=f"{activity.title}\n{activity.description}", 
                font=("Arial", 14), 
                fg_color="white", 
                text_color="#3E2723",
                hover_color="#D7CCC8",
                height=60,
                command=lambda a=activity: self.start_activity(a)
            )
            btn.pack(fill="x", padx=40, pady=10)

    def start_activity(self, activity):
        self.current_activity = activity
        self.wait_time = activity.duration_minutes * 60
        self.is_active = True
        
        # Clear Menu
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Lock Back Button
        self.back_btn.configure(state="disabled", text="Locked", fg_color="gray")

        # --- Activity UI ---
        self.manna_frame = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=20)
        self.manna_frame.pack(expand=True, fill="both", padx=40, pady=20)

        ctk.CTkLabel(self.manna_frame, text=activity.title, font=("Arial", 16, "bold"), text_color="#5D4037").pack(pady=(20, 5))
        ctk.CTkLabel(self.manna_frame, text=activity.description, font=("Arial", 12), text_color="gray").pack(pady=(0, 20))

        # Scripture Display (Large)
        scripture = self.module.get_daily_manna()
        self.verse_text = ctk.CTkLabel(self.manna_frame, text=f'"{scripture.text}"', font=("Times New Roman", 22, "italic"), wraplength=500, text_color="#3E2723")
        self.verse_text.pack(pady=10)
        
        ctk.CTkLabel(self.manna_frame, text=scripture.reference, font=("Arial", 12, "bold"), text_color="#5D4037").pack(pady=(0, 30))

        # Progress
        self.progress = ctk.CTkProgressBar(self.manna_frame, orientation="horizontal", mode="determinate", progress_color="#5D4037")
        self.progress.pack(fill="x", padx=60, pady=10)
        self.progress.set(0)
        
        self.status = ctk.CTkLabel(self.manna_frame, text="Begin...", font=("Arial", 14), text_color="gray")
        self.status.pack(pady=10)
        
        # Start Timer
        t = threading.Thread(target=self._run_timer)
        t.start()
        
    def _run_timer(self):
        steps = 100
        for i in range(steps + 1):
            if not self.winfo_exists(): return
            # Sleep a fraction of the total time
            # For testing, we might want to speed this up, but sticking to logic for now
            time.sleep(self.wait_time / steps)
            progress = i / steps
            self.after(0, self._update_ui, progress)
            
    def _update_ui(self, progress):
        self.progress.set(progress)
        if progress >= 1.0:
            self.status.configure(text="Completed.", text_color="#2E7D32")
            self.back_btn.configure(state="normal", text="← Back", fg_color="transparent", text_color="gray", hover_color="#D7CCC8")
            # Log completion if needed
            self.is_active = False
