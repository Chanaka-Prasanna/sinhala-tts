import re
import os
from typing import List, Tuple, Dict

class SinhalaTextToPhoneme:
    def __init__(self):
        # Import the phoneme system from the main file
        self.phoneme_system = self._init_phoneme_system()
        
        # Unicode ranges for Sinhala characters
        self.sinhala_vowels = set('අආඇඈඉඊඋඌඍඎඏඐඑඒඓඔඕඖ')
        self.sinhala_consonants = set('කඛගඝඞචඡජඣඤටඨඩඪණතථදධනපඵබභමයරලවශෂසහළෆ')
        self.sinhala_diacritics = set('ාැෑිීුූෘෲෟෳේෛෙොෝෞ')
        self.sinhala_special = set('ංඃ්')
        
        # Contextual pronunciation rules
        self.pronunciation_rules = self._load_pronunciation_rules()
        
    def _init_phoneme_system(self):
        """Initialize the phoneme system with comprehensive mappings"""
        return {
            # Base vowel sounds
            'අ': 'a', 'ආ': 'aa', 'ඇ': 'ae', 'ඈ': 'aae',
            'ඉ': 'i', 'ඊ': 'ii', 'උ': 'u', 'ඌ': 'uu',
            'ඍ': 'ri', 'ඎ': 'rii', 'ඏ': 'li', 'ඐ': 'lii',
            'එ': 'e', 'ඒ': 'ee', 'ඓ': 'ai', 'ඔ': 'o',
            'ඕ': 'oo', 'ඖ': 'au',
            
            # Base consonants with inherent 'a'
            'ක': 'ka', 'ඛ': 'kha', 'ග': 'ga', 'ඝ': 'gha', 'ඞ': 'nga',
            'ච': 'cha', 'ඡ': 'chha', 'ජ': 'ja', 'ඣ': 'jha', 'ඤ': 'nya',
            'ට': 'ta', 'ඨ': 'tha', 'ඩ': 'da', 'ඪ': 'dha', 'ණ': 'na',
            'ත': 'tha', 'ථ': 'thha', 'ද': 'da', 'ධ': 'dha', 'න': 'na',
            'ප': 'pa', 'ඵ': 'pha', 'බ': 'ba', 'භ': 'bha', 'ම': 'ma',
            'ය': 'ya', 'ර': 'ra', 'ල': 'la', 'ව': 'wa',
            'ශ': 'sha', 'ෂ': 'sha', 'ස': 'sa', 'හ': 'ha',
            'ළ': 'lla', 'ෆ': 'fa',
            
            # Vowel diacritics
            'ා': 'aa', 'ැ': 'ae', 'ෑ': 'aae', 'ි': 'i', 'ී': 'ii',
            'ු': 'u', 'ූ': 'uu', 'ෘ': 'ri', 'ෲ': 'rii',
            'ෟ': 'li', 'ෳ': 'lii', 'ේ': 'ee', 'ෛ': 'ai',
            'ෙ': 'e', 'ො': 'o', 'ෝ': 'oo', 'ෞ': 'au',
            
            # Special characters
            'ං': 'ng', 'ඃ': 'h', '්': ''
        }
    
    def _load_pronunciation_rules(self):
        """Load contextual pronunciation rules"""
        return {
            # Consonant clusters that have special pronunciations
            'consonant_clusters': {
                'ක්ර': 'kra', 'ග්ර': 'gra', 'ත්ර': 'thra', 'ද්ර': 'dra',
                'ප්ර': 'pra', 'බ්ර': 'bra', 'ම්ර': 'mra', 'ව්ර': 'wra',
                'ක්ල': 'kla', 'ග්ල': 'gla', 'ප්ල': 'pla', 'බ්ල': 'bla',
                'ස්ත': 'stha', 'ස්ථ': 'sthha', 'ස්ප': 'spa', 'ස්ක': 'ska',
                'න්ද': 'nda', 'න්ත': 'ntha', 'ම්ප': 'mpa', 'ම්බ': 'mba',
                'ඞ්ග': 'ngga', 'ඤ්ජ': 'nyja', 'ණ්ඩ': 'nda', 'න්ධ': 'ndha',
                'ක්ෂ': 'ksha', 'ත්්‍ර': 'thra', 'ද්්‍ර': 'dhra'
            },
            
            # Word position rules
            'word_final_modifications': {
                'ං': 'ng', 'න්': 'n', 'ම්': 'm', 'ල්': 'l', 'ර්': 'r'
            },
            
            # Vowel modifications in certain contexts
            'vowel_context_rules': {
                ('i', 'following_ya'): 'ii',
                ('u', 'following_wa'): 'uu',
                ('e', 'word_final'): 'e',
                ('o', 'word_final'): 'o'
            },
            
            # Common sound changes
            'sound_changes': {
                'ත්': 'th',  # ත් without vowel
                'ප්': 'p',   # ප් without vowel
                'ක්': 'k',   # ක් without vowel
                'ම්': 'm',   # ම් without vowel
                'න්': 'n',   # න් without vowel
                'ර්': 'r',   # ර් without vowel
                'ල්': 'l'    # ල් without vowel
            }
        }
    
    def tokenize_sinhala_text(self, text: str) -> List[str]:
        """Tokenize Sinhala text into characters and character clusters"""
        tokens = []
        i = 0
        
        while i < len(text):
            char = text[i]
            
            # Skip whitespace and punctuation
            if char.isspace() or char in '.,!?;:':
                tokens.append(char)
                i += 1
                continue
            
            # Check for consonant clusters (consonant + hal kirima + consonant)
            if (i + 2 < len(text) and 
                char in self.sinhala_consonants and 
                text[i + 1] == '්' and 
                text[i + 2] in self.sinhala_consonants):
                
                # Look for additional diacritics after the cluster
                cluster = text[i:i+3]
                j = i + 3
                while (j < len(text) and 
                       text[j] in self.sinhala_diacritics):
                    cluster += text[j]
                    j += 1
                tokens.append(cluster)
                i = j
                continue
            
            # Check for consonant + diacritics
            if char in self.sinhala_consonants:
                consonant_group = char
                j = i + 1
                while (j < len(text) and 
                       text[j] in self.sinhala_diacritics.union({'්'})):
                    consonant_group += text[j]
                    j += 1
                tokens.append(consonant_group)
                i = j
                continue
            
            # Single character (vowel, special character, etc.)
            tokens.append(char)
            i += 1
        
        return tokens
    
    def convert_token_to_phoneme(self, token: str, context: Dict = None) -> str:
        """Convert a single token to its phonetic representation"""
        if not token or token.isspace():
            return ' '
        
        if token in '.,!?;:':
            return token
        
        # Handle consonant clusters first
        for cluster, phoneme in self.pronunciation_rules['consonant_clusters'].items():
            if token.startswith(cluster):
                remaining = token[len(cluster):]
                cluster_phoneme = phoneme
                
                # Handle any additional diacritics
                if remaining:
                    for diacritic in remaining:
                        if diacritic in self.phoneme_system:
                            # Modify the cluster based on the diacritic
                            if cluster_phoneme.endswith('a') and diacritic != 'ා':
                                cluster_phoneme = cluster_phoneme[:-1] + self.phoneme_system[diacritic]
                            elif diacritic == 'ා':
                                cluster_phoneme = cluster_phoneme[:-1] + 'aa'
                            else:
                                cluster_phoneme += self.phoneme_system[diacritic]
                
                return cluster_phoneme
        
        # Handle single vowels
        if token in self.sinhala_vowels:
            return self.phoneme_system[token]
        
        # Handle consonants with diacritics
        if len(token) > 1 and token[0] in self.sinhala_consonants:
            consonant = token[0]
            base_sound = self.phoneme_system[consonant]
            
            # Remove inherent 'a' if there are diacritics
            if len(token) > 1 and base_sound.endswith('a'):
                base_sound = base_sound[:-1]
            
            # Apply diacritics
            for i, diacritic in enumerate(token[1:], 1):
                if diacritic == '්':  # hal kirima - removes vowel
                    continue
                elif diacritic in self.phoneme_system:
                    vowel_sound = self.phoneme_system[diacritic]
                    base_sound += vowel_sound
            
            # If no vowel added and original had inherent 'a', add it back
            if len(token) == 1 or (len(token) > 1 and all(d == '්' for d in token[1:])):
                if not any(d in self.sinhala_diacritics for d in token[1:]):
                    if token.endswith('්'):
                        pass  # No vowel for hal kirima
                    else:
                        base_sound += 'a'  # Restore inherent vowel
            
            return base_sound
        
        # Handle single consonants
        if token in self.sinhala_consonants:
            return self.phoneme_system[token]
        
        # Handle special characters
        if token in self.sinhala_special:
            return self.phoneme_system[token]
        
        # Handle English or other characters
        return token.lower()
    
    def apply_contextual_rules(self, phonemes: List[str], word_context: str = None) -> List[str]:
        """Apply contextual pronunciation rules to phoneme sequence"""
        if not phonemes:
            return phonemes
        
        modified_phonemes = phonemes.copy()
        
        # Apply word-final modifications
        if word_context == 'word_final' and phonemes:
            last_phoneme = phonemes[-1]
            for pattern, replacement in self.pronunciation_rules['word_final_modifications'].items():
                if last_phoneme.endswith(pattern):
                    modified_phonemes[-1] = replacement
        
        # Apply sound changes based on adjacent sounds
        for i in range(len(modified_phonemes) - 1):
            current = modified_phonemes[i]
            next_phoneme = modified_phonemes[i + 1]
            
            # Voicing assimilation rules
            if current.endswith(('k', 'p', 't')) and next_phoneme.startswith(('g', 'b', 'd')):
                # Voiceless consonant before voiced - partial voicing
                voiced_map = {'k': 'g', 'p': 'b', 't': 'd'}
                if current[-1] in voiced_map:
                    modified_phonemes[i] = current[:-1] + voiced_map[current[-1]]
        
        return modified_phonemes
    
    def text_to_phonemes(self, text: str) -> List[str]:
        """Convert Sinhala text to phonemes"""
        words = text.split()
        all_phonemes = []
        
        for word in words:
            if not word.strip():
                all_phonemes.append(' ')
                continue
            
            tokens = self.tokenize_sinhala_text(word)
            word_phonemes = []
            
            for i, token in enumerate(tokens):
                context = {
                    'position': 'initial' if i == 0 else 'medial' if i < len(tokens) - 1 else 'final',
                    'word_length': len(tokens)
                }
                
                phoneme = self.convert_token_to_phoneme(token, context)
                if phoneme:
                    word_phonemes.append(phoneme)
            
            # Apply contextual rules
            word_phonemes = self.apply_contextual_rules(word_phonemes, 'word_final')
            all_phonemes.extend(word_phonemes)
            all_phonemes.append(' ')  # Space between words
        
        # Remove trailing space
        if all_phonemes and all_phonemes[-1] == ' ':
            all_phonemes.pop()
        
        return all_phonemes
    
    def text_to_phoneme_string(self, text: str) -> str:
        """Convert text to a single phoneme string"""
        phonemes = self.text_to_phonemes(text)
        return ''.join(phonemes)

def demonstrate_conversion():
    """Demonstrate the text-to-phoneme conversion"""
    converter = SinhalaTextToPhoneme()
    
    # Test examples
    test_texts = [
        "ගම",      # village
        "කතා",     # story
        "ප්‍රේම",   # love (with consonant cluster)
        "සිංහල",   # Sinhala
        "මගේ නම",  # my name
        "ස්කූල",   # school (with consonant cluster)
        "ක්‍රීඩා",  # sports
        "අම්මා",   # mother
        "ගෙදර",    # home
        "පොත්"     # book (word-final)
    ]
    
    print("Sinhala Text-to-Phoneme Conversion Demo")
    print("=" * 50)
    
    for text in test_texts:
        phonemes = converter.text_to_phonemes(text)
        phoneme_string = converter.text_to_phoneme_string(text)
        
        print(f"Text: {text}")
        print(f"Phonemes: {phonemes}")
        print(f"Phoneme String: {phoneme_string}")
        print("-" * 30)

if __name__ == "__main__":
    demonstrate_conversion() 