#!/usr/bin/env python3
"""
MIDI to Sheet Generator for Beatmaking: Learn By Doing

This tool parses MIDI files and creates visual piano roll sheets
with each layer (drums, bass, chords, melody) clearly labeled and aligned.
"""

import mido
import json
import os
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class Note:
    """Represents a MIDI note"""
    pitch: int
    start_time: float
    duration: float
    velocity: int
    channel: int

@dataclass
class Track:
    """Represents a track/layer in the song"""
    name: str
    notes: List[Note]
    instrument: str
    color: str
    track_type: str  # 'drums', 'bass', 'chords', 'melody', 'percussion'

class MIDIAnalyzer:
    """Analyzes MIDI files and extracts layer information"""
    
    # MIDI note ranges for different instruments
    DRUM_CHANNEL = 9  # MIDI channel 10 (0-indexed)
    BASS_RANGE = (28, 52)  # E1 to E3
    CHORD_RANGE = (48, 84)  # C3 to C6
    MELODY_RANGE = (60, 96)  # C4 to C7
    
    def __init__(self, midi_file_path: str):
        self.midi_file = mido.MidiFile(midi_file_path)
        self.tempo = 500000  # Default: 120 BPM
        self.ticks_per_beat = self.midi_file.ticks_per_beat
        self.tracks = []
        
    def analyze(self) -> List[Track]:
        """Main analysis function"""
        print(f"\n🎵 Analyzing MIDI file: {os.path.basename(self.midi_file.filename)}")
        print(f"   Ticks per beat: {self.ticks_per_beat}")
        print(f"   Number of tracks: {len(self.midi_file.tracks)}")
        
        for i, track in enumerate(self.midi_file.tracks):
            print(f"\n   Track {i}: {track.name}")
            notes = self._extract_notes_from_track(track)
            
            if notes:
                track_type = self._classify_track(notes)
                instrument = self._get_instrument_name(track)
                color = self._get_track_color(track_type)
                
                analyzed_track = Track(
                    name=track.name or f"Track {i}",
                    notes=notes,
                    instrument=instrument,
                    color=color,
                    track_type=track_type
                )
                self.tracks.append(analyzed_track)
                print(f"      → Type: {track_type}, Notes: {len(notes)}")
        
        return self.tracks
    
    def _extract_notes_from_track(self, track) -> List[Note]:
        """Extract all notes from a track"""
        notes = []
        current_time = 0
        active_notes = {}  # pitch -> (start_time, velocity, channel)
        
        for msg in track:
            current_time += msg.time
            
            if msg.type == 'set_tempo':
                self.tempo = msg.tempo
            
            elif msg.type == 'note_on' and msg.velocity > 0:
                # Note starts
                active_notes[msg.note] = (current_time, msg.velocity, msg.channel)
            
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                # Note ends
                if msg.note in active_notes:
                    start_time, velocity, channel = active_notes[msg.note]
                    duration = current_time - start_time
                    
                    notes.append(Note(
                        pitch=msg.note,
                        start_time=self._ticks_to_beats(start_time),
                        duration=self._ticks_to_beats(duration),
                        velocity=velocity,
                        channel=channel
                    ))
                    del active_notes[msg.note]
        
        return notes
    
    def _ticks_to_beats(self, ticks: int) -> float:
        """Convert MIDI ticks to beat position"""
        return ticks / self.ticks_per_beat
    
    def _classify_track(self, notes: List[Note]) -> str:
        """Classify track as drums, bass, chords, or melody"""
        if not notes:
            return 'unknown'
        
        # Check if it's drums (channel 10)
        if notes[0].channel == self.DRUM_CHANNEL:
            return 'drums'
        
        # Analyze pitch range and note density
        pitches = [n.pitch for n in notes]
        min_pitch, max_pitch = min(pitches), max(pitches)
        avg_pitch = sum(pitches) / len(pitches)
        
        # Check for simultaneous notes (chords)
        time_buckets = defaultdict(list)
        for note in notes:
            time_bucket = round(note.start_time * 4) / 4  # Quantize to 16th notes
            time_buckets[time_bucket].append(note)
        
        simultaneous_notes = max(len(bucket) for bucket in time_buckets.values())
        
        # Classification logic
        if max_pitch < 52:  # Low range
            return 'bass'
        elif simultaneous_notes >= 3:  # 3+ notes at once
            return 'chords'
        elif avg_pitch >= 65:  # Higher range
            return 'melody'
        else:
            return 'harmony'
    
    def _get_instrument_name(self, track) -> str:
        """Try to determine instrument from track name or program change"""
        # Check track name for clues
        name_lower = track.name.lower()
        if 'drum' in name_lower or 'kick' in name_lower or 'snare' in name_lower:
            return 'Drums'
        elif 'bass' in name_lower:
            return 'Bass'
        elif 'piano' in name_lower or 'keys' in name_lower:
            return 'Piano'
        elif 'guitar' in name_lower:
            return 'Guitar'
        elif 'strings' in name_lower:
            return 'Strings'
        
        # TODO: Parse program_change messages for instrument
        return track.name or 'Unknown'
    
    def _get_track_color(self, track_type: str) -> str:
        """Get LaTeX color for track type"""
        colors = {
            'drums': 'red',
            'bass': 'blue',
            'chords': 'green',
            'melody': 'purple',
            'harmony': 'orange',
            'percussion': 'orange',
            'unknown': 'gray'
        }
        return colors.get(track_type, 'gray')


