import customtkinter as ctk
import time
import threading

class SlothView(ctk.CTkFrame):
    def __init__(self, master, module, on_back=None, **kwargs):
        super().__init__(master, fg_color="#FFF3E0", **kwargs) # Light Orange
        self.module = module
        self.on_back = on_back
        self.work_time = 25 * 60 # Default
        self.is_working = False
        self.current_activity = None

        # Log Usage
        from src.core.stats_service import StatsService
        StatsService().log_module_entry("sloth")

        # --- Header ---
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=20)
        
        self.back_btn = ctk.CTkButton(self.header, text="← Back", width=60, fg_color="transparent", text_color="gray", hover_color="#FFE0B2", command=self.on_back)
        self.back_btn.pack(side="left")
        
        title = ctk.CTkLabel(self.header, text=f"{module.icon_char} {module.title}", font=("Arial", 24, "bold"), text_color="#E65100")
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
        ctk.CTkLabel(self.content_frame, text="Choose your offering:", font=("Arial", 18, "bold"), text_color="#E65100").pack(pady=(10, 20))

        # List Activities
        for activity in self.module.get_activities():
            btn = ctk.CTkButton(
                self.content_frame, 
                text=f"{activity.title}\n{activity.description}", 
                font=("Arial", 14), 
                fg_color="white", 
                text_color="#E65100",
                hover_color="#FFE0B2",
                height=60,
                command=lambda a=activity: self.start_activity(a)
            )
            btn.pack(fill="x", padx=40, pady=10)

    def start_activity(self, activity):
        self.current_activity = activity
        self.work_time = activity.duration_minutes * 60
        self.is_working = False # Reset state
        
        # Clear Menu
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Lock Back Button
        self.back_btn.configure(state="disabled", text="Locked", fg_color="gray")

        # --- The Offering Altar ---
        self.altar_frame = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=20)
        self.altar_frame.pack(expand=True, fill="both", padx=40, pady=20)

        ctk.CTkLabel(self.altar_frame, text=activity.title, font=("Arial", 16, "bold"), text_color="#E65100").pack(pady=(20, 5))
        ctk.CTkLabel(self.altar_frame, text=activity.description, font=("Arial", 12), text_color="gray").pack(pady=(0, 20))

        self.task_entry = ctk.CTkEntry(self.altar_frame, placeholder_text="Describe your offering...", width=300, font=("Arial", 14))
        self.task_entry.pack(pady=10)

        # Timer format
        mins = activity.duration_minutes
        self.timer_label = ctk.CTkLabel(self.altar_frame, text=f"{mins:02}:00", font=("Arial", 48, "bold"), text_color="#E65100")
        self.timer_label.pack(pady=20)

        self.start_btn = ctk.CTkButton(
            self.altar_frame, 
            text="Dedicate & Start", 
            fg_color="#E65100", 
            hover_color="#EF6C00",
            font=("Arial", 16, "bold"),
            height=40,
            command=self.start_timer
        )
        self.start_btn.pack(pady=20)
        
        self.visual_label = ctk.CTkLabel(self.altar_frame, text="", font=("Courier", 12), text_color="#EF6C00")
        self.visual_label.pack(pady=20)

    def start_timer(self):
        task = self.task_entry.get()
        if not task: return
        
        if self.is_working: return
        self.is_working = True
        
        self.task_entry.configure(state="disabled")
        self.start_btn.configure(state="disabled", text="Working for the Lord...")
        
        t = threading.Thread(target=self._run_timer)
        t.start()
        
    def _run_timer(self):
        total_seconds = self.work_time
        # Simplified loop for thread safety check
        for i in range(total_seconds, -1, -1):
            if not self.winfo_exists(): return
            
            # Format time
            mins, secs = divmod(i, 60)
            time_str = f"{mins:02}:{secs:02}"
            
            # Visual update (Build a wall)
            # Just a simple visual progression based on %
            if self.work_time > 0:
                progress = (self.work_time - i) / self.work_time
            else:
                progress = 1.0
                
            bricks = int(progress * 10) # 10 bricks total
            wall = "🧱" * bricks
            
            self.after(0, self._update_ui, time_str, wall)
            
            # Sleep a bit faster for testing if needed, but 1s is standard
            time.sleep(1) 
            
        self.after(0, self._finish_work)
        
    def _update_ui(self, time_str, wall):
        self.timer_label.configure(text=time_str)
        self.visual_label.configure(text=wall)
        
    def _finish_work(self):
        self.timer_label.configure(text="Finished!", text_color="#2E7D32")
        self.start_btn.configure(text="Offering Accepted", fg_color="#2E7D32")
        self.back_btn.configure(state="normal", text="← Back", fg_color="transparent")
        self.is_working = False
