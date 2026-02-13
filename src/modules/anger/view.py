import customtkinter as ctk
import time
import threading

class AngerView(ctk.CTkFrame):
    def __init__(self, master, module, on_back=None, **kwargs):
        super().__init__(master, fg_color="#FFEBEE", **kwargs) # Light Red
        self.module = module
        self.on_back = on_back
        self.duration_seconds = 60 
        self.is_active = False
        self.current_activity = None

        # Log Usage
        from src.core.stats_service import StatsService
        StatsService().log_module_entry("anger")

        # --- Header ---
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=20)
        
        self.back_btn = ctk.CTkButton(self.header, text="← Back", width=60, fg_color="transparent", text_color="gray", hover_color="#FFCDD2", command=self.on_back)
        self.back_btn.pack(side="left")
        
        title = ctk.CTkLabel(self.header, text=f"{module.icon_char} {module.title}", font=("Arial", 24, "bold"), text_color="#B71C1C")
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
        ctk.CTkLabel(self.content_frame, text="Choose your path to peace:", font=("Arial", 18, "bold"), text_color="#B71C1C").pack(pady=(10, 20))

        # List Activities
        for activity in self.module.get_activities():
            btn = ctk.CTkButton(
                self.content_frame, 
                text=f"{activity.title}\n{activity.description}", 
                font=("Arial", 14), 
                fg_color="white", 
                text_color="#B71C1C",
                hover_color="#FFCDD2",
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

        # --- Activity Area ---
        self.activity_frame = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=20)
        self.activity_frame.pack(expand=True, fill="both", padx=40, pady=20)

        ctk.CTkLabel(self.activity_frame, text=activity.title, font=("Arial", 16, "bold"), text_color="#B71C1C").pack(pady=(20, 5))
        ctk.CTkLabel(self.activity_frame, text=activity.description, font=("Arial", 12), text_color="gray").pack(pady=(0, 10))

        # Specialized UI for "Cooling Chamber" vs others
        if activity.id == "anger_cool_down" or activity.id == "anger_journal":
             self._build_journal_ui()
        else:
             self._build_timer_ui()

    def _build_journal_ui(self):
        self.textbox = ctk.CTkTextbox(self.activity_frame, font=("Arial", 14), wrap="word", height=200)
        self.textbox.pack(fill="x", padx=20, pady=10)
        self.textbox.insert("0.0", "Write it all down here...")
        
        self.start_btn = ctk.CTkButton(
            self.activity_frame, 
            text="Start Cooling Phase", 
            fg_color="#B71C1C", 
            hover_color="#D32F2F",
            command=self.start_timer
        )
        self.start_btn.pack(pady=20)
        
        self.status_label = ctk.CTkLabel(self.activity_frame, text="", font=("Arial", 12), text_color="gray")
        self.status_label.pack(pady=5)

    def _build_timer_ui(self):
        # Daily Manna for prayer/reflection activities
        scripture = self.module.get_daily_manna()
        ctk.CTkLabel(self.activity_frame, text=f'"{scripture.text}"', font=("Times New Roman", 18, "italic"), wraplength=400, text_color="#B71C1C").pack(pady=(10, 5))
        ctk.CTkLabel(self.activity_frame, text=scripture.reference, font=("Arial", 10, "bold"), text_color="gray").pack(pady=(0, 15))

        self.start_btn = ctk.CTkButton(
            self.activity_frame, 
            text="Begin", 
            fg_color="#B71C1C", 
            hover_color="#D32F2F",
            command=self.start_timer
        )
        self.start_btn.pack(pady=20)
        
        self.status_label = ctk.CTkLabel(self.activity_frame, text="", font=("Arial", 12), text_color="gray")
        self.status_label.pack(pady=5)

    def start_timer(self):
        if self.is_active: return
        self.is_active = True
        
        self.start_btn.configure(state="disabled", text="In Progress...")
        if hasattr(self, 'textbox'):
             self.textbox.configure(state="normal") # Keep editable for journaling
        
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
            self.status_label.configure(text="Completed. Peace be with you.", text_color="#2E7D32")
            self.start_btn.configure(text="Finished", fg_color="#2E7D32")
            self.back_btn.configure(state="normal", text="← Back", fg_color="transparent")
            
            if hasattr(self, 'textbox'):
                 self.textbox.configure(state="disabled") # Lock log after done
            
            self.is_active = False
        else:
            self.status_label.configure(text=f"Time remaining... {int((1-progress)*100)}%")
