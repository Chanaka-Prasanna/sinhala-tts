import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import pyttsx3
import threading
import json
import os
from datetime import datetime
import re

class SinhalaTTSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sinhala Text-to-Speech System")
        self.root.geometry("800x600")
        
        # Initialize TTS engine
        self.tts_engine = pyttsx3.init()
        self.setup_tts_engine()
        
        # Load Sinhala phoneme mappings
        self.load_sinhala_phonemes()
        
        # Create GUI
        self.create_widgets()
        
        # Configure styles
        self.configure_styles()
        
    def setup_tts_engine(self):
        """Configure the TTS engine with appropriate settings"""
        try:
            # Set properties
            self.tts_engine.setProperty('rate', 150)  # Speaking rate
            self.tts_engine.setProperty('volume', 0.8)  # Volume level
            
            # Try to find available voices
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Use the first available voice
                self.tts_engine.setProperty('voice', voices[0].id)
        except Exception as e:
            print(f"TTS Engine setup error: {e}")
    
    def load_sinhala_phonemes(self):
        """Load Sinhala character to phoneme mappings in a structured way."""
        self.phoneme_map = {
            'vowels': {
                'අ': 'a', 'ආ': 'aa', 'ඇ': 'ae', 'ඈ': 'aae',
                'ඉ': 'i', 'ඊ': 'ii', 'උ': 'u', 'ඌ': 'uu',
                'ඍ': 'ru', 'ඎ': 'ruu', 'ඏ': 'li', 'ඐ': 'lii',
                'එ': 'e', 'ඒ': 'ee', 'ඓ': 'ai', 'ඔ': 'o',
                'ඕ': 'oo', 'ඖ': 'au'
            },
            'consonants': {
                'ක': 'ka', 'ඛ': 'kha', 'ග': 'ga', 'ඝ': 'gha', 'ඞ': 'nga',
                'ච': 'cha', 'ඡ': 'chha', 'ජ': 'ja', 'ඣ': 'jha', 'ඤ': 'nya',
                'ට': 'ta', 'ඨ': 'tha', 'ඩ': 'da', 'ඪ': 'dha', 'ණ': 'na',
                'ත': 'tha', 'ථ': 'thha', 'ද': 'da', 'ධ': 'dha', 'න': 'na',
                'ප': 'pa', 'ඵ': 'pha', 'බ': 'ba', 'භ': 'bha', 'ම': 'ma',
                'ය': 'ya', 'ර': 'ra', 'ල': 'la', 'ව': 'wa',
                'ශ': 'sha', 'ෂ': 'sha', 'ස': 'sa', 'හ': 'ha',
                'ළ': 'la', 'ෆ': 'fa'
            },
            'diacritics': {
                'ා': 'aa', 'ැ': 'ae', 'ෑ': 'aae', 'ි': 'i', 'ී': 'ii',
                'ු': 'u', 'ූ': 'uu', 'ෘ': 'ru', 'ෲ': 'ruu',
                'ෟ': 'li', 'ෳ': 'lii', 'ේ': 'ee', 'ෛ': 'ai',
                'ො': 'o', 'ෝ': 'oo', 'ෞ': 'au'
            },
            'special': {
                '්': '',   # Hal kirima - handled in logic
                'ං': 'ng', # Anusvaraya
                'ඃ': 'h'   # Visargaya
            },
            'punctuation': {
                ' ': ' ', '.': '.', ',': ',', '!': '!', '?': '?'
            }
        }
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Sinhala Text-to-Speech System", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Sinhala Text Input", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        # Text input area
        self.text_input = scrolledtext.ScrolledText(input_frame, height=8, width=60, 
                                                   font=("Noto Sans Sinhala", 12))
        self.text_input.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Sample text button
        sample_btn = ttk.Button(input_frame, text="Load Sample Text", 
                               command=self.load_sample_text)
        sample_btn.grid(row=1, column=0, sticky=tk.W)
        
        # Clear button
        clear_btn = ttk.Button(input_frame, text="Clear Text", 
                              command=self.clear_text)
        clear_btn.grid(row=1, column=1, sticky=tk.E)
        
        # Phonetic output section
        phonetic_frame = ttk.LabelFrame(main_frame, text="Phonetic Representation", padding="10")
        phonetic_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        phonetic_frame.columnconfigure(0, weight=1)
        
        self.phonetic_output = scrolledtext.ScrolledText(phonetic_frame, height=6, width=60, 
                                                        font=("Consolas", 10), state='disabled')
        self.phonetic_output.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Controls section
        controls_frame = ttk.LabelFrame(main_frame, text="TTS Controls", padding="10")
        controls_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Speed control
        ttk.Label(controls_frame, text="Speed:").grid(row=0, column=0, sticky=tk.W)
        self.speed_var = tk.IntVar(value=150)
        speed_scale = ttk.Scale(controls_frame, from_=50, to=300, variable=self.speed_var, 
                               orient=tk.HORIZONTAL, length=200)
        speed_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        self.speed_label = ttk.Label(controls_frame, text="150")
        self.speed_label.grid(row=0, column=2, sticky=tk.W, padx=(5, 0))
        speed_scale.configure(command=self.update_speed_label)
        
        # Volume control
        ttk.Label(controls_frame, text="Volume:").grid(row=1, column=0, sticky=tk.W)
        self.volume_var = tk.DoubleVar(value=0.8)
        volume_scale = ttk.Scale(controls_frame, from_=0.0, to=1.0, variable=self.volume_var, 
                                orient=tk.HORIZONTAL, length=200)
        volume_scale.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        self.volume_label = ttk.Label(controls_frame, text="0.8")
        self.volume_label.grid(row=1, column=2, sticky=tk.W, padx=(5, 0))
        volume_scale.configure(command=self.update_volume_label)
        
        controls_frame.columnconfigure(1, weight=1)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(10, 0))
        
        # Convert to phonetics button
        convert_btn = ttk.Button(button_frame, text="Convert to Phonetics", 
                                command=self.convert_to_phonetics)
        convert_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Speak button
        self.speak_btn = ttk.Button(button_frame, text="Speak", 
                                   command=self.speak_text)
        self.speak_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Stop button
        self.stop_btn = ttk.Button(button_frame, text="Stop", 
                                  command=self.stop_speaking, state='disabled')
        self.stop_btn.grid(row=0, column=2, padx=(0, 10))
        
        # Save audio button
        save_btn = ttk.Button(button_frame, text="Save as Audio", 
                             command=self.save_audio)
        save_btn.grid(row=0, column=3, padx=(0, 10))
        
        # Load file button
        load_btn = ttk.Button(button_frame, text="Load Text File", 
                             command=self.load_text_file)
        load_btn.grid(row=0, column=4)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Configure grid weights for resizing
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        input_frame.rowconfigure(0, weight=1)
        phonetic_frame.rowconfigure(0, weight=1)
    
    def configure_styles(self):
        """Configure GUI styles"""
        style = ttk.Style()
        style.theme_use('clam')
    
    def update_speed_label(self, value):
        """Update speed label"""
        self.speed_label.config(text=str(int(float(value))))
    
    def update_volume_label(self, value):
        """Update volume label"""
        self.volume_label.config(text=f"{float(value):.1f}")
    
    def load_sample_text(self):
        """Load sample Sinhala text"""
        sample_text = """සුභ උදෑසනක්! මේ සිංහල පෙළ කථන පද්ධතියයි.
ආයුබෝවන්! ඔබට කෙසේද?
මම සිංහල භාෂාව ඉගෙන ගන්නවා.
දෙන්නම්, හරියට ලියන්න!"""
        
        self.text_input.delete(1.0, tk.END)
        self.text_input.insert(1.0, sample_text)
        self.status_var.set("Sample text loaded")
    
    def clear_text(self):
        """Clear all text areas"""
        self.text_input.delete(1.0, tk.END)
        self.phonetic_output.config(state='normal')
        self.phonetic_output.delete(1.0, tk.END)
        self.phonetic_output.config(state='disabled')
        self.status_var.set("Text cleared")
    
    def sinhala_to_phonetic(self, sinhala_text):
        """Convert Sinhala text to phonetic representation using improved logic."""
        phonetic_text = ""
        i = 0
        text_len = len(sinhala_text)
        
        while i < text_len:
            char = sinhala_text[i]
            
            if char in self.phoneme_map['consonants']:
                base_phoneme = self.phoneme_map['consonants'][char]
                
                # Check for diacritics or hal kirima
                if i + 1 < text_len:
                    next_char = sinhala_text[i+1]
                    if next_char in self.phoneme_map['diacritics']:
                        # Vowel modification
                        phonetic_text += base_phoneme[:-1] + self.phoneme_map['diacritics'][next_char]
                        i += 1
                    elif next_char == '්':
                        # Hal kirima (vowel suppression)
                        phonetic_text += base_phoneme[:-1]
                        i += 1
                    else:
                        # Consonant with inherent 'a'
                        phonetic_text += base_phoneme
                else:
                    # Last character is a consonant with inherent 'a'
                    phonetic_text += base_phoneme
            
            elif char in self.phoneme_map['vowels']:
                phonetic_text += self.phoneme_map['vowels'][char]
            
            elif char in self.phoneme_map['special']:
                phonetic_text += self.phoneme_map['special'][char]
            
            elif char in self.phoneme_map['punctuation']:
                phonetic_text += self.phoneme_map['punctuation'][char]
                
            else:
                # Keep unknown characters
                phonetic_text += char
            
            i += 1
            
        return phonetic_text
    
    def convert_to_phonetics(self):
        """Convert input text to phonetic representation"""
        sinhala_text = self.text_input.get(1.0, tk.END).strip()
        
        if not sinhala_text:
            messagebox.showwarning("Warning", "Please enter some Sinhala text first!")
            return
        
        try:
            phonetic_text = self.sinhala_to_phonetic(sinhala_text)
            
            self.phonetic_output.config(state='normal')
            self.phonetic_output.delete(1.0, tk.END)
            self.phonetic_output.insert(1.0, phonetic_text)
            self.phonetic_output.config(state='disabled')
            
            self.status_var.set("Text converted to phonetics")
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")
    
    def speak_text(self):
        """Speak the phonetic text"""
        phonetic_text = self.phonetic_output.get(1.0, tk.END).strip()
        
        if not phonetic_text:
            # Convert first if not done
            self.convert_to_phonetics()
            phonetic_text = self.phonetic_output.get(1.0, tk.END).strip()
        
        if not phonetic_text:
            messagebox.showwarning("Warning", "No text to speak!")
            return
        
        # Update TTS engine properties
        self.tts_engine.setProperty('rate', self.speed_var.get())
        self.tts_engine.setProperty('volume', self.volume_var.get())
        
        # Start speaking in a separate thread
        def speak_thread():
            try:
                self.speak_btn.config(state='disabled')
                self.stop_btn.config(state='normal')
                self.status_var.set("Speaking...")
                
                self.tts_engine.say(phonetic_text)
                self.tts_engine.runAndWait()
                
            except Exception as e:
                messagebox.showerror("Error", f"Speech synthesis failed: {str(e)}")
            finally:
                self.speak_btn.config(state='normal')
                self.stop_btn.config(state='disabled')
                self.status_var.set("Ready")
        
        threading.Thread(target=speak_thread, daemon=True).start()
    
    def stop_speaking(self):
        """Stop current speech synthesis"""
        try:
            self.tts_engine.stop()
            self.speak_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            self.status_var.set("Speech stopped")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop speech: {str(e)}")
    
    def save_audio(self):
        """Save phonetic text as audio file"""
        phonetic_text = self.phonetic_output.get(1.0, tk.END).strip()
        
        if not phonetic_text:
            messagebox.showwarning("Warning", "No phonetic text to save!")
            return
        
        # Get save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")],
            title="Save Audio File"
        )
        
        if file_path:
            try:
                # Update TTS engine properties
                self.tts_engine.setProperty('rate', self.speed_var.get())
                self.tts_engine.setProperty('volume', self.volume_var.get())
                
                # Save to file
                self.tts_engine.save_to_file(phonetic_text, file_path)
                self.tts_engine.runAndWait()
                
                self.status_var.set(f"Audio saved to: {file_path}")
                messagebox.showinfo("Success", f"Audio saved successfully to:\n{file_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save audio: {str(e)}")
    
    def load_text_file(self):
        """Load text from file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Load Text File"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                self.text_input.delete(1.0, tk.END)
                self.text_input.insert(1.0, content)
                
                self.status_var.set(f"Text loaded from: {os.path.basename(file_path)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = SinhalaTTSApp(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main() 