import customtkinter as ctk
import threading
import time

class CommunityView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="white", **kwargs)
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(header, text="The Communion of Saints", font=("Times New Roman", 24, "bold"), text_color="#4A148C").pack(side="left")
        ctk.CTkLabel(header, text="Nearby Pilgrims", font=("Arial", 12), text_color="gray").pack(side="left", padx=10, pady=(10, 0))

        # Peer List Container
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(expand=True, fill="both", padx=20, pady=(0, 20))
        
        self.status_label = ctk.CTkLabel(self.scroll, text="Scanning for nearby pilgrims...", text_color="gray")
        self.status_label.pack(pady=20)
        
        # Refresh Logic
        self.running = True
        self.refresh_thread = threading.Thread(target=self._auto_refresh, daemon=True)
        self.refresh_thread.start()

    def _auto_refresh(self):
        from src.services.discovery_service import DiscoveryService
        ds = DiscoveryService()
        
        # Ensure service is started
        if not ds.running:
            ds.start(username="Pilgrim") # Default name for now
            
        while self.running:
            if not self.winfo_exists(): break
            
            peers = ds.get_active_peers()
            self.after(0, self._update_list, peers)
            time.sleep(2)

    def _update_list(self, peers):
        # Clear current list (inefficient but simple for now)
        for widget in self.scroll.winfo_children():
            widget.destroy()
            
        if not peers:
            ctk.CTkLabel(self.scroll, text="No other pilgrims found nearby.", text_color="gray").pack(pady=20)
            return

        for p in peers:
            self._create_peer_card(p)

    def _create_peer_card(self, peer):
        card = ctk.CTkFrame(self.scroll, fg_color="#F3E5F5", corner_radius=10)
        card.pack(fill="x", pady=5)
        
        ctk.CTkLabel(card, text=peer['name'], font=("Arial", 14, "bold"), text_color="#4A148C").pack(side="left", padx=15, pady=10)
        
        # Send Grace Button
        btn = ctk.CTkButton(card, text="Send Grace", width=80, fg_color="#AB47BC", hover_color="#8E24AA", command=lambda: self.send_grace(peer))
        btn.pack(side="right", padx=15, pady=10)

    def send_grace(self, peer):
        print(f"Angle sent to {peer['name']}")
        # TODO: Implement actual messaging
