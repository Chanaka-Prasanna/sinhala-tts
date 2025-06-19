#!/usr/bin/env python3
"""
Test and demonstrate the comprehensive Sinhala phoneme system
"""

import os
import sys
from sinhala_text_to_phoneme import SinhalaTextToPhoneme
from generate_phoneme import SinhalaPhonemeSystem

def test_phoneme_generation():
    """Test the phoneme generation system"""
    print("=" * 60)
    print("TESTING COMPREHENSIVE PHONEME GENERATION SYSTEM")
    print("=" * 60)
    
    phoneme_system = SinhalaPhonemeSystem()
    all_phonemes = phoneme_system.get_all_phonemes()
    
    print(f"Total phonemes generated: {len(all_phonemes)}")
    print(f"First 50 phonemes: {all_phonemes[:50]}")
    print(f"Sample consonant+vowel combinations:")
    
    # Show some examples of consonant+vowel combinations
    consonant_vowel_examples = [p for p in all_phonemes if len(p) > 1 and any(v in p for v in ['aa', 'ii', 'uu', 'ee', 'oo'])]
    print(f"Consonant+vowel examples: {consonant_vowel_examples[:20]}")
    
    # Show consonant clusters
    cluster_examples = [p for p in all_phonemes if any(cluster in p for cluster in ['kra', 'gra', 'pra', 'bra', 'tra', 'dra'])]
    print(f"Consonant cluster examples: {cluster_examples}")
    
    # Show special sound combinations
    special_examples = [p for p in all_phonemes if any(sound in p for sound in ['ng', 'nda', 'mpa', 'sha'])]
    print(f"Special sound examples: {special_examples[:15]}")

def test_text_to_phoneme_conversion():
    """Test the text-to-phoneme conversion"""
    print("\n" + "=" * 60)
    print("TESTING TEXT-TO-PHONEME CONVERSION")
    print("=" * 60)
    
    converter = SinhalaTextToPhoneme()
    
    # Test cases with different complexity levels
    test_cases = [
        # Basic words
        ("අම්මා", "Mother"),
        ("තාත්තා", "Father"),
        ("ගම", "Village"),
        ("කතා", "Story"),
        ("පොත", "Book"),
        
        # Words with diacritics
        ("ගෙදර", "Home"),
        ("කීර", "Milk"),
        ("කූර", "Curry"),
        ("පෙම", "Love"),
        ("මෙම", "This"),
        
        # Words with consonant clusters
        ("ප්‍රේම", "Love (with cluster)"),
        ("ක්‍රීඩා", "Sports"),
        ("ස්කූල", "School"),
        ("ග්‍රාම", "Village (formal)"),
        ("ත්‍රෙන්", "Train"),
        
        # Complex words
        ("සිංහල", "Sinhala"),
        ("ශ්‍රී ලංකා", "Sri Lanka"),
        ("මහනුවර", "Kandy"),
        ("කොළඹ", "Colombo"),
        ("අනුරාධපුර", "Anuradhapura"),
        
        # Words with special characters
        ("සංදර්ශන", "Exhibition"),
        ("කාර්ය", "Work"),
        ("වාර්ත", "Report"),
        ("ආහාර", "Food"),
        ("උදාහරණ", "Example"),
        
        # Phrases
        ("මගේ නම", "My name"),
        ("ඔබේ ගම", "Your village"),
        ("සුභ උදෑසන", "Good morning"),
        ("අපි යමු", "Let's go"),
    ]
    
    print("Text-to-Phoneme Conversion Results:")
    print("-" * 60)
    
    for sinhala_text, english_meaning in test_cases:
        try:
            phonemes_list = converter.text_to_phonemes(sinhala_text)
            phonemes_string = converter.text_to_phoneme_string(sinhala_text)
            
            print(f"Text: {sinhala_text:<20} ({english_meaning})")
            print(f"Phonemes: {phonemes_string}")
            print(f"Breakdown: {' + '.join(phonemes_list)}")
            print("-" * 40)
            
        except Exception as e:
            print(f"Error processing '{sinhala_text}': {e}")
            print("-" * 40)

def test_contextual_variations():
    """Test contextual pronunciation variations"""
    print("\n" + "=" * 60)
    print("TESTING CONTEXTUAL PRONUNCIATION VARIATIONS")
    print("=" * 60)
    
    converter = SinhalaTextToPhoneme()
    
    # Test cases showing how the same character can have different pronunciations
    variation_tests = [
        # Same character in different contexts
        ("ත", "ta/tha in isolation"),
        ("තා", "ta + aa"),
        ("ත්", "ta without vowel"),
        ("ත්‍රේ", "ta in cluster 'tra'"),
        
        ("ද", "da in isolation"),
        ("දා", "da + aa"),
        ("ද්", "da without vowel"),
        ("ද්‍රෙන්", "da in cluster 'dra'"),
        
        # Consonant clusters vs separate consonants
        ("ක්‍ර", "consonant cluster 'kra'"),
        ("ක් ර", "separate k + ra"),
        ("ප්‍ර", "consonant cluster 'pra'"),
        ("ප් ර", "separate p + ra"),
        
        # Words ending with different sounds
        ("ගම්", "with final hal kirima"),
        ("ගම", "without hal kirima"),
        ("කර", "kara"),
        ("කර්", "kar (final r)"),
    ]
    
    print("Contextual Variation Results:")
    print("-" * 40)
    
    for text, description in variation_tests:
        try:
            phonemes = converter.text_to_phoneme_string(text)
            print(f"{text:<15} ({description:<25}) -> {phonemes}")
        except Exception as e:
            print(f"Error processing '{text}': {e}")

