import os
import re
from google.cloud import texttospeech

# 2) Set up Google Cloud credentials
# The script will automatically look for the JSON key file in the current directory
def setup_google_credentials():
    """Setup Google Cloud credentials automatically"""
    json_files = [f for f in os.listdir('.') if f.endswith('.json') and 'projects' in f]
    if json_files:
        credentials_path = os.path.abspath(json_files[0])
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        print(f"Using credentials: {credentials_path}")
        return True
    else:
        print("No Google Cloud JSON key file found!")
        print("Please place your service account JSON key in this directory.")
        return False

# 3) Comprehensive Sinhala Phoneme System with contextual rules
class SinhalaPhonemeSystem:
    def __init__(self):
        # Base vowel sounds (independent vowels)
        self.base_vowels = {
            'අ': 'a', 'ආ': 'aa', 'ඇ': 'ae', 'ඈ': 'aae',
            'ඉ': 'i', 'ඊ': 'ii', 'උ': 'u', 'ඌ': 'uu',
            'ඍ': 'ri', 'ඎ': 'rii', 'ඏ': 'li', 'ඐ': 'lii',
            'එ': 'e', 'ඒ': 'ee', 'ඓ': 'ai', 'ඔ': 'o',
            'ඕ': 'oo', 'ඖ': 'au'
        }
        
        # Base consonants with inherent 'a' sound
        self.base_consonants = {
            # Velar stops
            'ක': 'ka', 'ඛ': 'kha', 'ග': 'ga', 'ඝ': 'gha', 'ඞ': 'nga',
            # Palatal stops  
            'ච': 'cha', 'ඡ': 'chha', 'ජ': 'ja', 'ඣ': 'jha', 'ඤ': 'nya',
            # Retroflex stops
            'ට': 'ta', 'ඨ': 'tha', 'ඩ': 'da', 'ඪ': 'dha', 'ණ': 'na',
            # Dental stops
            'ත': 'tha', 'ථ': 'thha', 'ද': 'da', 'ධ': 'dha', 'න': 'na',
            # Labial stops
            'ප': 'pa', 'ඵ': 'pha', 'බ': 'ba', 'භ': 'bha', 'ම': 'ma',
            # Sonorants
            'ය': 'ya', 'ර': 'ra', 'ල': 'la', 'ව': 'wa',
            # Sibilants and aspirates
            'ශ': 'sha', 'ෂ': 'sha', 'ස': 'sa', 'හ': 'ha',
            # Additional
            'ළ': 'lla', 'ෆ': 'fa'
        }
        
        # Vowel diacritics (matras)
        self.vowel_diacritics = {
            'ා': 'aa', 'ැ': 'ae', 'ෑ': 'aae', 'ි': 'i', 'ී': 'ii',
            'ු': 'u', 'ූ': 'uu', 'ෘ': 'ri', 'ෲ': 'rii',
            'ෟ': 'li', 'ෳ': 'lii', 'ේ': 'ee', 'ෛ': 'ai',
            'ෙ': 'e', 'ො': 'o', 'ෝ': 'oo', 'ෞ': 'au'
        }
        
        # Special characters
        self.special_chars = {
            'ං': 'ng', 'ඃ': 'h', '්': ''  # hal kirima (vowel killer)
        }
        
        # Contextual pronunciation rules
        self.contextual_rules = {
            # Consonant clusters and combinations
            'consonant_clusters': {
                'ක්ර': 'kra', 'ග්ර': 'gra', 'ත්ර': 'thra', 'ද්ර': 'dra',
                'ප්ර': 'pra', 'බ්ර': 'bra', 'ම්ර': 'mra', 'ව්ර': 'wra',
                'ක්ල': 'kla', 'ග්ල': 'gla', 'ප්ල': 'pla', 'බ්ල': 'bla',
                'ස්ත': 'stha', 'ස්ථ': 'sthha', 'ස්ප': 'spa', 'ස්ක': 'ska',
                'න්ද': 'nda', 'න්ත': 'ntha', 'ම්ප': 'mpa', 'ම්බ': 'mba',
                'ඞ්ග': 'ngga', 'ඤ්ජ': 'nyja', 'ණ්ඩ': 'nda', 'න්ධ': 'ndha'
            },
            # Position-dependent variations
            'word_initial': {
                'ර': 'ra', 'ල': 'la', 'ව': 'wa', 'ය': 'ya'
            },
            'word_medial': {
                'ර': 'ra', 'ල': 'la', 'ව': 'wa', 'ය': 'ya'
            },
            'word_final': {
                'ර': 'ra', 'ල': 'la', 'ව': 'wa', 'ය': 'ya',
                'ං': 'ng', 'න්': 'n', 'ම්': 'm', 'ල්': 'l'
            }
        }
        
        # Phonetic variations for same characters in different contexts
        self.phonetic_variations = {
            # Different pronunciations of same character
            'ත': ['tha', 'ta'],  # Can be pronounced as both
            'ද': ['da', 'dha'],  # Contextual variation
            'ධ': ['dha', 'da'],  # Sometimes softer
            'ප': ['pa', 'ba'],   # In some contexts sounds like 'ba'
            'ක': ['ka', 'ga'],   # Can be voiced in some contexts
            'ච': ['cha', 'ja'],  # Can be voiced
            'ට': ['ta', 'da'],   # Retroflex variation
            'ල': ['la', 'lla'],  # Standard vs retroflex
            'ව': ['wa', 'va'],   # 'w' vs 'v' sound
            'ය': ['ya', 'ja'],   # Sometimes sounds like 'ja'
        }
        
        # Vowel harmony and modification rules
        self.vowel_harmony = {
            'front_vowels': ['i', 'ii', 'e', 'ee', 'ae', 'aae'],
            'back_vowels': ['u', 'uu', 'o', 'oo', 'au'],
            'central_vowels': ['a', 'aa']
        }

    def get_all_phonemes(self):
        """Generate comprehensive set of all possible phonemes"""
        phonemes = set()
        
        # 1. Basic vowel sounds
        phonemes.update(self.base_vowels.values())
        phonemes.update(self.vowel_diacritics.values())
        
        # 2. Basic consonant sounds (with inherent 'a')
        for cons in self.base_consonants.values():
            phonemes.add(cons)
            # Also add pure consonant (without vowel)
            if cons.endswith('a'):
                phonemes.add(cons[:-1])
        
        # 3. Consonant + vowel combinations
        for cons_char, cons_sound in self.base_consonants.items():
            cons_base = cons_sound[:-1] if cons_sound.endswith('a') else cons_sound
            for vowel_sound in self.vowel_diacritics.values():
                phonemes.add(cons_base + vowel_sound)
            for vowel_sound in self.base_vowels.values():
                phonemes.add(cons_base + vowel_sound)
        
        # 4. Consonant clusters
        phonemes.update(self.contextual_rules['consonant_clusters'].values())
        
        # 5. Add consonant clusters with different vowels
        for cluster_sound in self.contextual_rules['consonant_clusters'].values():
            # Remove the inherent 'a' if present
            if cluster_sound.endswith('a'):
                cluster_base = cluster_sound[:-1]
            else:
                cluster_base = cluster_sound
                
            for vowel_sound in self.vowel_diacritics.values():
                phonemes.add(cluster_base + vowel_sound)
            for vowel_sound in self.base_vowels.values():
                phonemes.add(cluster_base + vowel_sound)
        
        # 6. Phonetic variations
        for variations in self.phonetic_variations.values():
            phonemes.update(variations)
            # Add variations with vowels
            for var in variations:
                var_base = var[:-1] if var.endswith('a') else var
                for vowel_sound in self.vowel_diacritics.values():
                    phonemes.add(var_base + vowel_sound)
                for vowel_sound in self.base_vowels.values():
                    phonemes.add(var_base + vowel_sound)
        
        # 7. Special sounds
        phonemes.update(self.special_chars.values())
        
        # 8. Additional common sound combinations
        additional_sounds = [
            # Nasalized vowels
            'an', 'ang', 'am', 'ing', 'ung', 'eng', 'ong',
            # Aspirated combinations
            'kha', 'gha', 'cha', 'jha', 'tha', 'dha', 'pha', 'bha',
            # Retroflex sounds
            'tra', 'dra', 'nda', 'nta',
            # Sibilant combinations
            'sha', 'shha', 'sri', 'sra', 'sla',
            # Liquid combinations
            'rya', 'lya', 'wya', 'rwa', 'lwa',
            # Dental vs retroflex distinction
            'tha', 'ta', 'dha', 'da', 'na', 'nna',
            # Voiced/voiceless variations
            'ka', 'ga', 'cha', 'ja', 'ta', 'da', 'pa', 'ba'
        ]
        phonemes.update(additional_sounds)
        
        # 9. Length variations (short and long)
        length_variants = []
        for phoneme in list(phonemes):
            if phoneme and not phoneme.endswith('a'):  # Don't double 'a' endings
                # Add long version
                if phoneme[-1] in 'aeiou':
                    length_variants.append(phoneme + phoneme[-1])
        phonemes.update(length_variants)
        
        # Remove empty strings and None values
        phonemes = {p for p in phonemes if p and p.strip()}
        
        return sorted(phonemes)

    def analyze_text(self, text):
        """Analyze Sinhala text and return phonetic representation"""
        # This could be expanded for actual text-to-phoneme conversion
        # For now, just return the comprehensive phoneme set
        return self.get_all_phonemes()

