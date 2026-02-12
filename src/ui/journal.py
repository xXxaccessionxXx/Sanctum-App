import customtkinter as ctk
import json
import os
from datetime import datetime
from src.core.covenant import Confession

DATA_FILE = "data/confessions.json"

class JournalView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="white", **kwargs)
        
        # Log Usage
        from src.core.stats_service import StatsService
        StatsService().log_module_entry("journal")
        
        # Grid Layout: 2 Columns (Write | History)
        self.grid_columnconfigure(0, weight=3) # Writing area
        self.grid_columnconfigure(1, weight=1) # History sidebar
        self.grid_rowconfigure(0, weight=1)

        # --- Left Side: Writing Area ---
        self.write_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.write_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        self.label = ctk.CTkLabel(
            self.write_frame, 
            text="Reflections", 
            font=("Times New Roman", 24, "bold"),
            text_color="#1A237E"
        )
        self.label.pack(pady=(0, 20), anchor="w")

        # Text Area with Placeholder Logic
        self.placeholder_text = "Write your prayer or confession here..."
        self.textbox = ctk.CTkTextbox(self.write_frame, corner_radius=10, font=("Arial", 14), fg_color="#F5F5F5")
        self.textbox.pack(expand=True, fill="both", pady=(0, 20))
        
        self.textbox.insert("0.0", self.placeholder_text)
        self.textbox.configure(text_color="gray")
        
        self.textbox.bind("<FocusIn>", self.on_focus_in)
        self.textbox.bind("<FocusOut>", self.on_focus_out)

        # Amen Button
        self.save_btn = ctk.CTkButton(
            self.write_frame,
            text="Amen (Save)",
            command=self.save_confession,
            fg_color="#1A237E",
            hover_color="#0D47A1",
            font=("Arial", 14, "bold"),
            height=40
        )
        self.save_btn.pack(anchor="e")

        # --- Right Side: History Sidebar ---
        self.history_frame = ctk.CTkScrollableFrame(self, label_text="History", fg_color="#ECEFF1", label_text_color="#455A64")
        self.history_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)

        self.load_history()

    def on_focus_in(self, event):
        if self.textbox.get("0.0", "end-1c") == self.placeholder_text:
            self.textbox.delete("0.0", "end")
            self.textbox.configure(text_color="black")

    def on_focus_out(self, event):
        if not self.textbox.get("0.0", "end-1c"):
            self.textbox.insert("0.0", self.placeholder_text)
            self.textbox.configure(text_color="gray")

    def save_confession(self):
        print("Save button clicked.")
        text = self.textbox.get("0.0", "end-1c")
        print(f"Text content: '{text}'")
        
        if not text or text == self.placeholder_text:
            print("Save aborted: Empty text or placeholder.")
            return

        try:
            print("Creating confession object...")
            confession = Confession(
                id=str(int(datetime.now().timestamp())),
                text=text,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M")
            )
            print(f"Confession created: {confession}")

            self.save_to_file(confession)
            print("Save to file successful.")
            
            # Clear and reset
            self.textbox.delete("0.0", "end")
            self.on_focus_out(None)
            
            # Refresh History
            self.load_history()
            
            # Show visible feedback (optional, but good for user)
            self.label.configure(text="Reflections (Saved!)", text_color="green")
            self.after(2000, lambda: self.label.configure(text="Reflections", text_color="#1A237E"))
            
        except Exception as e:
            print(f"Error saving confession: {e}")
            self.label.configure(text=f"Error: {e}", text_color="red")

    def save_to_file(self, confession):
        data = []
        
        # Ensure dir exists
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        
        data.append({"id": confession.id, "text": confession.text, "timestamp": confession.timestamp})
        
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def load_history(self):
        # Clear existing
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        if not os.path.exists(DATA_FILE):
            return

        with open(DATA_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return

        # Display latest first
        for item in reversed(data):
            self.create_history_item(item)

    def create_history_item(self, item):
        card = ctk.CTkFrame(self.history_frame, fg_color="white", corner_radius=10)
        card.pack(fill="x", pady=5, padx=5)
        
        # Click to view logic can be added here, for now just static display
        
        date_lbl = ctk.CTkLabel(card, text=item["timestamp"], font=("Arial", 10, "bold"), text_color="gray")
        date_lbl.pack(anchor="w", padx=10, pady=(5, 0))
        
        preview_text = item["text"][:50] + "..." if len(item["text"]) > 50 else item["text"]
        text_lbl = ctk.CTkLabel(card, text=preview_text, font=("Arial", 12), anchor="w", justify="left")
        text_lbl.pack(fill="x", padx=10, pady=(0, 5))
        
        # View Button (Small)
        view_btn = ctk.CTkButton(
            card, text="Read", width=50, height=20, 
            fg_color="transparent", border_width=1, border_color="gray", text_color="gray",
            command=lambda i=item: self.view_confession(i)
        )
        view_btn.pack(anchor="e", padx=10, pady=(0, 5))

    def view_confession(self, item):
        # Create a popup window
        top = ctk.CTkToplevel(self)
        top.title(f"Confession - {item['timestamp']}")
        top.geometry("500x500")
        top.attributes("-topmost", True)
        
        txt = ctk.CTkTextbox(top, font=("Arial", 14), wrap="word")
        txt.pack(expand=True, fill="both", padx=20, pady=20)
        txt.insert("0.0", item["text"])
        txt.configure(state="disabled") # Read-only

        # Email Button
        self.email_status = ctk.CTkLabel(top, text="", text_color="gray")
        self.email_status.pack(pady=(10, 0))

        self.email_btn = ctk.CTkButton(
            top, 
            text="Send via Email", 
            fg_color="#1A237E",
            command=lambda: self.start_email_thread(item)
        )
        self.email_btn.pack(pady=20)

    def start_email_thread(self, item):
        import threading
        self.email_btn.configure(state="disabled", text="Sending...")
        self.email_status.configure(text="Connecting to server...", text_color="blue")
        
        thread = threading.Thread(target=self.send_email_task, args=(item,))
        thread.start()

    def send_email_task(self, item):
        from src.core.email_service import EmailService
        import json, os
        
        # Load Settings
        target = ""
        sender = ""
        pwd = ""
        
        if os.path.exists("data/settings.json"):
             with open("data/settings.json", "r") as f:
                try:
                    data = json.load(f)
                    target = data.get("target_email", "")
                    sender = data.get("sender_email", "")
                    pwd = data.get("sender_password", "")
                except:
                    pass

        subject = f"Confession - {item['timestamp']}"
        body = f"{item['text']}\n\n---\nSent from Sanctum"

        success = False
        msg = ""

        if sender and pwd and target:
            # Try SMTP
            success, msg = EmailService.send_via_smtp(sender, pwd, target, subject, body)
            if not success:
                # Update UI on failure (schedule on main thread ideally, but CTk is lenient or we use after)
                print(f"SMTP Failed: {msg}")
                # Fallback handled below
        else:
            msg = "No SMTP credentials found. Opening default client."
        
        # UI Update must happen on main thread usually. 
        # But for simple label updates, Tkinter sometimes tolerates it, better to use .after
        self.after(0, lambda: self.finish_email_task(success, msg, subject, body, target))

    def finish_email_task(self, success, msg, subject, body, target):
        self.email_btn.configure(state="normal", text="Send via Email")
        
        if success:
            self.email_status.configure(text=f"Email Sent Successfully! ({msg})", text_color="green")
        else:
            self.email_status.configure(text="Connection Failed. Opening Default Mail App...", text_color="#E65100")
            print(f"SMTP Debug: {msg}")
            
            # Show a small error dialog/label if possible, or just the status
            # Fallback open
            from src.core.email_service import EmailService
            EmailService.send_via_client(subject, body, [target] if target else [])