class PianoRollGenerator:
    """Generates visual piano roll representations"""
    
    def __init__(self, tracks: List[Track], bars: int = 8):
        self.tracks = tracks
        self.bars = bars
        self.beats_per_bar = 4
        self.total_beats = bars * self.beats_per_bar
        
    def generate_latex(self, output_file: str = "piano_roll.tex"):
        """Generate LaTeX document with piano roll visualizations"""
        latex_content = self._get_latex_header()
        
        # Add each track
        for i, track in enumerate(self.tracks):
            latex_content += self._generate_track_visualization(track, i)
            latex_content += "\n\\vspace{1cm}\n\n"
        
        latex_content += self._get_latex_footer()
        
        with open(output_file, 'w') as f:
            f.write(latex_content)
        
        print(f"\n✓ Generated LaTeX: {output_file}")
        return output_file
    
    def _get_latex_header(self) -> str:
        """LaTeX document header"""
        return r'''\documentclass[11pt,landscape]{article}
\usepackage[margin=0.5in]{geometry}
\usepackage{fontspec}
\usepackage{xcolor}
\usepackage{tikz}
\usetikzlibrary{patterns}
\usepackage{setspace}

% Font setup
\setmainfont{ElMessiri-Regular}[
    Path = ./,
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

\begin{document}
\pagestyle{empty}

\begin{center}
{\Huge\bfseries Piano Roll - Layer by Layer}
\end{center}

\vspace{1cm}

'''
    
    def _generate_track_visualization(self, track: Track, index: int) -> str:
        """Generate TikZ visualization for a single track"""
        # Calculate pitch range for this track
        if track.notes:
            pitches = [n.pitch for n in track.notes]
            min_pitch = min(pitches) - 2
            max_pitch = max(pitches) + 2
            pitch_range = max_pitch - min_pitch
        else:
            min_pitch, max_pitch, pitch_range = 60, 72, 12
        
        latex = f"\\subsection*{{Layer {index + 1}: {track.name} ({track.track_type.title()})}}\n\n"
        latex += "\\begin{tikzpicture}[scale=0.8]\n"
        
        # Draw grid
        latex += self._draw_grid(pitch_range, min_pitch)
        
        # Draw notes
        for note in track.notes:
            if note.start_time < self.total_beats:  # Only show notes within our range
                latex += self._draw_note(note, min_pitch, track.color)
        
        latex += "\\end{tikzpicture}\n"
        
        return latex
    
    def _draw_grid(self, pitch_range: int, min_pitch: int) -> str:
        """Draw the piano roll grid"""
        latex = ""
        
        # Horizontal lines (pitches)
        for i in range(pitch_range + 1):
            y = i * 0.5
            latex += f"\\draw[gray!30] (0,{y}) -- ({self.total_beats},{y});\n"
        
        # Vertical lines (beats)
        for beat in range(self.total_beats + 1):
            # Thicker lines for bar divisions
            if beat % self.beats_per_bar == 0:
                latex += f"\\draw[gray!70, thick] ({beat},0) -- ({beat},{pitch_range * 0.5});\n"
                latex += f"\\node[below] at ({beat},-0.3) {{Bar {beat // self.beats_per_bar + 1}}};\n"
            else:
                latex += f"\\draw[gray!30] ({beat},0) -- ({beat},{pitch_range * 0.5});\n"
        
        # Note labels on the left
        for i in range(0, pitch_range + 1, 2):
            pitch = min_pitch + i
            note_name = self._pitch_to_note_name(pitch)
            latex += f"\\node[left] at (-0.2,{i * 0.5}) {{\\small {note_name}}};\n"
        
        return latex
    
    def _draw_note(self, note: Note, min_pitch: int, color: str) -> str:
        """Draw a single note rectangle"""
        x = note.start_time
        y = (note.pitch - min_pitch) * 0.5
        width = max(note.duration, 0.1)  # Minimum width for visibility
        height = 0.4
        
        # Opacity based on velocity
        opacity = 0.5 + (note.velocity / 127) * 0.5
        
        return f"\\fill[{color}, opacity={opacity:.2f}] ({x},{y}) rectangle ({x + width},{y + height});\n"
    
    def _pitch_to_note_name(self, pitch: int) -> str:
        """Convert MIDI pitch to note name"""
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = (pitch // 12) - 1
        note = notes[pitch % 12]
        return f"{note}{octave}"
    
    def _get_latex_footer(self) -> str:
        """LaTeX document footer"""
        return r'''
\vspace{2cm}

\begin{center}
\textbf{Beatmaking: Learn By Doing} \\
\textit{Piano Roll Notation for Modern Music Making}
\end{center}

\end{document}
'''


def main():
    """Main function"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 midi_to_sheet.py <midi_file.mid> [bars]")
        print("\nExample: python3 midi_to_sheet.py come_together.mid 8")
        sys.exit(1)
    
    midi_file = sys.argv[1]
    bars = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    
    if not os.path.exists(midi_file):
        print(f"Error: File '{midi_file}' not found")
        sys.exit(1)
    
    # Analyze MIDI
    analyzer = MIDIAnalyzer(midi_file)
    tracks = analyzer.analyze()
    
    if not tracks:
        print("\n⚠️  No tracks found in MIDI file")
        sys.exit(1)
    
    # Generate piano roll
    generator = PianoRollGenerator(tracks, bars=bars)
    output_file = f"{os.path.splitext(midi_file)[0]}_pianoroll.tex"
    generator.generate_latex(output_file)
    
    print(f"\n✅ Done! Compile with: xelatex {output_file}")


if __name__ == "__main__":
    main()

