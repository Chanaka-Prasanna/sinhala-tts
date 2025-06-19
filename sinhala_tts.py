import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import os
import wave
import pygame
import tempfile

class SinhalaTTS:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sinhala Text-to-Speech")
        self.root.geometry("600x500")

        # initialize pygame mixer for WAV playback (16kHz mono)
        pygame.mixer.init(frequency=16000, size=-16, channels=1)

        # phonemes directory
        self.phonemes_dir = "phonemes"
        os.makedirs(self.phonemes_dir, exist_ok=True)

        self.stop_requested = False
        self.setup_ui()

    def setup_ui(self):
        main = ttk.Frame(self.root, padding=10)
        main.grid(sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        ttk.Label(main, text="Sinhala Text-to-Speech", font=("Arial", 16, "bold"))\
            .grid(row=0, column=0, columnspan=3, pady=(0,20))

        ttk.Label(main, text="Enter Sinhala Text:").grid(row=1, column=0, sticky=tk.W)
        self.text_input = scrolledtext.ScrolledText(main, height=8, font=("Noto Sans Sinhala",12))
        self.text_input.grid(row=2, column=0, columnspan=3, sticky=(tk.W,tk.E), pady=(5,10))

        btn_frame = ttk.Frame(main)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=10)
        self.speak_btn = ttk.Button(btn_frame, text="🔊 Speak", command=self.on_speak)
        self.speak_btn.pack(side=tk.LEFT, padx=(0,10))
        self.stop_btn  = ttk.Button(btn_frame, text="⏹ Stop", command=self.on_stop, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=(0,10))
        self.clear_btn = ttk.Button(btn_frame, text="🗑 Clear", command=lambda: self.text_input.delete("1.0", tk.END))
        self.clear_btn.pack(side=tk.LEFT)

        self.progress = ttk.Progressbar(main, mode="indeterminate")
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W,tk.E), pady=(10,5))
        self.status = ttk.Label(main, text="Ready to speak…")
        self.status.grid(row=5, column=0, columnspan=3, pady=(5,0))

        sample = "මේ සිංහල text-to-speech වැඩසටහනයි.\nකරුණාකර ඔබේ වාක්‍යය ඇතුල් කරන්න."
        self.text_input.insert("1.0", sample)

    def load_phoneme_map(self):
        # mapping of single characters to phoneme WAV filenames
        return {
            'අ':'a.wav','ආ':'aa.wav','ඇ':'ae.wav','ඈ':'aae.wav',
            'ඉ':'i.wav','ඊ':'ii.wav','උ':'u.wav','ඌ':'uu.wav',
            'එ':'e.wav','ඒ':'ee.wav','ඓ':'ai.wav','ඔ':'o.wav','ඕ':'oo.wav','ඖ':'au.wav',
            'ක':'ka.wav','ඛ':'kha.wav','ග':'ga.wav','ඝ':'gha.wav','ං':'ng.wav','ඞ':'nga.wav',
            'ච':'cha.wav','ඡ':'chha.wav','ජ':'ja.wav','ඣ':'jha.wav','ඤ':'nya.wav',
            'ට':'ta.wav','ඨ':'tha.wav','ඩ':'da.wav','ඪ':'dha.wav','ණ':'na.wav',
            'ත':'tha.wav','ථ':'thha.wav','ද':'da.wav','ධ':'dha.wav','න':'na.wav',
            'ප':'pa.wav','ඵ':'pha.wav','බ':'ba.wav','භ':'bha.wav','ම':'ma.wav',
            'ය':'ya.wav','ර':'ra.wav','ල':'la.wav','ව':'wa.wav','ශ':'sha.wav','ෂ':'sha.wav',
            'ස':'sa.wav','හ':'ha.wav','ළ':'la.wav','ෆ':'fa.wav',
            'ා':'aa.wav','ැ':'ae.wav','ෑ':'aae.wav','ි':'i.wav','ී':'ii.wav',
            'ු':'u.wav','ූ':'uu.wav','ෘ':'ru.wav','ෙ':'e.wav','ේ':'ee.wav',
            'ෛ':'ai.wav','ො':'o.wav','ෝ':'oo.wav','ෞ':'au.wav','්':'',
        }

    def ensure_phoneme(self, filename):
        path = os.path.join(self.phonemes_dir, filename)
        if not filename:
            return None
        if os.path.exists(path):
            return path
        # no phoneme available
        return None

    def text_to_phonemes(self, text):
        mapping = self.load_phoneme_map()
        seq = []
        for ch in text:
            if ch.isspace():
                seq.append(('pause', 0.3))
            elif ch in '.!?,;:\n':
                seq.append(('pause', 0.6))
            elif ch in mapping:
                fname = mapping[ch]
                if fname:
                    seq.append((fname, None))
        return seq

    def concatenate(self, phoneme_seq, out_path) -> None:
        frames = []
        params = None
        for item, pause in phoneme_seq:
            if item == 'pause':
                num = int(16000 * pause)
                frames.append(b'\x00\x00' * num)
                if not params:
                    # default WAV params: mono, 16-bit, 16kHz
                    params = (1, 2, 16000, 0, 'NONE', 'not compressed')
            else:
                wav_path = self.ensure_phoneme(item)
                if not wav_path:
                    continue
                with wave.open(wav_path, 'rb') as w:
                    if not params:
                        params = w.getparams()
                    frames.append(w.readframes(w.getnframes()))
        if not params:
            return
        with wave.open(out_path, 'wb') as out_wav:
            out_wav.setparams(params)
            out_wav.writeframes(b''.join(frames))

    def _build_and_play(self, seq):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        tmp.close()
        try:
            self.concatenate(seq, tmp.name)
            pygame.mixer.music.load(tmp.name)
            pygame.mixer.music.play()
            self.root.after(0, lambda: self.status.config(text="Playing…"))
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                if self.stop_requested:
                    pygame.mixer.music.stop()
                    break
        finally:
            try: os.unlink(tmp.name)
            except: pass
            self.root.after(0, self._on_finish)

    def on_speak(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning","Enter text to speak.")
            return
        seq = self.text_to_phonemes(text)
        if not seq:
            messagebox.showwarning("Warning","No Sinhala chars found.")
            return
        self.speak_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress.start()
        self.status.config(text="Generating audio…")
        threading.Thread(target=self._build_and_play, args=(seq,), daemon=True).start()

    def on_stop(self):
        self.stop_requested = True
        pygame.mixer.music.stop()
        self._on_finish()

    def _on_finish(self):
        self.stop_requested = False
        self.progress.stop()
        self.speak_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status.config(text="Ready to speak…")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    SinhalaTTS().run()
