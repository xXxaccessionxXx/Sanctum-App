import socket
import threading
import time
import json
import uuid

class DiscoveryService:
    _instance = None
    _is_initialized = False

    PORT = 5005
    BROADCAST_IP = '<broadcast>'
    ANNOUNCE_INTERVAL = 5 # seconds

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DiscoveryService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if DiscoveryService._is_initialized:
            return
        
        self.my_id = str(uuid.uuid4())[:8]
        self.peers = {} # {id: {'last_seen': time, 'ip': ip, 'name': name}}
        self.running = False
        
        # Initialize attributes to None to satisfy linter
        self.socket = None
        self.username = "Pilgrim"
        self.listen_thread = None
        self.announce_thread = None
        
        DiscoveryService._is_initialized = True

    def start(self, username="Pilgrim"):
        if self.running: return
        self.running = True
        self.username = username
        
        # Setup UDP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # Bind to listen
        try:
             # On Windows, binding to "" allows receiving broadcasts
            self.socket.bind(("", self.PORT))
        except Exception as e:
            print(f"Discovery Bind Error: {e}")
            self.running = False
            return

        # Start threads
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()
        
        self.announce_thread = threading.Thread(target=self._announce_loop, daemon=True)
        self.announce_thread.start()
        
        print(f"Discovery Service Started as {self.username} ({self.my_id})")

    def stop(self):
        self.running = False
        if self.socket:
            self.socket.close()

    def _announce_loop(self):
        while self.running:
            try:
                msg = json.dumps({
                    "id": self.my_id,
                    "type": "ANNOUNCE",
                    "name": self.username
                })
                self.socket.sendto(msg.encode(), (self.BROADCAST_IP, self.PORT))
            except Exception as e:
                print(f"Announce Error: {e}")
            time.sleep(self.ANNOUNCE_INTERVAL)

    def _listen_loop(self):
        while self.running:
            try:
                data, addr = self.socket.recvfrom(1024)
                msg = json.loads(data.decode())
                
                if msg.get("id") == self.my_id:
                    continue # Ignore self
                
                if msg.get("type") == "ANNOUNCE":
                    self._update_peer(msg["id"], msg.get("name", "Unknown"), addr[0])
                    
            except Exception:
                pass # Socket closed or error

    def _update_peer(self, peer_id, name, ip):
        self.peers[peer_id] = {
            "last_seen": time.time(),
            "name": name,
            "ip": ip
        }
    
    def get_active_peers(self, timeout=15):
        """Returns list of peers seen in last `timeout` seconds."""
        current_time = time.time()
        active = []
        for pid, data in self.peers.items():
            if current_time - data["last_seen"] < timeout:
                active.append(data)
        return active
