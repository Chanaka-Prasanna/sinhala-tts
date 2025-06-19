import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import time
import os
import wave
import pygame
import tempfile
import json
from sinhala_text_to_phoneme import SinhalaTextToPhoneme

class EnhancedSinhalaTTS:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Enhanced Sinhala Text-to-Speech & Linguistic Analysis")
        self.root.geometry("1000x700")
        self.root.state('zoomed')  # Maximize window
        
        # Initialize components
        self.phoneme_converter = SinhalaTextToPhoneme()
        pygame.mixer.init(frequency=16000, size=-16, channels=1)
        
        # Directories
        self.phonemes_dir = "phonemes"
        os.makedirs(self.phonemes_dir, exist_ok=True)
        
        # State variables
        self.stop_requested = False
        self.current_analysis = {}
        
        self.setup_ui()
        self.check_phoneme_files()

    def setup_ui(self):
        """Setup the main user interface"""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # TTS Tab
        self.setup_tts_tab(notebook)
        
        # Linguistic Analysis Tab
        self.setup_analysis_tab(notebook)
        
        # Phoneme Explorer Tab
        self.setup_phoneme_tab(notebook)
        
        # Settings Tab
        self.setup_settings_tab(notebook)

    def setup_tts_tab(self, notebook):
        """Setup the Text-to-Speech tab"""
        tts_frame = ttk.Frame(notebook)
        notebook.add(tts_frame, text="🔊 Text-to-Speech")
        
        # Main container
        main_container = ttk.Frame(tts_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_container, text="Sinhala Text-to-Speech", 
                               font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Input section
        input_frame = ttk.LabelFrame(main_container, text="Input Text", padding=10)
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Text input with Sinhala font
        self.text_input = scrolledtext.ScrolledText(
            input_frame, 
            height=10, 
            font=("Noto Sans Sinhala", 14),
            wrap=tk.WORD
        )
        self.text_input.pack(fill=tk.BOTH, expand=True)
        
        # Sample text
        sample_text = """මම පොතක් කියවන්න යනවා."""
        
        self.text_input.insert("1.0", sample_text)
        
        # Control buttons
        button_frame = ttk.Frame(main_container)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.speak_btn = ttk.Button(button_frame, text="🔊 Speak", 
                                   command=self.on_speak, style="Accent.TButton")
        self.speak_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(button_frame, text="⏹ Stop", 
                                  command=self.on_stop, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = ttk.Button(button_frame, text="🗑 Clear", 
                                   command=self.clear_text)
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.analyze_btn = ttk.Button(button_frame, text="🔍 Analyze", 
                                     command=self.show_analysis)
        self.analyze_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_audio_btn = ttk.Button(button_frame, text="💾 Save Audio", 
                                        command=self.save_audio)
        self.save_audio_btn.pack(side=tk.LEFT)
        
        # Speed control
        speed_frame = ttk.Frame(button_frame)
        speed_frame.pack(side=tk.RIGHT)
        
        ttk.Label(speed_frame, text="Speed:").pack(side=tk.LEFT)
        self.speed_var = tk.DoubleVar(value=1.0)
        self.speed_scale = ttk.Scale(speed_frame, from_=0.5, to=2.0, 
                                    variable=self.speed_var, orient=tk.HORIZONTAL)
        self.speed_scale.pack(side=tk.LEFT, padx=5)
        
        self.speed_label = ttk.Label(speed_frame, text="1.0x")
        self.speed_label.pack(side=tk.LEFT)
        self.speed_var.trace('w', self.update_speed_label)
        
        # Status section
        status_frame = ttk.LabelFrame(main_container, text="Status", padding=10)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress = ttk.Progressbar(status_frame, mode="indeterminate")
        self.progress.pack(fill=tk.X, pady=(0, 5))
        
        self.status_label = ttk.Label(status_frame, text="Ready to speak...")
        self.status_label.pack()
        
        # Quick analysis preview
        preview_frame = ttk.LabelFrame(main_container, text="Quick Preview", padding=10)
        preview_frame.pack(fill=tk.X)
        
        self.preview_text = tk.Text(preview_frame, height=3, font=("Consolas", 10),
                                   state=tk.DISABLED, bg="#f0f0f0")
        self.preview_text.pack(fill=tk.X)

    def setup_analysis_tab(self, notebook):
        """Setup the Linguistic Analysis tab"""
        analysis_frame = ttk.Frame(notebook)
        notebook.add(analysis_frame, text="🔍 Linguistic Analysis")
        
        # Main container
        main_container = ttk.Frame(analysis_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_container, text="Sinhala Linguistic Analysis", 
                               font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Create paned window for split layout
        paned = ttk.PanedWindow(main_container, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Input and controls
        left_panel = ttk.Frame(paned)
        paned.add(left_panel, weight=1)
        
        # Text input for analysis
        input_frame = ttk.LabelFrame(left_panel, text="Text for Analysis", padding=10)
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.analysis_input = scrolledtext.ScrolledText(
            input_frame, 
            height=10, 
            font=("Noto Sans Sinhala", 12)
        )
        self.analysis_input.pack(fill=tk.BOTH, expand=True)
        
        # Analysis controls
        control_frame = ttk.Frame(left_panel)
        control_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(control_frame, text="🔍 Analyze Text", 
                  command=self.perform_analysis).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="📋 Copy Analysis", 
                  command=self.copy_analysis).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="💾 Save Analysis", 
                  command=self.save_analysis).pack(side=tk.LEFT)
        
        # Right panel - Results
        right_panel = ttk.Frame(paned)
        paned.add(right_panel, weight=2)
        
        # Analysis results notebook
        self.analysis_notebook = ttk.Notebook(right_panel)
        self.analysis_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Phoneme breakdown tab
        self.setup_phoneme_breakdown_tab()
        
        # Tokenization tab
        self.setup_tokenization_tab()
        
        # Statistics tab
        self.setup_statistics_tab()

    def setup_phoneme_breakdown_tab(self):
        """Setup phoneme breakdown analysis tab"""
        phoneme_frame = ttk.Frame(self.analysis_notebook)
        self.analysis_notebook.add(phoneme_frame, text="Phonemes")
        
        self.phoneme_result = scrolledtext.ScrolledText(
            phoneme_frame, 
            font=("Consolas", 11),
            state=tk.DISABLED
        )
        self.phoneme_result.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def setup_tokenization_tab(self):
        """Setup tokenization analysis tab"""
        token_frame = ttk.Frame(self.analysis_notebook)
        self.analysis_notebook.add(token_frame, text="Tokenization")
        
        self.token_result = scrolledtext.ScrolledText(
            token_frame, 
            font=("Consolas", 11),
            state=tk.DISABLED
        )
        self.token_result.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def setup_statistics_tab(self):
        """Setup statistics analysis tab"""
        stats_frame = ttk.Frame(self.analysis_notebook)
        self.analysis_notebook.add(stats_frame, text="Statistics")
        
        self.stats_result = scrolledtext.ScrolledText(
            stats_frame, 
            font=("Consolas", 11),
            state=tk.DISABLED
        )
        self.stats_result.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def setup_phoneme_tab(self, notebook):
        """Setup the Phoneme Explorer tab"""
        phoneme_frame = ttk.Frame(notebook)
        notebook.add(phoneme_frame, text="🎵 Phoneme Explorer")
        
        # Main container
        main_container = ttk.Frame(phoneme_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_container, text="Phoneme Explorer", 
                               font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Phoneme list frame
        list_frame = ttk.LabelFrame(main_container, text="Available Phonemes", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create treeview for phonemes
        columns = ("Phoneme", "File", "Status")
        self.phoneme_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Define headings
        self.phoneme_tree.heading("Phoneme", text="Phoneme")
        self.phoneme_tree.heading("File", text="Audio File")
        self.phoneme_tree.heading("Status", text="Status")
        
        # Configure column widths
        self.phoneme_tree.column("Phoneme", width=100)
        self.phoneme_tree.column("File", width=150)
        self.phoneme_tree.column("Status", width=100)
        
        # Scrollbar for treeview
        phoneme_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.phoneme_tree.yview)
        self.phoneme_tree.configure(yscrollcommand=phoneme_scrollbar.set)
        
        self.phoneme_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        phoneme_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Phoneme controls
        control_frame = ttk.Frame(main_container)
        control_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(control_frame, text="🔄 Refresh List", 
                  command=self.refresh_phoneme_list).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="▶ Play Selected", 
                  command=self.play_selected_phoneme).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="📊 Generate Report", 
                  command=self.generate_phoneme_report).pack(side=tk.LEFT)
        
        # Bind double-click to play
        self.phoneme_tree.bind("<Double-1>", lambda e: self.play_selected_phoneme())

    def setup_settings_tab(self, notebook):
        """Setup the Settings tab"""
        settings_frame = ttk.Frame(notebook)
        notebook.add(settings_frame, text="⚙ Settings")
        
        # Main container
        main_container = ttk.Frame(settings_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_container, text="Settings", 
                               font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Audio settings
        audio_frame = ttk.LabelFrame(main_container, text="Audio Settings", padding=10)
        audio_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Sample rate
        ttk.Label(audio_frame, text="Sample Rate:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.sample_rate_var = tk.StringVar(value="16000")
        sample_rate_combo = ttk.Combobox(audio_frame, textvariable=self.sample_rate_var,
                                        values=["8000", "16000", "22050", "44100"], state="readonly")
        sample_rate_combo.grid(row=0, column=1, sticky=tk.W, padx=10)
        
        # Pause duration
        ttk.Label(audio_frame, text="Word Pause (seconds):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.word_pause_var = tk.DoubleVar(value=0.3)
        word_pause_scale = ttk.Scale(audio_frame, from_=0.1, to=1.0, 
                                    variable=self.word_pause_var, orient=tk.HORIZONTAL)
        word_pause_scale.grid(row=1, column=1, sticky=tk.W, padx=10)
        
        ttk.Label(audio_frame, text="Sentence Pause (seconds):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.sentence_pause_var = tk.DoubleVar(value=0.6)
        sentence_pause_scale = ttk.Scale(audio_frame, from_=0.2, to=2.0, 
                                        variable=self.sentence_pause_var, orient=tk.HORIZONTAL)
        sentence_pause_scale.grid(row=2, column=1, sticky=tk.W, padx=10)
        
        # Analysis settings
        analysis_frame = ttk.LabelFrame(main_container, text="Analysis Settings", padding=10)
        analysis_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.show_clusters_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(analysis_frame, text="Show consonant clusters", 
                       variable=self.show_clusters_var).pack(anchor=tk.W)
        
        self.show_diacritics_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(analysis_frame, text="Show diacritic breakdown", 
                       variable=self.show_diacritics_var).pack(anchor=tk.W)
        
        self.show_phonetic_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(analysis_frame, text="Show phonetic variations", 
                       variable=self.show_phonetic_var).pack(anchor=tk.W)
        
        # File settings
        file_frame = ttk.LabelFrame(main_container, text="File Settings", padding=10)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(file_frame, text="Phonemes Directory:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.phoneme_dir_var = tk.StringVar(value=self.phonemes_dir)
        ttk.Entry(file_frame, textvariable=self.phoneme_dir_var, width=40).grid(row=0, column=1, padx=10)
        ttk.Button(file_frame, text="Browse", 
                  command=self.browse_phoneme_dir).grid(row=0, column=2, padx=5)
        
        # Action buttons
        action_frame = ttk.Frame(main_container)
        action_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(action_frame, text="💾 Save Settings", 
                  command=self.save_settings).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="🔄 Reset to Defaults", 
                  command=self.reset_settings).pack(side=tk.LEFT)

    # Core TTS Methods
    def text_to_phonemes_enhanced(self, text):
        """Convert text to phonemes using the enhanced system"""
        try:
            phonemes = self.phoneme_converter.text_to_phonemes(text)
            phoneme_sequence = []
            
            for phoneme in phonemes:
                if phoneme == ' ':
                    phoneme_sequence.append(('pause', self.word_pause_var.get()))
                elif phoneme in '.,!?;:\n':
                    phoneme_sequence.append(('pause', self.sentence_pause_var.get()))
                else:
                    # Look for phoneme file
                    phoneme_file = f"{phoneme}.wav"
                    if self.ensure_phoneme_file(phoneme_file):
                        phoneme_sequence.append((phoneme_file, None))
                    else:
                        # Fallback: try to break down complex phonemes
                        fallback_sequence = self.handle_missing_phoneme(phoneme)
                        phoneme_sequence.extend(fallback_sequence)
            
            return phoneme_sequence
        except Exception as e:
            messagebox.showerror("Error", f"Error converting text to phonemes: {e}")
            return []

    def ensure_phoneme_file(self, filename):
        """Check if phoneme file exists"""
        if not filename:
            return False
        path = os.path.join(self.phonemes_dir, filename)
        return os.path.exists(path)

    def handle_missing_phoneme(self, phoneme):
        """Handle missing phoneme by breaking it down"""
        sequence = []
        # Try to break down complex phonemes into simpler ones
        if len(phoneme) > 2:
            # Try breaking into smaller parts
            for i in range(len(phoneme)):
                part = phoneme[i]
                part_file = f"{part}.wav"
                if self.ensure_phoneme_file(part_file):
                    sequence.append((part_file, None))
        return sequence

    def concatenate_audio(self, phoneme_seq, out_path):
        """Concatenate phoneme audio files with improved error handling"""
        try:
            frames = []
            params = None
            sample_rate = int(self.sample_rate_var.get())
            
            for item, pause in phoneme_seq:
                if item == 'pause':
                    # Add silence
                    num_samples = int(sample_rate * pause)
                    silence = b'\x00\x00' * num_samples
                    frames.append(silence)
                    if not params:
                        params = (1, 2, sample_rate, 0, 'NONE', 'not compressed')
                else:
                    wav_path = os.path.join(self.phonemes_dir, item)
                    if os.path.exists(wav_path):
                        try:
                            with wave.open(wav_path, 'rb') as w:
                                if not params:
                                    params = w.getparams()
                                audio_data = w.readframes(w.getnframes())
                                frames.append(audio_data)
                        except Exception as e:
                            print(f"Error reading {wav_path}: {e}")
                            continue
            
            if not params:
                raise Exception("No valid audio data found")
            
            with wave.open(out_path, 'wb') as out_wav:
                out_wav.setparams(params)
                out_wav.writeframes(b''.join(frames))
            
            return True
        except Exception as e:
            messagebox.showerror("Audio Error", f"Error creating audio: {e}")
            return False 

    # Event Handlers
    def on_speak(self):
        """Handle speak button click"""
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to speak.")
            return
        
        # Update preview
        self.update_preview(text)
        
        # Convert to phonemes
        phoneme_seq = self.text_to_phonemes_enhanced(text)
        if not phoneme_seq:
            messagebox.showwarning("Warning", "No valid phonemes found in the text.")
            return
        
        # Update UI state
        self.speak_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress.start()
        self.status_label.config(text="Generating audio...")
        
        # Start playback in thread
        threading.Thread(target=self._play_audio_sequence, args=(phoneme_seq,), daemon=True).start()

    def on_stop(self):
        """Handle stop button click"""
        self.stop_requested = True
        pygame.mixer.music.stop()
        self._on_playback_finish()

    def clear_text(self):
        """Clear the text input"""
        self.text_input.delete("1.0", tk.END)
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.config(state=tk.DISABLED)

    def show_analysis(self):
        """Show detailed analysis in the analysis tab"""
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to analyze.")
            return
        
        self.analysis_input.delete("1.0", tk.END)
        self.analysis_input.insert("1.0", text)
        self.perform_analysis()
        
        # Switch to analysis tab
        for i in range(self.root.winfo_children()[0].index("end")):
            if "Analysis" in self.root.winfo_children()[0].tab(i, "text"):
                self.root.winfo_children()[0].select(i)
                break

    def save_audio(self):
        """Save the current audio to a file"""
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text first.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        
        if filename:
            phoneme_seq = self.text_to_phonemes_enhanced(text)
            if self.concatenate_audio(phoneme_seq, filename):
                messagebox.showinfo("Success", f"Audio saved to {filename}")

    def update_speed_label(self, *args):
        """Update the speed label"""
        speed = self.speed_var.get()
        self.speed_label.config(text=f"{speed:.1f}x")

    def update_preview(self, text):
        """Update the quick preview with phonemes"""
        try:
            phonemes = self.phoneme_converter.text_to_phoneme_string(text[:100])  # Limit for preview
            self.preview_text.config(state=tk.NORMAL)
            self.preview_text.delete("1.0", tk.END)
            self.preview_text.insert("1.0", f"Phonemes: {phonemes}")
            self.preview_text.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Preview error: {e}")

    def _play_audio_sequence(self, phoneme_seq):
        """Play the audio sequence in a separate thread"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                tmp_path = tmp_file.name
            
            # Generate audio
            if self.concatenate_audio(phoneme_seq, tmp_path):
                # Load and play
                pygame.mixer.music.load(tmp_path)
                
                # Apply speed if needed
                speed = self.speed_var.get()
                if speed != 1.0:
                    # For speed adjustment, we'd need more complex audio processing
                    # For now, just play at normal speed
                    pass
                
                pygame.mixer.music.play()
                
                self.root.after(0, lambda: self.status_label.config(text="Playing..."))
                
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                    if self.stop_requested:
                        pygame.mixer.music.stop()
                        break
            
            # Cleanup
            try:
                os.unlink(tmp_path)
            except:
                pass
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Playback Error", f"Error during playback: {e}"))
        finally:
            self.root.after(0, self._on_playback_finish)

    def _on_playback_finish(self):
        """Clean up after playback finishes"""
        self.stop_requested = False
        self.progress.stop()
        self.speak_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Ready to speak...")

    # Analysis Methods
    def perform_analysis(self):
        """Perform comprehensive linguistic analysis"""
        text = self.analysis_input.get("1.0", tk.END).strip()
        if not text:
            return
        
        try:
            # Perform analysis
            analysis_results = self.analyze_text_comprehensive(text)
            
            # Update analysis tabs
            self.update_phoneme_analysis(analysis_results)
            self.update_tokenization_analysis(analysis_results)
            self.update_statistics_analysis(analysis_results)
            
        except Exception as e:
            messagebox.showerror("Analysis Error", f"Error during analysis: {e}")

    def analyze_text_comprehensive(self, text):
        """Perform comprehensive text analysis"""
        results = {
            'original_text': text,
            'words': text.split(),
            'characters': list(text),
            'phonemes': [],
            'tokens': [],
            'clusters': [],
            'statistics': {}
        }
        
        # Tokenization
        for word in results['words']:
            if word.strip():
                tokens = self.phoneme_converter.tokenize_sinhala_text(word)
                results['tokens'].extend(tokens)
        
        # Phoneme conversion
        results['phonemes'] = self.phoneme_converter.text_to_phonemes(text)
        
        # Find consonant clusters
        for token in results['tokens']:
            if len(token) > 2 and '්' in token:
                results['clusters'].append(token)
        
        # Statistics
        results['statistics'] = {
            'total_characters': len(text),
            'total_words': len(results['words']),
            'total_phonemes': len(results['phonemes']),
            'total_tokens': len(results['tokens']),
            'consonant_clusters': len(results['clusters']),
            'unique_phonemes': len(set(results['phonemes'])),
            'character_frequency': self.calculate_frequency(results['characters']),
            'phoneme_frequency': self.calculate_frequency(results['phonemes'])
        }
        
        return results

    def calculate_frequency(self, items):
        """Calculate frequency of items"""
        frequency = {}
        for item in items:
            if item.strip():
                frequency[item] = frequency.get(item, 0) + 1
        return dict(sorted(frequency.items(), key=lambda x: x[1], reverse=True))

    def update_phoneme_analysis(self, analysis):
        """Update the phoneme analysis tab"""
        self.phoneme_result.config(state=tk.NORMAL)
        self.phoneme_result.delete("1.0", tk.END)
        
        content = "PHONEME BREAKDOWN ANALYSIS\n"
        content += "=" * 50 + "\n\n"
        
        content += f"Original Text: {analysis['original_text']}\n\n"
        
        content += "Phoneme Sequence:\n"
        content += " + ".join(analysis['phonemes']) + "\n\n"
        
        content += "Phoneme String:\n"
        content += "".join(analysis['phonemes']) + "\n\n"
        
        if self.show_phonetic_var.get():
            content += "Phoneme Frequency:\n"
            for phoneme, count in list(analysis['statistics']['phoneme_frequency'].items())[:20]:
                content += f"  {phoneme}: {count} times\n"
        
        self.phoneme_result.insert("1.0", content)
        self.phoneme_result.config(state=tk.DISABLED)

    def update_tokenization_analysis(self, analysis):
        """Update the tokenization analysis tab"""
        self.token_result.config(state=tk.NORMAL)
        self.token_result.delete("1.0", tk.END)
        
        content = "TOKENIZATION ANALYSIS\n"
        content += "=" * 50 + "\n\n"
        
        content += "Word Breakdown:\n"
        for i, word in enumerate(analysis['words']):
            if word.strip():
                tokens = self.phoneme_converter.tokenize_sinhala_text(word)
                content += f"{i+1}. '{word}' → {tokens}\n"
        
        content += "\nAll Tokens:\n"
        content += str(analysis['tokens']) + "\n\n"
        
        if self.show_clusters_var.get() and analysis['clusters']:
            content += "Consonant Clusters Found:\n"
            for cluster in analysis['clusters']:
                content += f"  {cluster}\n"
        
        if self.show_diacritics_var.get():
            content += "\nDiacritic Analysis:\n"
            diacritics = [char for char in analysis['characters'] 
                         if char in self.phoneme_converter.sinhala_diacritics]
            if diacritics:
                diacritic_freq = self.calculate_frequency(diacritics)
                for diacritic, count in diacritic_freq.items():
                    content += f"  {diacritic}: {count} times\n"
        
        self.token_result.insert("1.0", content)
        self.token_result.config(state=tk.DISABLED)

    def update_statistics_analysis(self, analysis):
        """Update the statistics analysis tab"""
        self.stats_result.config(state=tk.NORMAL)
        self.stats_result.delete("1.0", tk.END)
        
        stats = analysis['statistics']
        
        content = "STATISTICAL ANALYSIS\n"
        content += "=" * 50 + "\n\n"
        
        content += "Basic Statistics:\n"
        content += f"  Total Characters: {stats['total_characters']}\n"
        content += f"  Total Words: {stats['total_words']}\n"
        content += f"  Total Phonemes: {stats['total_phonemes']}\n"
        content += f"  Total Tokens: {stats['total_tokens']}\n"
        content += f"  Consonant Clusters: {stats['consonant_clusters']}\n"
        content += f"  Unique Phonemes: {stats['unique_phonemes']}\n\n"
        
        content += "Character Frequency (Top 20):\n"
        for char, count in list(stats['character_frequency'].items())[:20]:
            if char.strip():
                content += f"  '{char}': {count} times\n"
        
        content += "\nPhoneme Coverage Analysis:\n"
        # Check which phonemes are available as audio files
        available_phonemes = self.get_available_phonemes()
        used_phonemes = set(analysis['phonemes'])
        
        coverage = len(used_phonemes.intersection(available_phonemes)) / len(used_phonemes) * 100 if used_phonemes else 0
        content += f"  Audio Coverage: {coverage:.1f}%\n"
        
        missing_phonemes = used_phonemes - available_phonemes
        if missing_phonemes:
            content += f"  Missing Audio Files: {sorted(missing_phonemes)}\n"
        
        self.stats_result.insert("1.0", content)
        self.stats_result.config(state=tk.DISABLED)

    # Phoneme Explorer Methods
    def refresh_phoneme_list(self):
        """Refresh the phoneme list in the explorer"""
        # Clear existing items
        for item in self.phoneme_tree.get_children():
            self.phoneme_tree.delete(item)
        
        # Get available phoneme files
        if os.path.exists(self.phonemes_dir):
            files = [f for f in os.listdir(self.phonemes_dir) if f.endswith('.wav')]
            
            for filename in sorted(files):
                phoneme = filename[:-4]  # Remove .wav extension
                filepath = os.path.join(self.phonemes_dir, filename)
                
                # Check file size to determine status
                try:
                    size = os.path.getsize(filepath)
                    status = "Available" if size > 0 else "Empty"
                except:
                    status = "Error"
                
                self.phoneme_tree.insert("", tk.END, values=(phoneme, filename, status))

    def play_selected_phoneme(self):
        """Play the selected phoneme"""
        selection = self.phoneme_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a phoneme to play.")
            return
        
        item = self.phoneme_tree.item(selection[0])
        filename = item['values'][1]
        filepath = os.path.join(self.phonemes_dir, filename)
        
        if os.path.exists(filepath):
            try:
                pygame.mixer.music.load(filepath)
                pygame.mixer.music.play()
            except Exception as e:
                messagebox.showerror("Playback Error", f"Error playing {filename}: {e}")
        else:
            messagebox.showerror("File Error", f"File not found: {filename}")

    def generate_phoneme_report(self):
        """Generate a comprehensive phoneme report"""
        report_data = {
            'total_phonemes': 0,
            'available_phonemes': 0,
            'missing_phonemes': [],
            'file_sizes': {},
            'status_summary': {}
        }
        
        if os.path.exists(self.phonemes_dir):
            files = [f for f in os.listdir(self.phonemes_dir) if f.endswith('.wav')]
            report_data['total_phonemes'] = len(files)
            
            for filename in files:
                filepath = os.path.join(self.phonemes_dir, filename)
                try:
                    size = os.path.getsize(filepath)
                    report_data['file_sizes'][filename] = size
                    if size > 0:
                        report_data['available_phonemes'] += 1
                except:
                    report_data['missing_phonemes'].append(filename)
        
        # Show report in a new window
        self.show_phoneme_report(report_data)

    def show_phoneme_report(self, report_data):
        """Show phoneme report in a new window"""
        report_window = tk.Toplevel(self.root)
        report_window.title("Phoneme Report")
        report_window.geometry("600x400")
        
        report_text = scrolledtext.ScrolledText(report_window, font=("Consolas", 10))
        report_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        content = "PHONEME SYSTEM REPORT\n"
        content += "=" * 40 + "\n\n"
        content += f"Total Phoneme Files: {report_data['total_phonemes']}\n"
        content += f"Available Files: {report_data['available_phonemes']}\n"
        content += f"Missing/Empty Files: {len(report_data['missing_phonemes'])}\n\n"
        
        if report_data['missing_phonemes']:
            content += "Missing Files:\n"
            for filename in report_data['missing_phonemes']:
                content += f"  {filename}\n"
        
        content += "\nFile Sizes:\n"
        for filename, size in sorted(report_data['file_sizes'].items()):
            content += f"  {filename}: {size} bytes\n"
        
        report_text.insert("1.0", content)
        report_text.config(state=tk.DISABLED)

    # Utility Methods
    def get_available_phonemes(self):
        """Get list of available phoneme audio files"""
        available = set()
        if os.path.exists(self.phonemes_dir):
            files = [f for f in os.listdir(self.phonemes_dir) if f.endswith('.wav')]
            for filename in files:
                phoneme = filename[:-4]  # Remove .wav extension
                available.add(phoneme)
        return available

    def check_phoneme_files(self):
        """Check if phoneme files exist and update UI accordingly"""
        if not os.path.exists(self.phonemes_dir):
            self.status_label.config(text="Phonemes directory not found!")
            return
        
        files = [f for f in os.listdir(self.phonemes_dir) if f.endswith('.wav')]
        if not files:
            self.status_label.config(text="No phoneme files found! Please generate phonemes first.")
        else:
            self.status_label.config(text=f"Ready to speak... ({len(files)} phonemes loaded)")

    # Settings Methods
    def browse_phoneme_dir(self):
        """Browse for phonemes directory"""
        directory = filedialog.askdirectory(initialdir=self.phonemes_dir)
        if directory:
            self.phoneme_dir_var.set(directory)
            self.phonemes_dir = directory
            self.check_phoneme_files()

    def save_settings(self):
        """Save settings to file"""
        settings = {
            'sample_rate': self.sample_rate_var.get(),
            'word_pause': self.word_pause_var.get(),
            'sentence_pause': self.sentence_pause_var.get(),
            'phonemes_dir': self.phoneme_dir_var.get(),
            'show_clusters': self.show_clusters_var.get(),
            'show_diacritics': self.show_diacritics_var.get(),
            'show_phonetic': self.show_phonetic_var.get()
        }
        
        try:
            with open('tts_settings.json', 'w') as f:
                json.dump(settings, f, indent=2)
            messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving settings: {e}")

    def reset_settings(self):
        """Reset settings to defaults"""
        self.sample_rate_var.set("16000")
        self.word_pause_var.set(0.3)
        self.sentence_pause_var.set(0.6)
        self.phoneme_dir_var.set("phonemes")
        self.show_clusters_var.set(True)
        self.show_diacritics_var.set(True)
        self.show_phonetic_var.set(True)
        messagebox.showinfo("Success", "Settings reset to defaults!")

    def copy_analysis(self):
        """Copy analysis results to clipboard"""
        try:
            # Get current tab content
            current_tab = self.analysis_notebook.select()
            tab_text = self.analysis_notebook.tab(current_tab, "text")
            
            if "Phonemes" in tab_text:
                content = self.phoneme_result.get("1.0", tk.END)
            elif "Tokenization" in tab_text:
                content = self.token_result.get("1.0", tk.END)
            elif "Statistics" in tab_text:
                content = self.stats_result.get("1.0", tk.END)
            else:
                content = "No content to copy"
            
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            messagebox.showinfo("Success", "Analysis copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Error copying analysis: {e}")

    def save_analysis(self):
        """Save analysis results to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"Phoneme Analysis:\n{self.phoneme_result.get('1.0', tk.END)}\n\n")
                    f.write(f"Tokenization Analysis:\n{self.token_result.get('1.0', tk.END)}\n\n")
                    f.write(f"Statistics Analysis:\n{self.stats_result.get('1.0', tk.END)}\n")
                messagebox.showinfo("Success", f"Analysis saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving analysis: {e}")

    def run(self):
        """Run the application"""
        # Load settings if they exist
        try:
            with open('tts_settings.json', 'r') as f:
                settings = json.load(f)
                self.sample_rate_var.set(settings.get('sample_rate', '16000'))
                self.word_pause_var.set(settings.get('word_pause', 0.3))
                self.sentence_pause_var.set(settings.get('sentence_pause', 0.6))
                self.phoneme_dir_var.set(settings.get('phonemes_dir', 'phonemes'))
                self.show_clusters_var.set(settings.get('show_clusters', True))
                self.show_diacritics_var.set(settings.get('show_diacritics', True))
                self.show_phonetic_var.set(settings.get('show_phonetic', True))
        except:
            pass
        
        # Initialize phoneme list
        self.refresh_phoneme_list()
        
        # Start the GUI
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = EnhancedSinhalaTTS()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc() 