# Initialize the phoneme system
phoneme_system = SinhalaPhonemeSystem()

# 4) Setup credentials and prepare output dir
if not setup_google_credentials():
    print("Exiting due to missing credentials...")
    exit(1)

output_dir = "phonemes"
os.makedirs(output_dir, exist_ok=True)

# 5) Init TTS client
try:
    client = texttospeech.TextToSpeechClient()
    print("Google Cloud TTS client initialized successfully!")
except Exception as e:
    print(f"Error initializing TTS client: {e}")
    print("Please check your Google Cloud credentials and billing setup.")
    exit(1)

# Check available voices
print("Checking available voices...")
voices = client.list_voices()
print(f"Available voices: {len(voices.voices)}")

# Look for Sinhala voices or English voices as fallback
sinhala_voices = [v for v in voices.voices if 'si' in v.language_codes]
english_voices = [v for v in voices.voices if 'en' in v.language_codes]

print(f"Sinhala voices found: {len(sinhala_voices)}")
for v in sinhala_voices[:3]:  # Show first 3
    print(f"  - {v.name}, Language: {v.language_codes}, Gender: {v.ssml_gender}")

if not sinhala_voices:
    print("No Sinhala voices found. Using English voice as fallback.")
    print(f"English voices available: {len(english_voices)}")
    for v in english_voices[:3]:  # Show first 3
        print(f"  - {v.name}, Language: {v.language_codes}, Gender: {v.ssml_gender}")

