import customtkinter as ctk
from src.core.stats_service import StatsService

class GreedView(ctk.CTkFrame):
    def __init__(self, master, module, on_back=None, **kwargs):
        super().__init__(master, fg_color="#E8F5E9", **kwargs) # Light Green
        self.module = module
        self.on_back = on_back
        # self.logic = LedgerLogic() # Removed
        
        # Log Usage
        from src.core.stats_service import StatsService
        StatsService().log_module_entry("greed")
        
        self.entry_count = 0
        self.required_entries = 3

        # --- Header ---
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=20)
        
        # Disabled Back Button initially
        self.back_btn = ctk.CTkButton(self.header, text="Locked", width=60, state="disabled", fg_color="gray", command=self.on_back)
        self.back_btn.pack(side="left")
        
        title = ctk.CTkLabel(self.header, text=f"{module.icon_char} {module.title}", font=("Arial", 24, "bold"), text_color="#2E7D32")
        title.pack(side="left", padx=20)

        # --- The Ledger ---
        self.ledger_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        self.ledger_frame.pack(expand=True, fill="both", padx=40, pady=20)

        ctk.CTkLabel(self.ledger_frame, text="The Ledger of Grace", font=("Arial", 16, "bold"), text_color="#2E7D32").pack(pady=(20, 5))
        ctk.CTkLabel(self.ledger_frame, text="Log 3 things you received today that money cannot buy.", font=("Arial", 12), text_color="gray").pack(pady=(0, 20))

        # Balance Display
        self.balance_label = ctk.CTkLabel(self.ledger_frame, text=f"Spiritual Balance: {self.entry_count}/{self.required_entries}", font=("Arial", 14, "bold"), text_color="gray")
        self.balance_label.pack(pady=10)

        # Inputs
        self.entries = []
        for i in range(3):
            entry = ctk.CTkEntry(self.ledger_frame, placeholder_text=f"Blessing #{i+1}...", width=300)
            entry.pack(pady=5)
            self.entries.append(entry)

        self.submit_btn = ctk.CTkButton(
            self.ledger_frame, 
            text="Deposit into Treasury", 
            fg_color="#2E7D32", 
            hover_color="#1B5E20",
            command=self.submit_gratitude
        )
        self.submit_btn.pack(pady=20)
        
        self.msg_label = ctk.CTkLabel(self.ledger_frame, text="", text_color="#2E7D32")
        self.msg_label.pack()

    def submit_gratitude(self):
        # Validate inputs
        filled = [e.get() for e in self.entries if e.get().strip()]
        count = len(filled)
        
        if count >= self.required_entries:
            self.entry_count = count
            self.balance_label.configure(text=f"Spiritual Balance: {count}/{self.required_entries} (Full)", text_color="#2E7D32")
            self.msg_label.configure(text="Offering Accepted. You are richer than you know.")
            
            # Unlock Back Button
            self.back_btn.configure(state="normal", text="← Back", fg_color="transparent", text_color="gray", hover_color="#C8E6C9")
            self.submit_btn.configure(state="disabled", text="Deposited")
            
            # Disable entries
            for e in self.entries:
                e.configure(state="disabled")
        else:
            self.msg_label.configure(text=f"The ledger is incomplete. Found {count}/{self.required_entries}.", text_color="#D32F2F")
