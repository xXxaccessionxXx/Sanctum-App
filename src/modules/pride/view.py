import customtkinter as ctk
import time
import threading

class PrideView(ctk.CTkFrame):
    def __init__(self, master, module, on_back=None, **kwargs):
        super().__init__(master, fg_color="#F3E5F5", **kwargs) # Light Purple
        self.module = module
        self.on_back = on_back
        self.is_active = False
        self.current_activity = None
        self.duration_seconds = 0

        # Log Usage
        from src.core.stats_service import StatsService
        StatsService().log_module_entry("pride")

        # --- Header ---
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=20)
        
        self.back_btn = ctk.CTkButton(self.header, text="← Back", width=60, fg_color="transparent", text_color="gray", hover_color="#E1BEE7", command=self.on_back)
        self.back_btn.pack(side="left")
        
        title = ctk.CTkLabel(self.header, text=f"{module.icon_char} {module.title}", font=("Arial", 24, "bold"), text_color="#4A148C")
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
        ctk.CTkLabel(self.content_frame, text="Choose your path to humility:", font=("Arial", 18, "bold"), text_color="#4A148C").pack(pady=(10, 20))

        # List Activities
        for activity in self.module.get_activities():
            btn = ctk.CTkButton(
                self.content_frame, 
                text=f"{activity.title}\n{activity.description}", 
                font=("Arial", 14), 
                fg_color="white", 
                text_color="#4A148C",
                hover_color="#E1BEE7",
                height=60,
                command=lambda a=activity: self.start_activity(a)
            )
            btn.pack(fill="x", padx=40, pady=10)

    def start_activity(self, activity):
        self.current_activity = activity
        self.duration_seconds = activity.duration_minutes * 60
        self.is_active = False
        
        # Clear Menu
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Lock Back Button
        self.back_btn.configure(state="disabled", text="Locked", fg_color="gray")

        # --- Activity UI ---
        self.activity_frame = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=20)
        self.activity_frame.pack(expand=True, fill="both", padx=40, pady=20)

        ctk.CTkLabel(self.activity_frame, text=activity.title, font=("Arial", 16, "bold"), text_color="#4A148C").pack(pady=(20, 5))
        ctk.CTkLabel(self.activity_frame, text=activity.description, font=("Arial", 12), text_color="gray").pack(pady=(0, 20))

        if activity.id == "pride_litany":
            self._build_prayer_ui()
        else:
            self._build_timer_ui()

    def _build_prayer_ui(self):
        # Litany Logic
        self.initials_entry = ctk.CTkEntry(self.activity_frame, placeholder_text="Initials of someone better than you...", width=250, font=("Arial", 14))
        self.initials_entry.pack(pady=10)

        self.start_btn = ctk.CTkButton(
            self.activity_frame, 
            text="Begin Prayer", 
            fg_color="#4A148C", 
            hover_color="#6A1B9A",
            command=self.show_prayer_text
        )
        self.start_btn.pack(pady=20)
        
        self.text_display = ctk.CTkLabel(self.activity_frame, text="", font=("Times New Roman", 18, "italic"), wraplength=400, text_color="gray")
        self.text_display.pack(pady=20)

    def show_prayer_text(self):
        initials = self.initials_entry.get().upper()
        if not initials: 
            initials = "THEM" # Fallback
            
        prayer = f"\"Lord, deliver me from the desire of being estimated. Deliver me from the fear of being humiliated. Let {initials} be increased, and I decreased.\""
        
        self.text_display.configure(text=prayer, text_color="#4A148C")
        self.start_btn.configure(text="Amen", fg_color="#2E7D32", command=self.finish_activity)
        self.initials_entry.configure(state="disabled")

    def _build_timer_ui(self):
         # Daily Manna
        scripture = self.module.get_daily_manna()
        ctk.CTkLabel(self.activity_frame, text=f'"{scripture.text}"', font=("Times New Roman", 18, "italic"), wraplength=400, text_color="#4A148C").pack(pady=(10, 5))
        ctk.CTkLabel(self.activity_frame, text=scripture.reference, font=("Arial", 10, "bold"), text_color="gray").pack(pady=(0, 15))

        self.start_btn = ctk.CTkButton(
            self.activity_frame, 
            text="Begin", 
            fg_color="#4A148C", 
            hover_color="#6A1B9A",
            command=self.start_timer
        )
        self.start_btn.pack(pady=20)
        
        self.status_label = ctk.CTkLabel(self.activity_frame, text="", font=("Arial", 12), text_color="gray")
        self.status_label.pack(pady=5)

    def start_timer(self):
        if self.is_active: return
        self.is_active = True
        
        self.start_btn.configure(state="disabled", text="In Progress...")
        t = threading.Thread(target=self._run_timer)
        t.start()
        
    def _run_timer(self):
        steps = 100
        for i in range(steps + 1):
            if not self.winfo_exists(): return
            time.sleep(self.duration_seconds / steps)
            progress = i / steps
            self.after(0, self._update_ui, progress)
            
    def _update_ui(self, progress):
        if progress >= 1.0:
            self.status_label.configure(text="Completed. Walk humbly.", text_color="#2E7D32")
            self.finish_activity()
        else:
            self.status_label.configure(text=f"Time remaining... {int((1-progress)*100)}%")

    def finish_activity(self):
        self.is_active = False
        self.start_btn.configure(text="Finished", fg_color="#2E7D32", state="disabled")
        self.back_btn.configure(state="normal", text="← Back", fg_color="transparent")
