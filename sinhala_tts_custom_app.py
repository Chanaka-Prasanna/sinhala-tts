import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import os
import time
import re
import simpleaudio as sa

# Directory containing WAV files for each phoneme (e.g. "ka.wav", "ae.wav", etc.)
PHONEME_AUDIO_DIR = os.path.join(os.path.dirname(__file__), "phonemes")

class CustomVoiceTTSApp:
    """Sinhala TTS that plays user-recorded phoneme waveclips instead of using a synthesized voice."""

    def __init__(self, root):
        self.root = root
        self.root.title("Sinhala TTS – Custom Voice")
        self.root.geometry("800x600")

        self.load_phoneme_maps()
        self.create_widgets()
        self.configure_styles()

        self.is_playing = False

    def load_phoneme_maps(self):
        # Same phoneme dictionary used in the main application.
        self.phoneme_map = {
            'vowels': {
                'අ': 'a', 'ආ': 'aa', 'ඇ': 'ae', 'ඈ': 'aae',
                'ඉ': 'e', 'ඊ': 'ee', 'උ': 'u', 'ඌ': 'uu',
                'ඍ': 'ru', 'ඎ': 'ruu', 'ඏ': 'li', 'ඐ': 'lii',
                'එ': 'e', 'ඒ': 'ee', 'ඓ': 'ai', 'ඔ': 'o',
                'ඕ': 'oo', 'ඖ': 'au'
            },
            'consonants': {
                'ක': 'ka', 'ඛ': 'kha', 'ග': 'ga', 'ඝ': 'gha', 'ඞ': 'nga',
                'ච': 'cha', 'ඡ': 'chha', 'ජ': 'ja', 'ඣ': 'jha', 'ඤ': 'nya',
                'ට': 'ta', 'ඨ': 'tha', 'ඩ': 'da', 'ඪ': 'dha', 'ණ': 'na',
                'ත': 'tha', 'ථ': 'thha', 'ද': 'dha', 'ධ': 'dha', 'න': 'na',
                'ප': 'pa', 'ඵ': 'pha', 'බ': 'ba', 'භ': 'bha', 'ම': 'ma',
                'ය': 'ya', 'ර': 'ra', 'ල': 'la', 'ව': 'wa',
                'ශ': 'sha', 'ෂ': 'sha', 'ස': 'sa', 'හ': 'ha',
                'ළ': 'la', 'ෆ': 'fa'
            },
            'diacritics': {
                'ා': 'aa', 'ැ': 'ae', 'ෑ': 'aae', 'ි': 'i', 'ී': 'ii',
                'ු': 'u', 'ූ': 'uu', 'ෘ': 'ru', 'ෲ': 'ruu',
                'ෟ': 'li', 'ෳ': 'lii', 'ේ': 'ee', 'ෛ': 'ai',
                'ෙ': 'e', 'ො': 'o', 'ෝ': 'oo', 'ෞ': 'au'
            },
            'special': {'්': '', 'ං': 'ng', 'ඃ': 'h'},
            'punctuation': {' ': ' ', '.': '.', ',': ',', '!': '!', '?': '?'}
        }

    # ------------- GUI -------------
    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        ttk.Label(frame, text="Sinhala TTS – Custom Voice", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=(0, 20))

        self.text_input = scrolledtext.ScrolledText(frame, height=8, font=("Noto Sans Sinhala", 12))
        self.text_input.grid(row=1, column=0, sticky="nsew")

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, pady=(10, 0))
        convert_btn = ttk.Button(btn_frame, text="Convert to Phonetics", command=self.convert_text)
        convert_btn.grid(row=0, column=0, padx=5)
        play_btn = ttk.Button(btn_frame, text="Play", command=self.play_custom_voice)
        play_btn.grid(row=0, column=1, padx=5)

        self.phon_output = scrolledtext.ScrolledText(frame, height=6, font=("Consolas", 10), state='disabled')
        self.phon_output.grid(row=3, column=0, sticky="nsew", pady=(10, 0))

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).grid(row=4, column=0, sticky="ew", pady=(10, 0))

        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(3, weight=1)

    def configure_styles(self):
        ttk.Style().theme_use('clam')

    # ------------- Conversion -------------
    def sinhala_to_phonetic(self, text):
        phon = ""
        i = 0
        n = len(text)
        while i < n:
            ch = text[i]
            if ch in ("\u200c", "\u200d"):
                i += 1; continue
            if ch in self.phoneme_map['consonants']:
                base = self.phoneme_map['consonants'][ch]
                nxt = text[i+1] if i+1 < n else ''
                nxt2 = text[i+2] if i+2 < n else ''
                if nxt == '්':
                    if nxt2 in ('ය', 'ර'):
                        phon += base[:-1] + self.phoneme_map['consonants'][nxt2]
                        i += 3; continue
                    phon += base[:-1]; i += 2; continue
                if nxt in self.phoneme_map['diacritics']:
                    phon += base[:-1] + self.phoneme_map['diacritics'][nxt]
                    i += 2; continue
                phon += base; i += 1; continue
            if ch in self.phoneme_map['vowels']:
                phon += self.phoneme_map['vowels'][ch]; i += 1; continue
            if ch in self.phoneme_map['special']:
                phon += self.phoneme_map['special'][ch]; i += 1; continue
            if ch in self.phoneme_map['punctuation']:
                phon += self.phoneme_map['punctuation'][ch]; i += 1; continue
            phon += ch; i += 1
        return phon

    # ------------- Actions -------------
    def convert_text(self):
        txt = self.text_input.get(1.0, tk.END).strip()
        if not txt:
            messagebox.showwarning("Warning", "Please enter Sinhala text.")
            return
        phon = self.sinhala_to_phonetic(txt)
        self.phon_output.config(state='normal'); self.phon_output.delete(1.0, tk.END)
        self.phon_output.insert(1.0, phon); self.phon_output.config(state='disabled')
        self.status_var.set("Converted to phonetics")

    def play_custom_voice(self):
        if self.is_playing:
            return
        phon_text = self.phon_output.get(1.0, tk.END).strip()
        if not phon_text:
            self.convert_text()
            phon_text = self.phon_output.get(1.0, tk.END).strip()
            if not phon_text:
                return
        threading.Thread(target=self._play_thread, args=(phon_text,), daemon=True).start()

    def _play_thread(self, phon_text):
        self.is_playing = True
        self.status_var.set("Playing…")
        try:
            tokens = re.findall(r"[a-zA-Z]+|[ .,!?]", phon_text)
            for tok in tokens:
                tok = tok.strip()
                if tok == "":
                    time.sleep(0.05); continue
                if tok in (".", ",", "!", "?"):
                    time.sleep(0.2); continue
                wav = os.path.join(PHONEME_AUDIO_DIR, f"{tok}.wav")
                if os.path.isfile(wav):
                    play = sa.WaveObject.from_wave_file(wav).play()
                    play.wait_done()
                else:
                    time.sleep(0.05)  # Missing phoneme, brief pause
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.is_playing = False
            self.status_var.set("Ready")


def main():
    root = tk.Tk()
    app = CustomVoiceTTSApp(root)
    root.mainloop()


if __name__ == "__main__":
    main() 