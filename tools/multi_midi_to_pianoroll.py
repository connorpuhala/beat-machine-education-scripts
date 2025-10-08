#!/usr/bin/env python3
"""
Multi-MIDI to Sheet Generator for Beatmaking: Learn By Doing

This tool takes multiple MIDI files (one per layer) and creates a unified
piano roll sheet with all layers perfectly aligned.
"""

import mido
import os
import glob
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict
from pathlib import Path

# Get the project root directory (parent of tools/)
PROJECT_ROOT = Path(__file__).parent.parent

@dataclass
class Note:
    """Represents a MIDI note"""
    pitch: int
    start_time: float
    duration: float
    velocity: int

@dataclass
class Track:
    """Represents a track/layer in the song"""
    name: str
    notes: List[Note]
    color: str

class MultiMIDIAnalyzer:
    """Analyzes multiple MIDI files and combines them"""
    
    def __init__(self, midi_directory: str):
        self.midi_directory = midi_directory
        self.tracks = []
        self.max_length_beats = 0  # Track the longest MIDI file
        
    def analyze(self) -> List[Track]:
        """Analyze all MIDI files in directory"""
        midi_files = sorted(glob.glob(os.path.join(self.midi_directory, "*.mid")))
        
        if not midi_files:
            print(f"⚠️  No MIDI files found in {self.midi_directory}")
            return []
        
        print(f"\n🎵 Found {len(midi_files)} MIDI files:")
        
        for midi_file in midi_files:
            filename = os.path.basename(midi_file)
            layer_name = os.path.splitext(filename)[0].title()
            print(f"   • {filename}")
            
            notes = self._extract_notes_from_file(midi_file)
            color = self._get_color_for_layer(layer_name.lower())
            
            if notes:
                # Track maximum length
                max_end_time = max((note.start_time + note.duration) for note in notes)
                self.max_length_beats = max(self.max_length_beats, max_end_time)
                
                track = Track(
                    name=layer_name,
                    notes=notes,
                    color=color
                )
                self.tracks.append(track)
                print(f"      → {len(notes)} notes, length: {max_end_time:.1f} beats")
        
        return self.tracks
    
    def _extract_notes_from_file(self, midi_file_path: str) -> List[Note]:
        """Extract all notes from a MIDI file"""
        midi_file = mido.MidiFile(midi_file_path)
        notes = []
        
        for track in midi_file.tracks:
            current_time = 0
            active_notes = {}  # pitch -> (start_time, velocity)
            
            for msg in track:
                current_time += msg.time
                
                if msg.type == 'note_on' and msg.velocity > 0:
                    active_notes[msg.note] = (current_time, msg.velocity)
                
                elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                    if msg.note in active_notes:
                        start_time, velocity = active_notes[msg.note]
                        duration = current_time - start_time
                        
                        # Convert ticks to beats
                        ticks_per_beat = midi_file.ticks_per_beat
                        start_beats = start_time / ticks_per_beat
                        duration_beats = duration / ticks_per_beat
                        
                        notes.append(Note(
                            pitch=msg.note,
                            start_time=start_beats,
                            duration=duration_beats,
                            velocity=velocity
                        ))
                        del active_notes[msg.note]
        
        return notes
    
    def _get_color_for_layer(self, layer_name: str) -> str:
        """Get color based on layer name"""
        colors = {
            'drums': 'red',
            'kick': 'red',
            'snare': 'red',
            'bass': 'blue',
            'keys': 'green',
            'piano': 'green',
            'chords': 'green',
            'melody': 'purple',
            'lead': 'purple',
            'guitar': 'orange',
            'perc': 'orange',
            'percussion': 'orange'
        }
        
        for key, color in colors.items():
            if key in layer_name:
                return color
        
        return 'gray'


