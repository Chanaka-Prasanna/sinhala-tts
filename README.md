# Sinhala Text-to-Speech Application

A comprehensive Sinhala Text-to-Speech (TTS) system with linguistic analysis capabilities.

## Features

- **Text-to-Speech**: Convert Sinhala text to natural-sounding speech
- **Linguistic Analysis**: Detailed phoneme breakdown and tokenization
- **Phoneme Explorer**: Browse and test individual phonemes
- **Audio Export**: Save generated speech as WAV files
- **Multiple Tabs**: Organized interface for different functionalities

## System Requirements

- Windows 10 or later (64-bit)
- Audio output device (speakers/headphones)
- Minimum 4GB RAM
- 100MB free disk space

## Installation

1. Run the installer `SinhalaTTS_Setup_v1.0.exe`
2. Follow the installation wizard
3. The application will be installed to `Program Files\Sinhala Text-to-Speech`
4. A desktop shortcut will be created (optional)

## Usage

### Text-to-Speech

1. Open the application
2. Enter Sinhala text in the input field
3. Click "🔊 Speak" to generate and play audio
4. Use "💾 Save Audio" to export as WAV file

### Linguistic Analysis

1. Switch to the "🔍 Linguistic Analysis" tab
2. Enter text for analysis
3. Click "🔍 Analyze Text"
4. View results in the Phonemes, Tokenization, and Statistics tabs

### Phoneme Explorer

1. Go to "🎵 Phoneme Explorer" tab
2. Browse available phoneme audio files
3. Double-click any phoneme to play it
4. Generate phoneme reports

### Settings

1. Open the "⚙ Settings" tab
2. Adjust audio settings (sample rate, pause durations)
3. Configure analysis options
4. Change phonemes directory if needed

## Troubleshooting

**No sound output:**

- Check your audio device settings
- Ensure the phonemes directory contains audio files
- Try adjusting the sample rate in Settings

**Application won't start:**

- Run as Administrator
- Check Windows compatibility mode
- Ensure all dependencies are installed

**Missing phonemes:**

- The application requires phoneme audio files in the `phonemes` folder
- Check the Phoneme Explorer for missing files

## Technical Details

- Built with Python and Tkinter
- Uses pygame for audio playback
- Supports WAV audio format (16kHz recommended)
- Phoneme-based speech synthesis

## Support

For technical support or bug reports, please contact [your-email@domain.com]

## Version History

- v1.0: Initial release with full TTS and analysis features

---

© 2024 Your Name. All rights reserved.
