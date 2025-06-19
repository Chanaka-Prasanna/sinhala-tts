"""
Fixed Pronunciation Tuning Tool for Sinhala TTS
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pyttsx3
import json

class FixedPronunciationTuner:
    def __init__(self, root):
        self.root = root
        self.root.title("Sinhala Pronunciation Tuner")
        self.root.geometry("600x500")
        
        self.tts_engine = pyttsx3.init()
        
        # Initialize custom mappings first
        self.custom_mappings = self.load_custom_mappings()
        
        # Load basic mappings for reference
        self.basic_mappings = self.load_basic_mappings()
        
        # Create widgets after initialization
        self.create_widgets()
    
    def load_basic_mappings(self):
        """Load basic Sinhala mappings for reference"""
        return {
            'අ': 'uh', 'ආ': 'ah', 'ඇ': 'ae', 'ඈ': 'aeh',
            'ඉ': 'i', 'ඊ': 'ee', 'උ': 'u', 'ඌ': 'oo',
            'එ': 'e', 'ඒ': 'ay', 'ඓ': 'ahy', 'ඔ': 'o', 'ඕ': 'oh', 'ඖ': 'ow',
            'ක': 'ka', 'ග': 'ga', 'ච': 'cha', 'ජ': 'ja', 'ට': 'ta', 'ඩ': 'da',
            'ත': 'tha', 'ද': 'da', 'ප': 'pa', 'බ': 'ba', 'ම': 'ma', 'ය': 'ya',
            'ර': 'ra', 'ල': 'la', 'ව': 'va', 'ශ': 'sha', 'ස': 'sa', 'හ': 'ha',
            'න': 'na', 'ළ': 'lla', 'ෆ': 'fa'
        }
    
    def load_custom_mappings(self):
        """Load custom pronunciation mappings"""
        try:
            with open('custom_pronunciations.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except Exception as e:
            print(f"Error loading custom mappings: {e}")
            return {}
    
    def save_custom_mappings(self):
        """Save custom pronunciation mappings"""
        try:
            with open('custom_pronunciations.json', 'w', encoding='utf-8') as f:
                json.dump(self.custom_mappings, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save mappings: {e}")
            return False
    
    def create_widgets(self):
        """Create tuning interface"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        ttk.Label(main_frame, text="Sinhala Pronunciation Tuner", 
                 font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Character input
        ttk.Label(main_frame, text="Sinhala Character:").grid(row=1, column=0, sticky=tk.W)
        self.char_entry = ttk.Entry(main_frame, font=("Noto Sans Sinhala", 12), width=10)
        self.char_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Current pronunciation
        ttk.Label(main_frame, text="Current Pronunciation:").grid(row=2, column=0, sticky=tk.W)
        self.current_label = ttk.Label(main_frame, text="", font=("Consolas", 10))
        self.current_label.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # New pronunciation
        ttk.Label(main_frame, text="New Pronunciation:").grid(row=3, column=0, sticky=tk.W)
        self.new_entry = ttk.Entry(main_frame, font=("Consolas", 10))
        self.new_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(btn_frame, text="Load Character", command=self.load_character).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(btn_frame, text="Test Current", command=self.test_current).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(btn_frame, text="Test New", command=self.test_new).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(btn_frame, text="Save Mapping", command=self.save_mapping).grid(row=0, column=3, padx=(0, 5))
        
        # Word testing
        ttk.Label(main_frame, text="Test Full Word:").grid(row=5, column=0, sticky=tk.W, pady=(20, 5))
        self.word_entry = ttk.Entry(main_frame, font=("Noto Sans Sinhala", 12))
        self.word_entry.grid(row=5, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
        ttk.Button(main_frame, text="Test Word", command=self.test_word).grid(row=5, column=2, padx=(5, 0))
        
        # Custom mappings display
        ttk.Label(main_frame, text="Custom Mappings:").grid(row=6, column=0, columnspan=3, sticky=tk.W, pady=(20, 5))
        
        self.mappings_listbox = tk.Listbox(main_frame, height=10)
        self.mappings_listbox.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Control buttons
        ctrl_frame = ttk.Frame(main_frame)
        ctrl_frame.grid(row=8, column=0, columnspan=3)
        
        ttk.Button(ctrl_frame, text="Export Mappings", command=self.export_mappings).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(ctrl_frame, text="Import Mappings", command=self.import_mappings).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(ctrl_frame, text="Delete Selected", command=self.delete_mapping).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(ctrl_frame, text="Reset All", command=self.reset_mappings).grid(row=0, column=3)
        
        # Configure weights
        main_frame.rowconfigure(7, weight=1)
        
        # Update display
        self.update_mappings_display()
        
        # Bind events
        self.char_entry.bind('<KeyRelease>', self.on_char_change)
    
    def on_char_change(self, event=None):
        """Handle character input change"""
        char = self.char_entry.get().strip()
        if char:
            # Get current pronunciation
            current = self.basic_mappings.get(char, "Unknown")
            self.current_label.config(text=current)
            
            # Load custom pronunciation if exists
            if char in self.custom_mappings:
                self.new_entry.delete(0, tk.END)
                self.new_entry.insert(0, self.custom_mappings[char])
            else:
                self.new_entry.delete(0, tk.END)
    
    def load_character(self):
        """Load character for testing"""
        self.on_char_change()
    
    def test_current(self):
        """Test current pronunciation"""
        current = self.current_label.cget("text")
        if current and current != "Unknown":
            self.speak_text(current)
        else:
            messagebox.showwarning("Warning", "No current pronunciation available!")
    
    def test_new(self):
        """Test new pronunciation"""
        new = self.new_entry.get().strip()
        if new:
            self.speak_text(new)
        else:
            messagebox.showwarning("Warning", "Please enter a new pronunciation!")
    
    def test_word(self):
        """Test pronunciation of a full word"""
        word = self.word_entry.get().strip()
        if not word:
            messagebox.showwarning("Warning", "Please enter a word to test!")
            return
        
        # Convert word using current mappings
        phonetic = ""
        for char in word:
            if char in self.custom_mappings:
                phonetic += self.custom_mappings[char]
            elif char in self.basic_mappings:
                phonetic += self.basic_mappings[char]
            else:
                phonetic += char
        
        messagebox.showinfo("Word Pronunciation", f"Word: {word}\nPhonetic: {phonetic}")
        self.speak_text(phonetic)
    
    def speak_text(self, text):
        """Speak the given text"""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            messagebox.showerror("Error", f"Speech failed: {e}")
    
    def save_mapping(self):
        """Save the new pronunciation mapping"""
        char = self.char_entry.get().strip()
        new_pronunciation = self.new_entry.get().strip()
        
        if not char or not new_pronunciation:
            messagebox.showwarning("Warning", "Please enter both character and pronunciation!")
            return
        
        self.custom_mappings[char] = new_pronunciation
        if self.save_custom_mappings():
            self.update_mappings_display()
            messagebox.showinfo("Success", f"Saved: {char} → {new_pronunciation}")
    
    def update_mappings_display(self):
        """Update the mappings display"""
        self.mappings_listbox.delete(0, tk.END)
        for char, pronunciation in sorted(self.custom_mappings.items()):
            self.mappings_listbox.insert(tk.END, f"{char} → {pronunciation}")
    
    def delete_mapping(self):
        """Delete selected mapping"""
        selection = self.mappings_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a mapping to delete!")
            return
        
        selected_text = self.mappings_listbox.get(selection[0])
        char = selected_text.split(' → ')[0]
        
        if messagebox.askyesno("Confirm", f"Delete mapping for '{char}'?"):
            if char in self.custom_mappings:
                del self.custom_mappings[char]
                self.save_custom_mappings()
                self.update_mappings_display()
    
    def export_mappings(self):
        """Export mappings to file"""
        from tkinter import filedialog
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Export Custom Mappings"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.custom_mappings, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("Success", f"Mappings exported to: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {e}")
    
    def import_mappings(self):
        """Import mappings from file"""
        from tkinter import filedialog
        
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Import Custom Mappings"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    imported = json.load(f)
                
                self.custom_mappings.update(imported)
                self.save_custom_mappings()
                self.update_mappings_display()
                
                messagebox.showinfo("Success", f"Imported {len(imported)} mappings")
            except Exception as e:
                messagebox.showerror("Error", f"Import failed: {e}")
    
    def reset_mappings(self):
        """Reset all custom mappings"""
        if messagebox.askyesno("Confirm", "Reset all custom mappings?"):
            self.custom_mappings.clear()
            self.save_custom_mappings()
            self.update_mappings_display()

def main():
    root = tk.Tk()
    app = FixedPronunciationTuner(root)
    root.mainloop()

if __name__ == "__main__":
    main()