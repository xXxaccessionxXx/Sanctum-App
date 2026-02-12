import os
import time
import threading

# Try import pygame, if fail, try winsound (Windows only)
try:
    import pygame
    HAS_PYGAME = True
except ImportError:
    HAS_PYGAME = False

try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

class MusicService:
    _instance = None
    _is_initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MusicService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if MusicService._is_initialized:
            return
        
        self.current_volume = 0.3 # winsound doesn't support volume :(
        self.is_muted = False
        self.is_playing = False
        
        if HAS_PYGAME:
            try:
                pygame.mixer.init()
            except Exception as e:
                print(f"Pygame Init Error: {e}")
                global HAS_PYGAME
                HAS_PYGAME = False

        MusicService._is_initialized = True

    def play_background_music(self, file_path_base="assets/background"):
        """Tries to play mp3 with pygame, or wav with winsound."""
        if self.is_playing: return
        
        mp3_path = f"{file_path_base}.mp3"
        wav_path = f"{file_path_base}.wav"

        if HAS_PYGAME and os.path.exists(mp3_path) and not self.is_muted:
            try:
                pygame.mixer.music.load(mp3_path)
                pygame.mixer.music.play(loops=-1, fade_ms=2000)
                pygame.mixer.music.set_volume(self.current_volume)
                self.is_playing = True
                print("Playing background music (Pygame).")
                return
            except Exception as e:
                print(f"Pygame Play Error: {e}")

        # Fallback to Winsound
        if HAS_WINSOUND and os.path.exists(wav_path) and not self.is_muted:
            try:
                # SND_ASYNC | SND_LOOP
                winsound.PlaySound(wav_path, winsound.SND_ASYNC | winsound.SND_LOOP)
                self.is_playing = True
                print("Playing background music (Winsound).")
            except Exception as e:
                print(f"Winsound Play Error: {e}")

    def set_volume(self, volume: float):
        """Only works for Pygame."""
        self.current_volume = max(0.0, min(1.0, volume))
        if HAS_PYGAME:
            if self.is_muted:
                pygame.mixer.music.set_volume(0)
            else:
                pygame.mixer.music.set_volume(self.current_volume)

    def toggle_mute(self):
        self.is_muted = not self.is_muted
        if self.is_muted:
            self.stop()
        else:
            self.play_background_music() # Restart
        return self.is_muted

    def stop(self):
        self.is_playing = False
        if HAS_PYGAME:
            pygame.mixer.music.stop()
        if HAS_WINSOUND:
            winsound.PlaySound(None, 0)
