# Beatmaking: Learn By Doing - Packet Generator

This repository contains tools to generate education packets for the program.

## 📁 Repository Structure

```
beat-machine-education-packets/
│
├── tools/                         # Scripts and generators
│   ├── generate_song_pdfs.py      # Generate song lesson packets
│   ├── midi_to_pianoroll.py       # Single MIDI → piano roll
│   └── multi_midi_to_pianoroll.py # Multi-MIDI → unified piano roll
│
├── templates/                     # LaTeX templates
│   └── song_template.tex          # Template for song packets
│
├── assets/                        # Static assets
│   ├── fonts/                     # Font files
│   │   └── ElMessiri-Regular.ttf
│   └── images/                    # Images and illustrations
│       ├── beat_machine_3d_render.png
│       └── illustrations/         # Program illustrations
│
├── content/                       # Content and data
│   ├── songs.json                 # Song database
│   └── midi/                      # MIDI files by song
│       └── [song_name]/
│           ├── bass.mid
│           ├── drums.mid
│           └── keys.mid
│
├── packets/                       # Generated packets
│   ├── education/                 # Main education packet
│   │   ├── education_packet.tex   # Source file
│   │   └── _build/                # Compiled PDF (gitignored)
│   │
│   ├── songs/                     # Song lesson packets
│   │   ├── _generated/            # Generated .tex (gitignored)
│   │   └── _build/                # Compiled PDFs (gitignored)
│   │
│   └── pianorolls/                # Piano roll sheets
│       ├── _generated/            # Generated .tex (gitignored)
│       └── _build/                # Compiled PDFs (gitignored)
│
└── docs/                          # Documentation
```

---

## 🚀 Quick Start

### Prerequisites

1. **Python 3.7+** with packages:
   ```bash
   pip install -r requirements.txt
   ```

2. **XeLaTeX** (from MacTeX on macOS):
   ```bash
   # Check if installed
   which xelatex
   ```

---

## 📚 Main Education Packet

The comprehensive program overview document.

### Compile the Education Packet

```bash
cd packets/education
xelatex education_packet.tex
```

Output: `packets/education/_build/education_packet.pdf`

---

## 🎵 Song-Specific Lesson Packets

Individual lesson plans for songs students will learn.

### Add a New Song

1. **Add song data** to `content/songs.json`:
   ```json
   {
     "title": "Song Name",
     "artist": "Artist Name",
     "bpm": "120",
     "key": "C major",
     "year": "2020",
     "album": "Album Name",
     "genre": "Pop, Rock",
     "artist_bio": "...",
     "song_context": "...",
     "key_elements": ["...", "..."],
     "learning_points": ["...", "..."],
     "comparables": [
       {
         "song": "Similar Song",
         "artist": "Artist",
         "reason": "Why it's similar"
       }
     ]
   }
   ```

2. **Generate all song packets**:
   ```bash
   python3 tools/generate_song_pdfs.py
   ```

3. **Output**:
   - LaTeX: `packets/songs/_generated/`
   - PDFs: `packets/songs/_build/`

### Generate a Specific Song

The script automatically generates all songs in `content/songs.json`. To generate just one, you can temporarily edit the JSON file or modify the script.

---

## 🎹 MIDI to Piano Roll Conversion

Create visual piano roll sheets from MIDI files for use in lessons.

### Option 1: Multi-MIDI (Recommended)

Use when you have separate MIDI files for each instrument layer.

```bash
# Place MIDI files in content/midi/[song_name]/
# Example: content/midi/come_together/bass.mid, drums.mid, keys.mid

# Generate piano roll
python3 tools/multi_midi_to_pianoroll.py come_together "Come Together"
```

**Output**: `packets/pianorolls/_generated/come_together_pianoroll.tex`

**Compile to PDF**:
```bash
cd packets/pianorolls/_generated
xelatex come_together_pianoroll.tex
```

### Option 2: Single MIDI File

Use when you have one MIDI file with multiple tracks.

```bash
python3 tools/midi_to_pianoroll.py path/to/song.mid 8
# The "8" means show 8 bars
```

---

## 🎨 Features

### Song Packets Include:
- Song and artist metadata (BPM, key, year, genre)
- Artist biography
- Song context and cultural impact
- Key musical elements
- Learning objectives
- Comparable songs for exploration

### Piano Roll Sheets Include:
- Visual representation of all instrument layers
- Color-coded tracks (drums=red, bass=blue, chords=green, melody=purple)
- Bar/beat divisions with grid
- Note labels with pitch names
- Velocity visualization (opacity)
- Drum instrument labels (Kick, Snare, Hi-Hat, etc.)

---

## 🛠️ Workflow

### Typical workflow for adding a new song:

1. **Prepare MIDI files**
   ```bash
   mkdir -p content/midi/new_song
   # Add bass.mid, drums.mid, keys.mid, etc.
   ```

2. **Add song to database**
   ```bash
   # Edit content/songs.json and add entry
   ```

3. **Generate lesson packet**
   ```bash
   python3 tools/generate_song_pdfs.py
   ```

4. **Generate piano roll**
   ```bash
   python3 tools/multi_midi_to_pianoroll.py new_song "Song Title"
   ```

5. **Compile everything**
   ```bash
   cd packets/songs/_build
   xelatex ../generated/[your_song].tex
   
   cd ../../pianorolls/_generated
   xelatex new_song_pianoroll.tex
   ```

---

## 📝 Current Song List

1. ✅ Come Together - The Beatles
2. ✅ Still D.R.E. - Dr. Dre ft. Snoop Dogg

*More songs to be added...*

---

## 📖 Documentation

- **[WORKFLOW.md](docs/WORKFLOW.md)** - Complete workflow for adding songs
- **[THEORY_ANALYSIS_GUIDE.md](docs/THEORY_ANALYSIS_GUIDE.md)** - How to write music theory analysis sections
- **[MIGRATION_SUMMARY.md](docs/MIGRATION_SUMMARY.md)** - Repository reorganization details

---

## 🎓 Educational Theory

The program is grounded in:
- **John Dewey**: Learning by doing
- **David Kolb**: Experiential learning cycle
- **Constructivism**: Building knowledge through experience
- **Enactivism**: Cognition through physical interaction
- **Music as Language**: Play before notation

See `packets/education/education_packet.pdf` for full details.

---

## 📦 Dependencies

See `requirements.txt`:
- `mido` - MIDI file parsing
- `python-rtmidi` - MIDI I/O (optional)

---

## 🤝 Contributing

### Adding New Songs
1. Follow the format in `content/songs.json`
2. Include high-quality MIDI files (separate by instrument)
3. Run generation scripts
4. Test compile all outputs

### Modifying Templates
- Song template: `templates/song_template.tex`
- Education packet: `packets/education/education_packet.tex`


Making a new song

mkdir -p content/midi/still_dre
add midi content here



---

## 📞 Contact

**Connor Puhala**  
Berklee College of Music Graduate & Professional Music Educator

- Website: [www.makebeatsanywhere.com](https://www.makebeatsanywhere.com)
- Email: connor@makebeatsanywhere.com
- Instagram: [@the_beat_machine_](https://www.instagram.com/the_beat_machine_)

---

## 📄 License

Copyright © 2024 Connor Puhala. All rights reserved.