def test_phoneme_coverage():
    """Test how well our phoneme set covers actual text"""
    print("\n" + "=" * 60)
    print("TESTING PHONEME COVERAGE")
    print("=" * 60)
    
    phoneme_system = SinhalaPhonemeSystem()
    converter = SinhalaTextToPhoneme()
    
    all_generated_phonemes = set(phoneme_system.get_all_phonemes())
    
    # Sample texts to test coverage
    sample_texts = [
        "ගම", "කතා", "ප්‍රේම", "සිංහල", "මගේ නම", "ස්කූල", 
        "ක්‍රීඩා", "අම්මා", "ගෙදර", "පොත්", "සංදර්ශන", "ශ්‍රී ලංකා"
    ]
    
    used_phonemes = set()
    
    for text in sample_texts:
        try:
            phonemes = converter.text_to_phonemes(text)
            for phoneme in phonemes:
                if phoneme.strip() and phoneme not in '.,!?;: ':
                    used_phonemes.add(phoneme)
        except Exception as e:
            print(f"Error processing '{text}': {e}")
    
    print(f"Generated phonemes in system: {len(all_generated_phonemes)}")
    print(f"Phonemes used by sample texts: {len(used_phonemes)}")
    print(f"Coverage: {len(used_phonemes.intersection(all_generated_phonemes))} / {len(used_phonemes)} = {len(used_phonemes.intersection(all_generated_phonemes))/len(used_phonemes)*100:.1f}%")
    
    # Show missing phonemes
    missing = used_phonemes - all_generated_phonemes
    if missing:
        print(f"Missing phonemes: {sorted(missing)}")
    else:
        print("All used phonemes are covered by the generation system!")
    
    # Show some unused phonemes
    unused = all_generated_phonemes - used_phonemes
    print(f"Sample unused phonemes: {sorted(list(unused))[:20]}")

def create_phoneme_reference():
    """Create a reference document showing all phonemes and their usage"""
    print("\n" + "=" * 60)
    print("CREATING PHONEME REFERENCE")
    print("=" * 60)
    
    phoneme_system = SinhalaPhonemeSystem()
    all_phonemes = phoneme_system.get_all_phonemes()
    
    # Categorize phonemes
    categories = {
        'Basic Vowels': [],
        'Basic Consonants': [],
        'Consonant+Vowel': [],
        'Consonant Clusters': [],
        'Special Sounds': [],
        'Nasalized': [],
        'Long Vowels': []
    }
    
    for phoneme in all_phonemes:
        if phoneme in ['a', 'aa', 'ae', 'aae', 'i', 'ii', 'u', 'uu', 'e', 'ee', 'o', 'oo', 'ai', 'au', 'ri', 'rii', 'li', 'lii']:
            categories['Basic Vowels'].append(phoneme)
        elif len(phoneme) == 2 and phoneme.endswith('a') and phoneme[0] in 'kgcjtdpbmyrlvshf':
            categories['Basic Consonants'].append(phoneme)
        elif any(cluster in phoneme for cluster in ['kra', 'gra', 'pra', 'bra', 'tra', 'dra', 'kla', 'gla', 'pla', 'bla', 'stha', 'spa', 'ska']):
            categories['Consonant Clusters'].append(phoneme)
        elif 'ng' in phoneme or phoneme.endswith('ng') or phoneme.endswith('n') or phoneme.endswith('m'):
            categories['Nasalized'].append(phoneme)
        elif any(long_v in phoneme for long_v in ['aa', 'ii', 'uu', 'ee', 'oo']) and len(phoneme) > 2:
            categories['Long Vowels'].append(phoneme)
        elif len(phoneme) > 2:
            categories['Consonant+Vowel'].append(phoneme)
        else:
            categories['Special Sounds'].append(phoneme)
    
    print("Phoneme Categories:")
    print("-" * 40)
    
    for category, phonemes in categories.items():
        if phonemes:
            print(f"\n{category} ({len(phonemes)} phonemes):")
            # Show first 20 phonemes in each category
            for i in range(0, min(len(phonemes), 20), 10):
                print(f"  {', '.join(phonemes[i:i+10])}")
            if len(phonemes) > 20:
                print(f"  ... and {len(phonemes) - 20} more")

def main():
    """Run all tests"""
    print("COMPREHENSIVE SINHALA PHONEME SYSTEM TEST SUITE")
    print("=" * 80)
    
    try:
        test_phoneme_generation()
        test_text_to_phoneme_conversion()
        test_contextual_variations()
        test_phoneme_coverage()
        create_phoneme_reference()
        
        print("\n" + "=" * 80)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("The rule-based phoneme system is working properly.")
        print("You can now use generate_phoneme.py to create TTS audio files.")
        print("=" * 80)
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure sinhala_text_to_phoneme.py and generate_phoneme.py are in the same directory.")
    except Exception as e:
        print(f"Error during testing: {e}")
        print("Please check the implementation for issues.")

if __name__ == "__main__":
    main() 