import customtkinter as ctk

class UpdateDialog(ctk.CTkToplevel):
    def __init__(self, parent, new_version, on_update_click):
        super().__init__(parent)
        self.title("A New Regulation Issued")
        self.geometry("400x250")
        self.resizable(False, False)
        
        # Center the window
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (400 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (250 // 2)
        self.geometry(f"+{x}+{y}")
        
        self.attributes("-topmost", True)
        self.transient(parent)
        self.grab_set() # Modal

        # Visual Theology: Gold/Purple for Divine/Royal
        self.configure(fg_color="#FAFAFA")

        # Icon/Header
        ctk.CTkLabel(self, text="✨", font=("Arial", 40)).pack(pady=(20, 5))
        
        ctk.CTkLabel(self, text="Divine Revelation", font=("Times New Roman", 20, "bold"), text_color="#FBC02D").pack()
        ctk.CTkLabel(self, text=f"Version {new_version} is available.", font=("Arial", 12), text_color="gray").pack(pady=(0, 15))

        # Progress Bar (Hidden initially)
        self.progress_bar = ctk.CTkProgressBar(self, width=300, height=15, orientation="horizontal", mode="determinate")
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)
        self.progress_bar.pack_forget() # Hide until started

        self.status_label = ctk.CTkLabel(self, text="Would you like to receive this grace?", font=("Arial", 11), text_color="gray60")
        self.status_label.pack(pady=(0, 20))

        # Buttons
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(fill="x", padx=40)

        self.btn_cancel = ctk.CTkButton(self.btn_frame, text="Later", fg_color="transparent", text_color="gray", hover_color="#EEE", command=self.destroy)
        self.btn_cancel.pack(side="left", expand=True)

        self.btn_update = ctk.CTkButton(self.btn_frame, text="Update Now", fg_color="#FBC02D", text_color="black", hover_color="#F9A825", command=lambda: self.start_update(on_update_click))
        self.btn_update.pack(side="right", expand=True)

    def start_update(self, callback):
        self.btn_frame.pack_forget() # Hide buttons
        self.progress_bar.pack(pady=10) # Show progress
        self.status_label.configure(text="Manifesting changes...")
        callback(self) # Start the download logic passed from service

    def update_progress(self, current, total):
        if total > 0:
            val = current / total
            self.progress_bar.set(val)
        else:
            self.progress_bar.start()

    def set_status(self, text):
        self.status_label.configure(text=text)