class UnifiedPianoRollGenerator:
    """Generates unified piano roll with all layers"""
    
    def __init__(self, tracks: List[Track], total_beats: float, song_name: str = "Song"):
        self.tracks = tracks
        self.beats_per_bar = 4
        # Round up to nearest bar
        self.bars = int((total_beats + self.beats_per_bar - 1) // self.beats_per_bar)
        self.total_beats = self.bars * self.beats_per_bar
        self.song_name = song_name
        
    def generate_latex(self, output_file: str = "piano_roll.tex"):
        """Generate LaTeX document"""
        latex_content = self._get_latex_header()
        
        # Add each track as a separate layer
        for i, track in enumerate(self.tracks):
            is_last = (i == len(self.tracks) - 1)
            latex_content += self._generate_track_page(track, i + 1, is_last_layer=is_last)
        
        latex_content += self._get_latex_footer()
        
        with open(output_file, 'w') as f:
            f.write(latex_content)
        
        print(f"\n✓ Generated LaTeX: {output_file}")
        return output_file
    
    def _get_latex_header(self) -> str:
        """LaTeX document header"""
        return r'''\documentclass[11pt]{article}
\usepackage[top=0.4in, bottom=0.65in, left=0.75in, right=0.75in]{geometry}
\usepackage{fontspec}
\usepackage{xcolor}
\usepackage{tikz}
\usetikzlibrary{patterns}
\usepackage{setspace}

% Font setup
\setmainfont{ElMessiri-Regular}[
    Path = ../../../assets/fonts/,
    Extension = .ttf,
    BoldFont = ElMessiri-Regular,
    BoldFeatures = {FakeBold=1.5},
]

% Define colors
\definecolor{purple}{RGB}{138,43,226}
\definecolor{blue}{RGB}{30,144,255}
\definecolor{green}{RGB}{34,139,34}
\definecolor{red}{RGB}{220,20,60}
\definecolor{orange}{RGB}{255,140,0}
\definecolor{lightgray}{RGB}{245,245,245}

\begin{document}
\pagestyle{empty}

''' + f'''\\begin{{center}}
{{\\Huge\\bfseries {self.song_name}}}
\\end{{center}}

\\vspace{{0.05cm}}

'''
    
    def _generate_track_page(self, track: Track, layer_num: int, is_last_layer: bool = False) -> str:
        """Generate visualization for one track"""
        # Calculate pitch range
        if track.notes:
            pitches = [n.pitch for n in track.notes]
            is_drum = 'drum' in track.name.lower()
            
            if is_drum:
                # For drums, show only the exact range being used (no padding)
                min_pitch = min(pitches)
                max_pitch = max(pitches)
            else:
                # For melodic instruments, add some padding
                min_pitch = max(min(pitches) - 3, 21)  # Don't go below A0
                max_pitch = min(max(pitches) + 3, 108)  # Don't go above C8
        else:
            min_pitch, max_pitch = 60, 72
        
        # Don't center - use fixed positioning for perfect alignment
        latex = "\\noindent\\hspace{2.5cm}"  # Fixed left margin for all tracks
        # Calculate scale to fit page width (portrait)
        # Slightly narrower for better readability
        target_width = 13  # cm, leaving room for note labels
        x_scale = target_width / self.total_beats
        # Much taller vertical scale to fill the page
        latex += f"\\begin{{tikzpicture}}[xscale={x_scale:.2f}, yscale=1.1]\n"
        
        # Draw grid
        latex += self._draw_grid(min_pitch, max_pitch, track.name, show_bar_labels=is_last_layer)
        
        # Draw notes
        for note in track.notes:
            if note.start_time < self.total_beats:
                latex += self._draw_note(note, min_pitch, track.color)
        
        # Add vertical label on the right side
        pitch_range = max_pitch - min_pitch
        y_center = ((pitch_range + 1) * 0.4) / 2  # Center vertically
        label_x = self.total_beats + 0.5  # Position to the right of the grid
        latex += f"\\node[rotate=90, font=\\Large\\bfseries, overlay] at ({label_x},{y_center}) {{{track.name.upper()}}};\n"
        
        latex += "\\end{tikzpicture}\n\n"
        latex += "\\vspace{0.05cm}\n\n"
        
        return latex
    
    def _draw_grid(self, min_pitch: int, max_pitch: int, track_name: str, show_bar_labels: bool = False) -> str:
        """Draw the piano roll grid"""
        latex = ""
        pitch_range = max_pitch - min_pitch
        y_max = (pitch_range + 1) * 0.4
        
        # Black keys (sharps/flats) - these need shading
        black_keys = {1, 3, 6, 8, 10}  # C#, D#, F#, G#, A# (mod 12)
        
        # Draw shaded rectangles for black keys FIRST (so they're behind everything)
        for i in range(pitch_range + 1):
            pitch = min_pitch + i
            if (pitch % 12) in black_keys:
                y = i * 0.4
                latex += f"\\fill[black!8] (0,{y}) rectangle ({self.total_beats},{y + 0.4});\n"
        
        # Draw border frame (top, bottom, right) - left is already drawn as Bar 1 line
        latex += f"\\draw[black, very thick] (0,0) -- ({self.total_beats},0);\n"  # Bottom
        latex += f"\\draw[black, very thick] (0,{y_max}) -- ({self.total_beats},{y_max});\n"  # Top
        latex += f"\\draw[black, very thick] ({self.total_beats},0) -- ({self.total_beats},{y_max});\n"  # Right
        
        # Horizontal lines (pitches) - show every semitone
        for i in range(pitch_range + 1):
            pitch = min_pitch + i
            y = i * 0.4
            
            # Make C notes thicker
            if pitch % 12 == 0:
                latex += f"\\draw[gray!50, thick] (0,{y}) -- ({self.total_beats},{y});\n"
            else:
                latex += f"\\draw[gray!20] (0,{y}) -- ({self.total_beats},{y});\n"
        
        # Vertical lines (beats and subdivisions)
        # Add 32nd note subdivisions (8 per beat for ultra-fine grid)
        for subdivision in range(int(self.total_beats * 8) + 1):
            beat = subdivision / 8.0
            y_max = (pitch_range + 1) * 0.4  # Go all the way to top of grid
            
            if subdivision % 32 == 0:  # Bar lines (every 4 beats = 32 subdivisions)
                bar_num = (subdivision // 32) + 1
                # Only show bar labels within the actual music range
                if beat < self.total_beats:
                    latex += f"\\draw[black, very thick] ({beat},0) -- ({beat},{y_max});\n"
                    # Only show bar labels if show_bar_labels is True
                    if show_bar_labels:
                        latex += f"\\node[below, font=\\large\\bfseries, overlay] at ({beat},-0.5) {{Bar {bar_num}}};\n"
            elif subdivision % 8 == 0:  # Beat lines (quarter notes)
                latex += f"\\draw[gray!70] ({beat},0) -- ({beat},{y_max});\n"
                # Only show beat numbers if show_bar_labels is True
                if show_bar_labels:
                    beat_num = (subdivision % 32) // 8 + 1
                    latex += f"\\node[below, font=\\small, gray, overlay] at ({beat},-0.5) {{{beat_num}}};\n"
            elif subdivision % 4 == 0:  # 8th note lines
                latex += f"\\draw[gray!50] ({beat},0) -- ({beat},{y_max});\n"
            elif subdivision % 2 == 0:  # 16th note lines
                latex += f"\\draw[gray!35] ({beat},0) -- ({beat},{y_max});\n"
            else:  # 32nd note lines (finest subdivision)
                latex += f"\\draw[gray!20] ({beat},0) -- ({beat},{y_max});\n"
        
        # Note labels on the left - show ALL chromatic notes
        # Place labels at the CENTER of each note space (y + 0.2)
        # Use OVERLAY so labels don't affect bounding box - ensures all grids align perfectly
        is_drum_track = 'drum' in track_name.lower()
        label_x = -0.3  # Fixed position where labels END (right edge of labels)
        
        for i in range(pitch_range + 1):
            pitch = min_pitch + i
            note_name = self._pitch_to_note_name(pitch)
            y_center = i * 0.4 + 0.2  # Center of the note space
            
            # For drums, show ONLY instrument names (no note names)
            if is_drum_track:
                drum_name = self._get_drum_name(pitch)
                if drum_name:
                    # Only show drum instrument name, not pitch
                    latex += f"\\node[anchor=east, font=\\small, overlay] at ({label_x},{y_center}) {{{drum_name}}};\n"
                else:
                    # Skip notes that don't have drum mappings
                    pass
            else:
                # Make C notes bold for non-drum tracks
                if pitch % 12 == 0:
                    latex += f"\\node[anchor=east, font=\\small\\bfseries, overlay] at ({label_x},{y_center}) {{{note_name}}};\n"
                else:
                    latex += f"\\node[anchor=east, font=\\small, overlay] at ({label_x},{y_center}) {{{note_name}}};\n"
        
        return latex
    
    def _draw_note(self, note: Note, min_pitch: int, color: str) -> str:
        """Draw a single note rectangle with visual attack indicator"""
        x = note.start_time
        pitch_offset = note.pitch - min_pitch
        y_base = pitch_offset * 0.4 + 0.025  # Small offset to center in space
        width = max(note.duration, 0.15)  # Minimum width for visibility
        
        # Attack is full height, sustain is thinner
        full_height = 0.35
        sustain_height = 0.25  # Thinner tail
        attack_width = min(0.08, width * 0.3)  # Attack marker width
        
        # Opacity based on velocity
        opacity = 0.6 + (note.velocity / 127) * 0.4
        
        # Draw the thinner sustain (tail) first
        y_sustain = y_base + (full_height - sustain_height) / 2  # Center the thinner sustain
        latex = f"\\fill[{color}, opacity={opacity:.2f}, rounded corners=1pt] ({x},{y_sustain}) rectangle ({x + width},{y_sustain + sustain_height});\n"
        
        # Draw the full-height, darker attack on top
        latex += f"\\fill[{color}, opacity={min(1.0, opacity + 0.35)}, rounded corners=1pt] ({x},{y_base}) rectangle ({x + attack_width},{y_base + full_height});\n"
        
        return latex
    
    def _pitch_to_note_name(self, pitch: int) -> str:
        """Convert MIDI pitch to note name"""
        notes = ['C', 'C\\#', 'D', 'D\\#', 'E', 'F', 'F\\#', 'G', 'G\\#', 'A', 'A\\#', 'B']
        octave = (pitch // 12) - 1
        note = notes[pitch % 12]
        return f"{note}{octave}"
    
    def _get_drum_name(self, pitch: int) -> str:
        """Get drum instrument name from MIDI pitch (General MIDI standard)"""
        drum_map = {
            35: 'Kick',
            36: 'Kick',
            38: 'Snare',
            40: 'Snare',
            37: 'Side Stick',
            39: 'Clap',
            42: 'Hi-Hat Closed',
            44: 'Hi-Hat Pedal',
            46: 'Hi-Hat Open',
            41: 'Tom Low',
            43: 'Tom Low-Mid',
            45: 'Tom Mid',
            47: 'Tom Mid-High',
            48: 'Tom High',
            49: 'Crash',
            51: 'Ride',
            52: 'Crash China',
            53: 'Ride Bell',
            54: 'Tambourine',
            55: 'Splash',
            56: 'Cowbell',
            57: 'Crash',
            59: 'Ride',
        }
        return drum_map.get(pitch, '')
    
    def _get_latex_footer(self) -> str:
        """LaTeX document footer"""
        return r'''

\end{document}
'''


def main():
    """Main function"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 multi_midi_to_pianoroll.py <midi_directory> [song_name]")
        print("\nExample: python3 multi_midi_to_pianoroll.py content/midi/come_together \"Come Together\"")
        print("         python3 multi_midi_to_pianoroll.py come_together \"Come Together\" (searches in content/midi/)")
        sys.exit(1)
    
    midi_input = sys.argv[1]
    song_name = sys.argv[2] if len(sys.argv) > 2 else os.path.basename(midi_input).replace('_', ' ').title()
    
    # If path doesn't exist, try looking in content/midi/
    if not os.path.isdir(midi_input):
        midi_dir = PROJECT_ROOT / "content" / "midi" / midi_input
        if not midi_dir.exists():
            print(f"Error: Directory '{midi_input}' not found")
            print(f"Also tried: {midi_dir}")
            sys.exit(1)
    else:
        midi_dir = Path(midi_input)
    
    # Analyze MIDI files
    analyzer = MultiMIDIAnalyzer(str(midi_dir))
    tracks = analyzer.analyze()
    
    if not tracks:
        print("\n⚠️  No tracks found")
        sys.exit(1)
    
    # Get the maximum length from all tracks
    total_beats = analyzer.max_length_beats
    bars = int((total_beats + 3) // 4)  # Round up to nearest bar
    
    print(f"\n📏 Total length: {total_beats:.1f} beats ({bars} bars)")
    
    # Generate piano roll
    print(f"🎨 Generating unified piano roll for {len(tracks)} layers...")
    generator = UnifiedPianoRollGenerator(tracks, total_beats=total_beats, song_name=song_name)
    
    # Output to generated and build directories
    dir_name = midi_dir.name
    tex_output = PROJECT_ROOT / "packets" / "pianorolls" / "_generated" / f"{dir_name}_pianoroll.tex"
    
    # Ensure output directory exists
    tex_output.parent.mkdir(parents=True, exist_ok=True)
    
    generator.generate_latex(str(tex_output))
    
    print(f"\n✅ Done! LaTeX saved to: {tex_output.relative_to(PROJECT_ROOT)}")
    print(f"Compile with: cd packets/pianorolls/_generated && xelatex {tex_output.name}")


if __name__ == "__main__":
    main()

