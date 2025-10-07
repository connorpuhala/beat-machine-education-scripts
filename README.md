# Beatmaking: Learn By Doing - Packet Generator

This folder contains tools to generate education packets for the program.

## Main Education Packet

To compile the main program overview PDF:
```bash
xelatex education_packet.tex
```

## Song-Specific Packets

### Quick Start
1. Add song data to `songs_data.json`
2. Run the generator: `python3 generate_song_pdfs.py`
3. Compile PDFs: `cd song_packets && xelatex the_beatles_come_together.tex`

### File Structure

- **`songs_data.json`** - Database of all songs with metadata
- **`generate_song_pdfs.py`** - Python script to generate LaTeX files from JSON
- **`song_template.tex`** - Manual template (for reference)
- **`song_packets/`** - Output directory for generated packets

### Song Data Format

Each song in `songs_data.json` includes:
- Title, artist, BPM, key, year, album, genre
- Artist bio
- Song context and cultural impact
- Key musical elements
- Learning points
- Comparable songs

### Generating Song Packets

**Generate all songs:**
```bash
python3 generate_song_pdfs.py
```

**Compile a specific song to PDF:**
```bash
cd song_packets
xelatex the_beatles_come_together.tex
```

### Adding New Songs

1. Add entry to `songs_data.json` following the existing format
2. Run `python3 generate_song_pdfs.py`
3. LaTeX files will be generated in `song_packets/`

## MIDI to Piano Roll Sheets

### Quick Start

1. **Install Python dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Convert MIDI to piano roll:**
   ```bash
   python3 midi_to_sheet.py your_song.mid 8
   ```
   (The `8` means show 8 bars)

3. **Compile to PDF:**
   ```bash
   xelatex your_song_pianoroll.tex
   ```

### Features

The MIDI tool automatically:
- **Analyzes tracks** and classifies them (drums, bass, chords, melody)
- **Creates visual piano roll** representations with color coding
- **Aligns all layers** on a single page for easy reading
- **Labels notes** with pitch names
- **Shows bar divisions** clearly
- **Adjusts velocity** with opacity (louder = more opaque)

### Track Classification

- 🔴 **Drums** - Channel 10, percussion sounds
- 🔵 **Bass** - Low pitch range (E1-E3)
- 🟢 **Chords** - 3+ simultaneous notes
- 🟣 **Melody** - Higher range, single notes
- 🟠 **Harmony** - Supporting melodic elements

### Requirements

- Python 3
- `mido` library (MIDI parsing)
- XeLaTeX (from MacTeX)
- ElMessiri font (included: `ElMessiri-Regular.ttf`)

## Current Song List

1. Come Together - The Beatles ✓

*More songs to be added...*

# beat-machine-education-scripts
