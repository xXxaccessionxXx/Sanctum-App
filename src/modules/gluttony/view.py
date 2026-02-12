import customtkinter as ctk
import time
import threading
from src.core.stats_service import StatsService

class GluttonyView(ctk.CTkFrame):
    def __init__(self, master, module, on_back=None, **kwargs):
        super().__init__(master, fg_color="#EFEBE9", **kwargs) # Light Brown
        self.module = module
        self.on_back = on_back
        self.wait_time = 60 # 60 Seconds
        self.is_feasting = False

        # Log Usage
        StatsService().log_module_entry("gluttony")

        # --- Header ---
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=20)
        
        # Locked Back Button
        self.back_btn = ctk.CTkButton(self.header, text="Locked", width=60, state="disabled", fg_color="gray", command=self.on_back)
        self.back_btn.pack(side="left")
        
        title = ctk.CTkLabel(self.header, text=f"{module.icon_char} {module.title}", font=("Arial", 24, "bold"), text_color="#5D4037")
        title.pack(side="left", padx=20)

        # --- The Manna Portion ---
        self.manna_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        self.manna_frame.pack(expand=True, fill="both", padx=40, pady=20)

        ctk.CTkLabel(self.manna_frame, text="The Manna Portion", font=("Arial", 16, "bold"), text_color="#5D4037").pack(pady=(20, 5))
        ctk.CTkLabel(self.manna_frame, text="Feast on this Word before you eat.", font=("Arial", 12), text_color="gray").pack(pady=(0, 20))

        # Scripture Display (Large)
        scripture = module.get_daily_manna()
        self.verse_text = ctk.CTkLabel(self.manna_frame, text=f'"{scripture.text}"', font=("Times New Roman", 22, "italic"), wraplength=500, text_color="#3E2723")
        self.verse_text.pack(pady=10)
        
        ctk.CTkLabel(self.manna_frame, text=scripture.reference, font=("Arial", 12, "bold"), text_color="#5D4037").pack(pady=(0, 30))

        # Progress
        self.progress = ctk.CTkProgressBar(self.manna_frame, orientation="horizontal", mode="determinate", progress_color="#5D4037")
        self.progress.pack(fill="x", padx=60, pady=10)
        self.progress.set(0)
        
        self.status = ctk.CTkLabel(self.manna_frame, text="Read slowly...", font=("Arial", 14), text_color="gray")
        self.status.pack(pady=10)
        
        # Auto-start timer
        self.start_feasting()

    def start_feasting(self):
        if self.is_feasting: return
        self.is_feasting = True
        t = threading.Thread(target=self._run_timer)
        t.start()
        
    def _run_timer(self):
        steps = 100
        for i in range(steps + 1):
            if not self.winfo_exists(): return
            time.sleep(self.wait_time / steps)
            progress = i / steps
            self.after(0, self._update_ui, progress)
            
    def _update_ui(self, progress):
        self.progress.set(progress)
        if progress >= 1.0:
            self.status.configure(text="You are nourished.", text_color="#2E7D32")
            self.back_btn.configure(state="normal", text="← Back", fg_color="transparent", text_color="gray", hover_color="#D7CCC8")
