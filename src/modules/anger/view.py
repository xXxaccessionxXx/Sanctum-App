import customtkinter as ctk
import time
import threading

class AngerView(ctk.CTkFrame):
    def __init__(self, master, module, on_back=None, **kwargs):
        super().__init__(master, fg_color="#FFEBEE", **kwargs) # Light Red Drawing from theme
        self.module = module
        self.on_back = on_back
        self.cooldown_seconds = 120 # 2 Minutes
        self.is_cooling = False

        # Log Usage
        from src.core.stats_service import StatsService
        StatsService().log_module_entry("anger")

        # --- Header ---
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=20)
        
        back_btn = ctk.CTkButton(self.header, text="← Back", width=60, fg_color="transparent", text_color="gray", hover_color="#FFCDD2", command=self.on_back)
        back_btn.pack(side="left")
        
        title = ctk.CTkLabel(self.header, text=f"{module.icon_char} {module.title}", font=("Arial", 24, "bold"), text_color="#B71C1C")
        title.pack(side="left", padx=20)

        # --- Daily Manna ---
        manna_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=15, border_width=1, border_color="#FFCDD2")
        manna_frame.pack(fill="x", padx=40, pady=(0, 20))
        
        scripture = module.get_daily_manna()
        ctk.CTkLabel(manna_frame, text="Daily Anchor", font=("Arial", 10, "bold"), text_color="gray").pack(pady=(10, 5))
        ctk.CTkLabel(manna_frame, text=f'"{scripture.text}"', font=("Times New Roman", 18, "italic"), wraplength=400).pack(pady=(0, 5))
        ctk.CTkLabel(manna_frame, text=scripture.reference, font=("Arial", 10, "bold"), text_color="#B71C1C").pack(pady=(0, 15))

        # --- The Cooling Chamber ---
        self.chamber_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        self.chamber_frame.pack(expand=True, fill="both", padx=40, pady=20)

        ctk.CTkLabel(self.chamber_frame, text="The Cooling Chamber", font=("Arial", 16, "bold"), text_color="#B71C1C").pack(pady=(20, 5))
        ctk.CTkLabel(self.chamber_frame, text="Vent here. Say everything. But wait before you act.", font=("Arial", 12), text_color="gray").pack(pady=(0, 10))

        self.textbox = ctk.CTkTextbox(self.chamber_frame, font=("Arial", 14), wrap="word", height=200)
        self.textbox.pack(fill="x", padx=20, pady=10)

        # Timer / Progress
        self.progress = ctk.CTkProgressBar(self.chamber_frame, orientation="horizontal", mode="determinate", progress_color="#B71C1C")
        self.progress.pack(fill="x", padx=20, pady=10)
        self.progress.set(0)

        self.timer_label = ctk.CTkLabel(self.chamber_frame, text="Ready to vent?", font=("Arial", 14, "bold"), text_color="gray")
        self.timer_label.pack(pady=5)

        # Button Row
        btn_row = ctk.CTkFrame(self.chamber_frame, fg_color="transparent")
        btn_row.pack(pady=20)

        self.burn_btn = ctk.CTkButton(
            btn_row, 
            text="Start Cooling Phase", 
            fg_color="#B71C1C", 
            hover_color="#D32F2F",
            command=self.start_cooldown
        )
        self.burn_btn.pack(side="left", padx=10)
        
        # Disabled initially
        self.resolve_btn = ctk.CTkButton(
            btn_row, 
            text="Offer to God", 
            state="disabled",
            fg_color="gray",
            command=self.offer_to_god
        )
        self.resolve_btn.pack(side="left", padx=10)

    def start_cooldown(self):
        if self.is_cooling: return
        self.is_cooling = True
        self.burn_btn.configure(state="disabled", text="Cooling...")
        self.textbox.configure(state="normal") # Ensure editable
        
        # Start Thread
        t = threading.Thread(target=self._run_timer)
        t.start()

    def _run_timer(self):
        steps = 100
        for i in range(steps + 1):
            if not self.winfo_exists(): return
            time.sleep(self.cooldown_seconds / steps)
            progress = i / steps
            
            # Update UI safely
            self.after(0, self._update_ui, progress, i)
            
    def _update_ui(self, progress, step):
        self.progress.set(progress)
        self.timer_label.configure(text=f"Cooling Down... {int(progress * 100)}%")
        
        if progress >= 1.0:
            self.timer_label.configure(text="The fire has settled. What now?")
            self.resolve_btn.configure(state="normal", fg_color="#2E7D32") # Green
            self.burn_btn.configure(text="Cooling Complete")

    def offer_to_god(self):
        # Clear text, show success message
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "--- Offered to God ---")
        self.textbox.configure(state="disabled")
        self.timer_label.configure(text="Peace be with you.")
        self.resolve_btn.configure(state="disabled", text="Offered")
        
        # Determine if we should save a 'hidden' log or just delete?
        # For now, just deleting/clearing as per 'Text-Withholding' concept.
