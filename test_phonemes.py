import pygame
import os
import time

def test_phonemes():
    """Test if phoneme files can be loaded and played"""
    
    # Initialize pygame mixer
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    
    phonemes_dir = "phonemes"
    
    if not os.path.exists(phonemes_dir):
        print(f"Error: {phonemes_dir} directory not found!")
        return False
    
    # Test a few key phonemes
    test_sounds = ["a.wav", "ka.wav", "ma.wav", "na.wav"]
    
    print("Testing phoneme playback...")
    
    for sound_file in test_sounds:
        sound_path = os.path.join(phonemes_dir, sound_file)
        
        if os.path.exists(sound_path):
            try:
                print(f"Playing: {sound_file}")
                sound = pygame.mixer.Sound(sound_path)
                channel = sound.play()
                
                # Wait for sound to finish
                while channel.get_busy():
                    time.sleep(0.01)
                    
                time.sleep(0.2)  # Small pause between sounds
                print(f"✓ {sound_file} played successfully")
                
            except pygame.error as e:
                print(f"✗ Error playing {sound_file}: {e}")
                return False
        else:
            print(f"✗ Sound file not found: {sound_path}")
            return False
    
    print("\nAll phoneme tests passed! ✓")
    return True

if __name__ == "__main__":
    test_phonemes() 