# 6) Get comprehensive phoneme set
print("Generating comprehensive phoneme set...")
all_phonemes = phoneme_system.get_all_phonemes()
print(f"Total phonemes to generate: {len(all_phonemes)}")

# 7) Synthesize & write WAVs
print("Starting phoneme synthesis...")
success_count = 0
error_count = 0

for i, phon in enumerate(all_phonemes):
    try:
        # build request
        synthesis_input = texttospeech.SynthesisInput(text=phon)
        
        # Use available voice
        if sinhala_voices:
            # Use first available Sinhala voice
            selected_voice = sinhala_voices[0]
            voice = texttospeech.VoiceSelectionParams(
                name=selected_voice.name,
                language_code=selected_voice.language_codes[0]
            )
        else:
            # Fallback to English voice
            selected_voice = english_voices[0] if english_voices else None
            if selected_voice:
                voice = texttospeech.VoiceSelectionParams(
                    name=selected_voice.name,
                    language_code=selected_voice.language_codes[0]
                )
            else:
                # Last resort - try en-US
                voice = texttospeech.VoiceSelectionParams(
                    language_code="en-US",
                    ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
                )
        
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000
        )

        # call API
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        # write .wav directly
        wav_path = os.path.join(output_dir, f"{phon}.wav")
        with open(wav_path, "wb") as out_f:
            out_f.write(response.audio_content)

        success_count += 1
        if i % 50 == 0:  # Progress update every 50 phonemes
            print(f"Progress: {i+1}/{len(all_phonemes)} - Generated {phon}.wav")

    except Exception as e:
        error_count += 1
        print(f"Error generating {phon}: {e}")
        continue

print(f"\nPhoneme generation complete!")
print(f"Successfully generated: {success_count} phonemes")
print(f"Errors: {error_count} phonemes")
print(f"Total files in {output_dir}: {len(os.listdir(output_dir)) if os.path.exists(output_dir) else 0}")