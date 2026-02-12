import customtkinter as ctk
import time
import threading

class SlothView(ctk.CTkFrame):
    def __init__(self, master, module, on_back=None, **kwargs):
        super().__init__(master, fg_color="#FFF3E0", **kwargs) # Light Orange
        self.module = module
        self.on_back = on_back
        self.work_time = 25 * 60 # 25 Minutes
        self.is_working = False

        # --- Header ---
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=20)
        
        back_btn = ctk.CTkButton(self.header, text="← Back", width=60, fg_color="transparent", text_color="gray", hover_color="#FFE0B2", command=self.on_back)
        back_btn.pack(side="left")
        
        title = ctk.CTkLabel(self.header, text=f"{module.icon_char} {module.title}", font=("Arial", 24, "bold"), text_color="#E65100")
        title.pack(side="left", padx=20)

        # --- The Offering Altar ---
        self.altar_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        self.altar_frame.pack(expand=True, fill="both", padx=40, pady=20)

        ctk.CTkLabel(self.altar_frame, text="The Offering Timer", font=("Arial", 16, "bold"), text_color="#E65100").pack(pady=(20, 5))
        ctk.CTkLabel(self.altar_frame, text="What work will you offer to God?", font=("Arial", 12), text_color="gray").pack(pady=(0, 20))

        self.task_entry = ctk.CTkEntry(self.altar_frame, placeholder_text="I will build/write/clean...", width=300, font=("Arial", 14))
        self.task_entry.pack(pady=10)

        self.timer_label = ctk.CTkLabel(self.altar_frame, text="25:00", font=("Arial", 48, "bold"), text_color="#E65100")
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
        
        # Visual Metaphor (Simple Text for now, could be an ASCII wall)
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
        for i in range(total_seconds, -1, -1):
            if not self.winfo_exists(): return
            
            # Format time
            mins, secs = divmod(i, 60)
            time_str = f"{mins:02}:{secs:02}"
            
            # Visual update (Build a wall)
            # Every 5 mins (300s), add a brick
            bricks = (self.work_time - i) // 300
            wall = "🧱" * bricks
            
            self.after(0, self._update_ui, time_str, wall)
            time.sleep(1)

        self.after(0, self._finish_work)

    def _update_ui(self, time_str, wall):
        self.timer_label.configure(text=time_str)
        self.visual_label.configure(text=wall)

    def _finish_work(self):
        self.timer_label.configure(text="Finished!", text_color="#2E7D32")
        self.start_btn.configure(text="Offering Accepted", fg_color="#2E7D32")
