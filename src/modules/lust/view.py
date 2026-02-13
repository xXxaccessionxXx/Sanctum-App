import customtkinter as ctk
import random
import time
import threading

class LustView(ctk.CTkFrame):
    def __init__(self, master, module, on_back=None, **kwargs):
        super().__init__(master, **kwargs)
        self.module = module
        self.on_back = on_back
        self.is_active = False
        self.current_activity = None
        self.duration_seconds = 0

        # Log Usage
        from src.core.stats_service import StatsService
        StatsService().log_module_entry("lust")
        
        # --- Header ---
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=20)
        
        self.back_btn = ctk.CTkButton(self.header, text="← Back", width=60, fg_color="transparent", text_color="gray", hover_color="#EEEEEE", command=self.on_back)
        self.back_btn.pack(side="left")
        
        title = ctk.CTkLabel(self.header, text=f"{module.icon_char} {module.title}", font=("Arial", 24, "bold"), text_color="#1565C0")
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
        ctk.CTkLabel(self.content_frame, text="Choose your weapon:", font=("Arial", 18, "bold"), text_color="#1565C0").pack(pady=(10, 20))

        # List Activities
        for activity in self.module.get_activities():
            btn = ctk.CTkButton(
                self.content_frame, 
                text=f"{activity.title}\n{activity.description}", 
                font=("Arial", 14), 
                fg_color="white", 
                text_color="#0D47A1",
                hover_color="#BBDEFB",
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

        ctk.CTkLabel(self.activity_frame, text=activity.title, font=("Arial", 16, "bold"), text_color="#1565C0").pack(pady=(20, 5))
        ctk.CTkLabel(self.activity_frame, text=activity.description, font=("Arial", 12), text_color="gray").pack(pady=(0, 20))

        if activity.id == "lust_flight":
            self._build_panic_ui()
        else:
            self._build_timer_ui()

    def _build_panic_ui(self):
         # The original Panic Button logic for "Flee & Pray"
        ctk.CTkLabel(self.activity_frame, text="TEMPTATION DETECTED?", font=("Arial", 16, "bold"), text_color="#D32F2F").pack(pady=(10, 5))
        
        self.panic_btn = ctk.CTkButton(
            self.activity_frame,
            text="ACTIVATE PANIC PROTOCOL",
            fg_color="#D32F2F",
            hover_color="#B71C1C",
            height=60,
            font=("Arial", 16, "bold"),
            command=self.activate_panic_overlay
        )
        self.panic_btn.pack(pady=20)

    def activate_panic_overlay(self):
        # Create a full-screen overlay window
        self.overlay = ctk.CTkToplevel(self)
        self.overlay.title("COGNITIVE INTERRUPT")
        # Fullscreen handling
        self.overlay.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        self.overlay.attributes("-topmost", True)
        self.overlay.overrideredirect(True) # Remove title bar
        self.overlay.configure(fg_color="#111111")
        
        # Grid layout for centering
        self.overlay.grid_columnconfigure(0, weight=1)
        self.overlay.grid_rowconfigure(0, weight=1)
        
        self.task_container = ctk.CTkFrame(self.overlay, fg_color="transparent")
        self.task_container.grid(row=0, column=0)
        
        self.generate_cognitive_task()

    def generate_cognitive_task(self):
        # Clear container
        for widget in self.task_container.winfo_children():
            widget.destroy()

        # Task: Math Problem
        a = random.randint(12, 99)
        b = random.randint(12, 99)
        self.correct_answer = a + b
        
        ctk.CTkLabel(self.task_container, text="SOLVE TO UNLOCK", font=("Arial", 30, "bold"), text_color="white").pack(pady=20)
        ctk.CTkLabel(self.task_container, text=f"{a} + {b} = ?", font=("Arial", 60, "bold"), text_color="#4FC3F7").pack(pady=40)
        
        self.ans_entry = ctk.CTkEntry(self.task_container, font=("Arial", 30), justify="center", width=200)
        self.ans_entry.pack(pady=20)
        self.ans_entry.bind("<Return>", self.check_answer)
        self.ans_entry.focus_set()
        
        self.status = ctk.CTkLabel(self.task_container, text="", font=("Arial", 16))
        self.status.pack(pady=20)

    def check_answer(self, event=None):
        try:
            val = int(self.ans_entry.get())
            if val == self.correct_answer:
                self.status.configure(text="ACCESS GRANTED. BREATHE.", text_color="#66BB6A")
                self.overlay.after(1000, self.cleanup_panic)
            else:
                self.status.configure(text="INCORRECT. TRY AGAIN.", text_color="#EF5350")
                self.ans_entry.delete(0, "end")
        except:
            pass

    def cleanup_panic(self):
        self.overlay.destroy()
        self.back_btn.configure(state="normal", text="← Back", fg_color="transparent")
        self.panic_btn.configure(text="SESSION COMPLETE", state="disabled", fg_color="#2E7D32")

    def _build_timer_ui(self):
         # Daily Manna
        scripture = self.module.get_daily_manna()
        ctk.CTkLabel(self.activity_frame, text=f'"{scripture.text}"', font=("Times New Roman", 18, "italic"), wraplength=400, text_color="#1565C0").pack(pady=(10, 5))
        ctk.CTkLabel(self.activity_frame, text=scripture.reference, font=("Arial", 10, "bold"), text_color="gray").pack(pady=(0, 15))

        self.start_btn = ctk.CTkButton(
            self.activity_frame, 
            text="Begin", 
            fg_color="#1565C0", 
            hover_color="#0D47A1",
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
            self.status_label.configure(text="Completed. Stand firm.", text_color="#2E7D32")
            self.start_btn.configure(text="Finished", fg_color="#2E7D32")
            self.back_btn.configure(state="normal", text="← Back", fg_color="transparent")
            self.is_active = False
        else:
            self.status_label.configure(text=f"Time remaining... {int((1-progress)*100)}%")
