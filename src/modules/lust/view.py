import customtkinter as ctk
import random
import time

class LustView(ctk.CTkFrame):
    def __init__(self, master, module, on_back=None, **kwargs):
        super().__init__(master, **kwargs)
        self.module = module
        self.on_back = on_back
        # self.logic = PanicButtonLogic() # Removed

        # Log Usage
        from src.core.stats_service import StatsService
        StatsService().log_module_entry("lust")
        
        # UI Elements

        # --- Header ---
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=20)
        
        back_btn = ctk.CTkButton(self.header, text="← Back", width=60, fg_color="transparent", text_color="gray", hover_color="#EEEEEE", command=self.on_back)
        back_btn.pack(side="left")
        
        title = ctk.CTkLabel(self.header, text=f"{module.icon_char} {module.title}", font=("Arial", 24, "bold"), text_color="#1565C0")
        title.pack(side="left", padx=20)

        # --- Daily Manna ---
        manna_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=15, border_width=1, border_color="#E0E0E0")
        manna_frame.pack(fill="x", padx=40, pady=(0, 30))
        
        scripture = module.get_daily_manna()
        ctk.CTkLabel(manna_frame, text="Daily Anchor", font=("Arial", 10, "bold"), text_color="gray").pack(pady=(10, 5))
        ctk.CTkLabel(manna_frame, text=f'"{scripture.text}"', font=("Times New Roman", 18, "italic"), wraplength=400).pack(pady=(0, 5))
        ctk.CTkLabel(manna_frame, text=scripture.reference, font=("Arial", 10, "bold"), text_color="#1565C0").pack(pady=(0, 15))

        # --- The Panic Button ---
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.pack(expand=True, fill="both", padx=40, pady=20)

        ctk.CTkLabel(self.action_frame, text="TEMPTATION DETECTED?", font=("Arial", 16, "bold"), text_color="#D32F2F").pack(pady=(20, 10))
        ctk.CTkLabel(self.action_frame, text="Disrupt the loop immediately.", font=("Arial", 12), text_color="gray").pack(pady=(0, 20))

        self.panic_btn = ctk.CTkButton(
            self.action_frame,
            text="PANIC BUTTON",
            fg_color="#D32F2F",
            hover_color="#B71C1C",
            height=80,
            font=("Arial", 20, "bold"),
            command=self.activate_panic_mode
        )
        self.panic_btn.pack(fill="x", padx=40)

    def activate_panic_mode(self):
        # Create a full-screen overlay window
        self.overlay = ctk.CTkToplevel(self)
        self.overlay.title("COGNITIVE INTERRUPT")
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
                self.overlay.after(1500, self.overlay.destroy)
            else:
                self.status.configure(text="INCORRECT. TRY AGAIN.", text_color="#EF5350")
                self.ans_entry.delete(0, "end")
        except:
            pass
