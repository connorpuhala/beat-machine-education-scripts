# Workflow Guide

This document explains how to use the packet generation system.

## Quick Reference

### Generate All Song Packets
```bash
python3 tools/generate_song_pdfs.py
```

### Generate Piano Roll from MIDI Directory
```bash
python3 tools/multi_midi_to_pianoroll.py come_together "Come Together"
```

### Compile Education Packet
```bash
cd packets/education
xelatex education_packet.tex
```

---

## Adding a New Song: Complete Workflow

### Step 1: Prepare MIDI Files

Create a directory in `content/midi/` with the song name (use underscores):

```bash
mkdir -p content/midi/still_dre
```

Export or add your MIDI files:
- `bass.mid` - Bass line
- `drums.mid` - Drum track
- `keys.mid` - Keyboard/chords
- `melody.mid` - Melody (optional)
- `perc.mid` - Additional percussion (optional)

**Naming convention**: Use lowercase, descriptive names. The script will auto-detect instrument types based on filename.

### Step 2: Add Song Metadata

Edit `content/songs.json` and add a new entry:

```json
{
  "title": "Still D.R.E.",
  "artist": "Dr. Dre ft. Snoop Dogg",
  "bpm": "93",
  "key": "A minor",
  "year": "1999",
  "album": "2001",
  "genre": "Hip-Hop, West Coast Rap, G-Funk",
  "artist_bio": "Write a compelling biography about the artist...",
  "song_context": "Write about the song's history, cultural impact, and production details...",
  "key_elements": [
    "\\textbf{Iconic Piano Riff:} The instantly recognizable 4-note piano motif",
    "\\textbf{G-Funk Groove:} Classic West Coast hip-hop drum pattern",
    "\\textbf{Minimalist Production:} Space and simplicity create maximum impact"
  ],
  "learning_points": [
    "How to create memorable hooks with minimal notes",
    "Understanding the \\purple{G-Funk} production style",
    "Building tension with \\bluepurple{repetition} and variation"
  ],
  "comparables": [
    {
      "song": "Nuthin' but a 'G' Thang",
      "artist": "Dr. Dre",
      "reason": "Classic G-Funk sound with smooth groove and synth leads"
    },
    {
      "song": "Regulate",
      "artist": "Warren G ft. Nate Dogg",
      "reason": "Similar West Coast production with melodic hooks"
    }
  ]
}
```

**Tips for Writing Content:**
- Use LaTeX commands for colored text: `\purple{...}`, `\bluepurple{...}`, `\greentext{...}`, `\redtext{...}`
- Use `\textbf{...}` for bold text
- Use `\textit{...}` for italic text
- Escape special characters: `\&` for &, `\%` for %

### Step 3: Generate Song Packet

```bash
python3 tools/generate_song_pdfs.py
```

**Output:**
- LaTeX file: `packets/songs/_generated/dr_dre_ft_snoop_dogg_still_dre.tex`
- PDF: `packets/songs/_build/dr_dre_ft_snoop_dogg_still_dre.pdf`

### Step 4: Generate Piano Roll

```bash
python3 tools/multi_midi_to_pianoroll.py still_dre "Still D.R.E."
```

**Output:**
- LaTeX: `packets/pianorolls/_generated/still_dre_pianoroll.tex`

**Compile to PDF:**
```bash
cd packets/pianorolls/_generated
xelatex still_dre_pianoroll.tex
```

PDF saved to same directory.

### Step 5: Review and Iterate

1. **Open the PDFs** and review:
   - Song packet for content accuracy and formatting
   - Piano roll for MIDI accuracy and readability

2. **Make adjustments** if needed:
   - Edit `content/songs.json` for content changes
   - Edit MIDI files if notation needs correction
   - Re-run generation scripts

3. **Move to final location** (optional):
   ```bash
   # PDFs are already in _build directories
   # These can be distributed or committed to git
   ```

---

## Updating Existing Content

### Update Song Metadata
1. Edit `content/songs.json`
2. Run `python3 tools/generate_song_pdfs.py`
3. PDFs are automatically updated

### Update Piano Roll
1. Edit MIDI files in `content/midi/[song_name]/`
2. Re-run: `python3 tools/multi_midi_to_pianoroll.py [song_name] "Song Title"`
3. Recompile with xelatex

### Update Education Packet
1. Edit `packets/education/education_packet.tex`
2. Compile:
   ```bash
   cd packets/education
   xelatex education_packet.tex
   ```
3. PDF saved to `packets/education/_build/`

---

## Directory Organization

### Where Files Live

**Source Files** (version controlled):
- `content/songs.json` - Song database
- `content/midi/` - MIDI files
- `templates/` - LaTeX templates
- `packets/education/education_packet.tex` - Main packet source

**Generated Files** (gitignored):
- `packets/songs/_generated/*.tex` - Generated song packets
- `packets/pianorolls/_generated/*.tex` - Generated piano rolls

**Build Artifacts** (gitignored):
- `packets/songs/_build/*.pdf` - Compiled song packets
- `packets/pianorolls/_build/*.pdf` - Compiled piano rolls (if moved)
- `packets/education/_build/*.pdf` - Compiled education packet
- All `.aux`, `.log`, `.out` files

---

## Tips and Best Practices

### MIDI Files
- **Separate instruments** into different files for best results
- **Quantize** notes to the grid for cleaner piano rolls
- **Use standard MIDI pitches** for drums (General MIDI standard)
- Keep files **short** (8-16 bars) for classroom use

### Content Writing
- **Artist bio**: 3-4 paragraphs about the artist's background and influence
- **Song context**: 2-3 paragraphs about the song's creation and impact
- **Key elements**: 3-5 bullet points describing what makes the beat special
- **Learning points**: 3-5 bullet points about what students will learn
- **Comparables**: 3-5 songs with similar vibes and clear reasons why

### LaTeX Formatting
- Use `\\` for line breaks within items
- Use `---` for em-dashes
- Use `\"` for quotes around song titles
- Test compile after major changes

### Git Workflow
- **Commit**: Source files (songs.json, MIDI, .tex files)
- **Ignore**: Generated files (_generated/, _build/)
- **Optional**: Commit final PDFs if you want to track versions

---

## Troubleshooting

### "File not found" errors
- Check that paths are relative to project root
- Ensure you're running scripts from project root
- Verify MIDI files are in `content/midi/[song_name]/`

### Font errors in LaTeX
- Ensure `ElMessiri-Regular.ttf` is in `assets/fonts/`
- Check that Path in LaTeX files points correctly (relative to .tex file location)

### MIDI not parsing correctly
- Check file encoding (should be standard MIDI format)
- Verify tracks are named appropriately
- Ensure notes have proper note-off messages

### PDF layout issues
- Edit templates in `templates/` directory
- Regenerate all files: `python3 tools/generate_song_pdfs.py`
- For education packet, edit `packets/education/education_packet.tex` directly

---

## Advanced: Customizing Templates

### Modify Song Packet Template

Edit `templates/song_template.tex` for reference, but note that the actual template is embedded in `tools/generate_song_pdfs.py` (the `TEMPLATE` variable).

To make template changes:
1. Edit the `TEMPLATE` string in `tools/generate_song_pdfs.py`
2. Regenerate all packets: `python3 tools/generate_song_pdfs.py`

### Modify Piano Roll Output

Edit the `_get_latex_header()` method in:
- `tools/multi_midi_to_pianoroll.py` for multi-MIDI sheets
- `tools/midi_to_pianoroll.py` for single-MIDI sheets

---

## Need Help?

Contact: connor@makebeatsanywhere.com

