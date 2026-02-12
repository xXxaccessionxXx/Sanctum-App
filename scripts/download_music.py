import yt_dlp
import os

def download_audio(url, output_base="assets/background"):
    if not os.path.exists("assets"):
        os.makedirs("assets")
        
    # Option 1: Try to get wav directly (best for winsound)
    ydl_opts_wav = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'outtmpl': output_base + '.%(ext)s',
        'quiet': False
    }
    
    # Option 2: Fallback to mp3 manual/generic
    ydl_opts_mp3 = {
        'format': 'bestaudio/best',
        'outtmpl': output_base + '.mp3',
        'quiet': False
    }

    print(f"Attempting download to {output_base}...")
    try:
        # Try WAV (needs ffmpeg)
        with yt_dlp.YoutubeDL(ydl_opts_wav) as ydl:
            ydl.download([url])
        print("WAV Download successful.")
    except Exception as e:
        print(f"WAV conversion failed (likely no ffmpeg): {e}")
        try:
            # Fallback to generic (likely m4a/webm, rename to mp3 carefully?)
            # Actually just get best audio
            with yt_dlp.YoutubeDL(ydl_opts_mp3) as ydl:
                 ydl.download([url])
            print("Fallback audio download successful.")
        except Exception as e2:
            print(f"All downloads failed: {e2}")

if __name__ == "__main__":
    download_audio("https://music.youtube.com/watch?v=K-D87rL4ugU&si=bo7ZkkqIba6PxnjC")
