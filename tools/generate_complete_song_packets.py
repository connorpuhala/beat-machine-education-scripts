#!/usr/bin/env python3
"""
Complete Song Packet Generator for Beatmaking: Learn By Doing

This script generates comprehensive song packets that include:
- Page 1: Cover sheet with metadata
- Page 2+: Piano roll visualizations from MIDI
- Following pages: Song context, learning points, and comparables
"""

import json
import os
import subprocess
import re
from pathlib import Path
import sys

# Add the multi_midi_to_pianoroll module to import its classes
sys.path.insert(0, str(Path(__file__).parent))
from multi_midi_to_pianoroll import MultiMIDIAnalyzer, UnifiedPianoRollGenerator

# Get the project root directory (parent of tools/)
PROJECT_ROOT = Path(__file__).parent.parent

# Template for complete song packet
TEMPLATE_HEADER = r'''\documentclass[11pt,letterpaper]{article}

% Packages
\usepackage[margin=0.85in]{geometry}
\usepackage{fontspec}
\usepackage{xcolor}
\usepackage{tikz}
\usetikzlibrary{patterns}
\usepackage{tcolorbox}
\usepackage{enumitem}
\usepackage{graphicx}
\usepackage{setspace}
\usepackage{parskip}
\usepackage{multicol}
\usepackage[hidelinks]{hyperref}

% Font setup
\setmainfont{ElMessiri-Regular}[
    Path = ../../../assets/fonts/,
    Extension = .ttf,
    BoldFont = ElMessiri-Regular,
    BoldFeatures = {FakeBold=1.5},
    Scale=1.0
]

% Define colors
\definecolor{purple}{RGB}{138,43,226}
\definecolor{blue}{RGB}{30,144,255}
\definecolor{green}{RGB}{34,139,34}
\definecolor{red}{RGB}{220,20,60}
\definecolor{orange}{RGB}{255,140,0}
\definecolor{lightgray}{RGB}{245,245,245}
\definecolor{darkgray}{RGB}{100,100,100}

% Custom commands for colored text
\newcommand{\purple}[1]{\textcolor{purple}{\textbf{#1}}}
\newcommand{\bluepurple}[1]{\textcolor{blue}{\textbf{#1}}}
\newcommand{\greentext}[1]{\textcolor{green}{\textbf{#1}}}
\newcommand{\redtext}[1]{\textcolor{red}{\textbf{#1}}}
\newcommand{\orangetext}[1]{\textcolor{orange}{\textbf{#1}}}

% Header and footer
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\fancyfoot[C]{\small\thepage}

% Title formatting
\usepackage{titlesec}
\titleformat{\section}
  {\LARGE\bfseries\sffamily\color{darkgray}}
  {}
  {0em}
  {}
  [\vspace{-0.5em}\rule{\textwidth}{0.5pt}]
\titleformat{\subsection}
  {\Large\bfseries\sffamily\color{darkgray}}
  {}
  {0em}
  {}

% Better spacing
\setlength{\parskip}{0.6em}
\setstretch{1.15}

\begin{document}

\thispagestyle{empty}

% PAGE 1: COVER SHEET - VERTICALLY CENTERED
\vspace*{\fill}

\begin{center}
{\Huge\bfseries\sffamily {{SONG_TITLE}}}

\vspace{0.3cm}

{\LARGE by {{ARTIST_NAME}}}

\vspace{0.5cm}

\begin{tikzpicture}
    % Decorative music notes
    \fill[purple] (0,0) circle (0.2cm);
    \draw[purple, line width=1.5pt] (0.2,0) -- (0.2,1);
    \fill[blue] (1,0.2) circle (0.2cm);
    \draw[blue, line width=1.5pt] (1.2,0.2) -- (1.2,1.2);
    \fill[green] (2,0) circle (0.2cm);
    \draw[green, line width=1.5pt] (2.2,0) -- (2.2,1);
\end{tikzpicture}

\vspace{0.5cm}

\rule{0.8\textwidth}{0.5pt}
\end{center}

\vspace{0.5cm}

% SONG DETAILS BOX
\begin{tcolorbox}[colback=lightgray,colframe=purple,width=\textwidth,arc=3mm,boxrule=1pt]
\begin{multicols}{2}
\textbf{\purple{BPM:}} {{SONG_BPM}}

\textbf{\bluepurple{Key:}} {{SONG_KEY}}

\textbf{\greentext{Year:}} {{SONG_YEAR}}

\textbf{\orangetext{Album:}} {{SONG_ALBUM}}

\textbf{\redtext{Genre:}} {{SONG_GENRE}}
\end{multicols}
\end{tcolorbox}

\vspace*{\fill}

\newpage

% PAGE 2+: PIANO ROLLS
{{PIANO_ROLLS}}

\newpage

% MUSIC THEORY ANALYSIS
\section*{Music Theory Analysis}

{{THEORY_ANALYSIS}}

\vspace{0.5cm}

% ABOUT THE ARTIST
\section*{About {{ARTIST_NAME}}}

{{ARTIST_BIO}}

\vspace{0.5cm}

% ABOUT THE SONG
\section*{About "{{SONG_TITLE}}"}

{{SONG_CONTEXT}}

\vspace{0.5cm}

% MUSICAL ELEMENTS
\section*{Key Musical Elements}

\subsection*{What Makes This Beat Special:}

\begin{itemize}[leftmargin=*]
{{KEY_ELEMENTS}}
\end{itemize}

\subsection*{What You'll Learn:}

\begin{itemize}[leftmargin=*]
{{LEARNING_POINTS}}
\end{itemize}

\vspace{0.5cm}

% COMPARABLE SONGS
\section*{If You Like This, Check Out:}

\begin{tcolorbox}[colback=blue!5,colframe=blue,width=\textwidth,arc=3mm,boxrule=1pt]
\textbf{Similar Grooves \& Vibes:}

\begin{itemize}[leftmargin=*, itemsep=0.3em]
{{COMPARABLES}}
\end{itemize}
\end{tcolorbox}

\vspace{1cm}

% FOOTER
\begin{center}
\rule{0.8\textwidth}{0.5pt}

\vspace{0.3cm}

\textbf{Beatmaking: Learn By Doing}

\textit{Learn music through \purple{beats} — A fun, \bluepurple{human} path to modern music making}

\vspace{0.3cm}

\small www.makebeatsanywhere.com | connor@makebeatsanywhere.com | @the\_beat\_machine\_

\vspace{0.3cm}

\rule{0.8\textwidth}{0.5pt}
\end{center}

\end{document}
'''


def sanitize_filename(filename):
    """Convert song title to safe filename"""
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'[-\s]+', '_', filename)
    return filename.lower()


def generate_piano_roll_section(midi_folder_name, song_title):
    """Generate piano roll LaTeX code from MIDI files"""
    
    midi_dir = PROJECT_ROOT / "content" / "midi" / midi_folder_name
    
    if not midi_dir.exists():
        print(f"   ⚠️  Warning: MIDI folder not found at {midi_dir}")
        print(f"   Skipping piano rolls for this song.")
        return "% No MIDI files found\n\\textit{Piano rolls will be added when MIDI files are available.}\n\n\\newpage\n"
    
    # Analyze MIDI files
    analyzer = MultiMIDIAnalyzer(str(midi_dir))
    tracks = analyzer.analyze()
    
    if not tracks:
        return "% No MIDI tracks found\n\\textit{Piano rolls will be added when MIDI files are available.}\n\n\\newpage\n"
    
    # Generate piano roll LaTeX (inline, not as separate file)
    total_beats = analyzer.max_length_beats
    
    # Build piano roll sections
    piano_roll_latex = f"\\begin{{center}}\n{{\\Huge\\bfseries {song_title} — Piano Rolls}}\n\\end{{center}}\n\n\\vspace{{0.5cm}}\n\n"
    
    for i, track in enumerate(tracks):
        is_last = (i == len(tracks) - 1)
        piano_roll_latex += generate_single_track_latex(track, total_beats, i + 1, is_last_layer=is_last)
    
    return piano_roll_latex


def generate_single_track_latex(track, total_beats, layer_num, is_last_layer=False):
    """Generate LaTeX for a single piano roll track"""
    
    beats_per_bar = 4
    bars = int((total_beats + beats_per_bar - 1) // beats_per_bar)
    total_beats = bars * beats_per_bar
    
    # Calculate pitch range
    if track.notes:
        pitches = [n.pitch for n in track.notes]
        is_drum = 'drum' in track.name.lower()
        
        if is_drum:
            min_pitch = min(pitches)
            max_pitch = max(pitches)
        else:
            min_pitch = max(min(pitches) - 3, 21)
            max_pitch = min(max(pitches) + 3, 108)
    else:
        min_pitch, max_pitch = 60, 72
    
    latex = "\\noindent\\hspace{2.5cm}"
    target_width = 13
    x_scale = target_width / total_beats
    latex += f"\\begin{{tikzpicture}}[xscale={x_scale:.2f}, yscale=1.1]\n"
    
    # Draw grid
    latex += draw_piano_roll_grid(min_pitch, max_pitch, track.name, total_beats, show_bar_labels=is_last_layer)
    
    # Draw notes
    for note in track.notes:
        if note.start_time < total_beats:
            latex += draw_piano_roll_note(note, min_pitch, track.color)
    
    # Add label
    pitch_range = max_pitch - min_pitch
    y_center = ((pitch_range + 1) * 0.4) / 2
    label_x = total_beats + 0.5
    latex += f"\\node[rotate=90, font=\\Large\\bfseries, overlay] at ({label_x},{y_center}) {{{track.name.upper()}}};\n"
    
    latex += "\\end{tikzpicture}\n\n\\vspace{0.05cm}\n\n"
    
    return latex


def draw_piano_roll_grid(min_pitch, max_pitch, track_name, total_beats, show_bar_labels=False):
    """Draw piano roll grid"""
    latex = ""
    pitch_range = max_pitch - min_pitch
    y_max = (pitch_range + 1) * 0.4
    beats_per_bar = 4
    
    # Black keys shading
    black_keys = {1, 3, 6, 8, 10}
    for i in range(pitch_range + 1):
        pitch = min_pitch + i
        if (pitch % 12) in black_keys:
            y = i * 0.4
            latex += f"\\fill[black!8] (0,{y}) rectangle ({total_beats},{y + 0.4});\n"
    
    # Border
    latex += f"\\draw[black, very thick] (0,0) -- ({total_beats},0);\n"
    latex += f"\\draw[black, very thick] (0,{y_max}) -- ({total_beats},{y_max});\n"
    latex += f"\\draw[black, very thick] ({total_beats},0) -- ({total_beats},{y_max});\n"
    
    # Horizontal lines (pitches)
    for i in range(pitch_range + 1):
        pitch = min_pitch + i
        y = i * 0.4
        if pitch % 12 == 0:
            latex += f"\\draw[gray!50, thick] (0,{y}) -- ({total_beats},{y});\n"
        else:
            latex += f"\\draw[gray!20] (0,{y}) -- ({total_beats},{y});\n"
    
    # Vertical lines (beats and subdivisions)
    for subdivision in range(int(total_beats * 8) + 1):
        beat = subdivision / 8.0
        if beat > total_beats:
            continue
            
        if subdivision % 32 == 0:  # Bar lines
            bar_num = (subdivision // 32) + 1
            latex += f"\\draw[black, very thick] ({beat},0) -- ({beat},{y_max});\n"
            # Only show bar labels that are at the start of actual bars (not at the very end)
            if show_bar_labels and beat < total_beats:
                latex += f"\\node[below, font=\\large\\bfseries, overlay] at ({beat},-0.5) {{Bar {bar_num}}};\n"
        elif subdivision % 8 == 0:  # Beat lines
            latex += f"\\draw[gray!70] ({beat},0) -- ({beat},{y_max});\n"
        elif subdivision % 4 == 0:  # 8th notes
            latex += f"\\draw[gray!50] ({beat},0) -- ({beat},{y_max});\n"
        elif subdivision % 2 == 0:  # 16th notes
            latex += f"\\draw[gray!35] ({beat},0) -- ({beat},{y_max});\n"
        else:  # 32nd notes
            latex += f"\\draw[gray!20] ({beat},0) -- ({beat},{y_max});\n"
    
    # Note labels
    is_drum_track = 'drum' in track_name.lower()
    label_x = -0.3
    
    for i in range(pitch_range + 1):
        pitch = min_pitch + i
        y_center = i * 0.4 + 0.2
        
        if is_drum_track:
            drum_name = get_drum_name(pitch)
            if drum_name:
                latex += f"\\node[anchor=east, font=\\small, overlay] at ({label_x},{y_center}) {{{drum_name}}};\n"
        else:
            note_name = pitch_to_note_name(pitch)
            if pitch % 12 == 0:
                latex += f"\\node[anchor=east, font=\\small\\bfseries, overlay] at ({label_x},{y_center}) {{{note_name}}};\n"
            else:
                latex += f"\\node[anchor=east, font=\\small, overlay] at ({label_x},{y_center}) {{{note_name}}};\n"
    
    return latex


def draw_piano_roll_note(note, min_pitch, color):
    """Draw a single note on the piano roll"""
    x = note.start_time
    pitch_offset = note.pitch - min_pitch
    y_base = pitch_offset * 0.4 + 0.025
    width = max(note.duration, 0.15)
    
    full_height = 0.35
    sustain_height = 0.25
    attack_width = min(0.08, width * 0.3)
    
    opacity = 0.6 + (note.velocity / 127) * 0.4
    
    y_sustain = y_base + (full_height - sustain_height) / 2
    latex = f"\\fill[{color}, opacity={opacity:.2f}, rounded corners=1pt] ({x},{y_sustain}) rectangle ({x + width},{y_sustain + sustain_height});\n"
    latex += f"\\fill[{color}, opacity={min(1.0, opacity + 0.35)}, rounded corners=1pt] ({x},{y_base}) rectangle ({x + attack_width},{y_base + full_height});\n"
    
    return latex


def pitch_to_note_name(pitch):
    """Convert MIDI pitch to note name"""
    notes = ['C', 'C\\#', 'D', 'D\\#', 'E', 'F', 'F\\#', 'G', 'G\\#', 'A', 'A\\#', 'B']
    octave = (pitch // 12) - 1
    note = notes[pitch % 12]
    return f"{note}{octave}"


def get_drum_name(pitch):
    """Get drum name from MIDI pitch"""
    drum_map = {
        35: 'Kick', 36: 'Kick', 38: 'Snare', 40: 'Snare',
        37: 'Side Stick', 39: 'Clap',
        42: 'Hi-Hat Closed', 44: 'Hi-Hat Pedal', 46: 'Hi-Hat Open',
        41: 'Tom Low', 43: 'Tom Low-Mid', 45: 'Tom Mid', 47: 'Tom Mid-High', 48: 'Tom High',
        49: 'Crash', 51: 'Ride', 52: 'Crash China', 53: 'Ride Bell',
        54: 'Tambourine', 55: 'Splash', 56: 'Cowbell', 57: 'Crash', 59: 'Ride',
    }
    return drum_map.get(pitch, '')


def generate_complete_song_packet(song_data, midi_folder_name=None, tex_output_dir=None, pdf_output_dir=None):
    """Generate complete LaTeX file and compile to PDF"""
    
    if tex_output_dir is None:
        tex_output_dir = PROJECT_ROOT / "packets" / "songs" / "_generated"
    if pdf_output_dir is None:
        pdf_output_dir = PROJECT_ROOT / "packets" / "songs" / "_build"
    
    os.makedirs(tex_output_dir, exist_ok=True)
    os.makedirs(pdf_output_dir, exist_ok=True)
    
    # Generate piano rolls section
    if midi_folder_name is None:
        midi_folder_name = sanitize_filename(f"{song_data['artist']}_{song_data['title']}")
    
    piano_rolls_latex = generate_piano_roll_section(midi_folder_name, song_data['title'])
    
    # Format the rest of the data
    key_elements = "\n".join([f"\\item {elem}" for elem in song_data['key_elements']])
    learning_points = "\n".join([f"\\item {point}" for point in song_data['learning_points']])
    comparables = "\n".join([
        f"\\item \\textbf{{\"{comp['song']}\" - {comp['artist']}}} \\\\\n    \\textit{{{comp['reason']}}}"
        for comp in song_data['comparables']
    ])
    
    # Replace placeholders
    latex_content = TEMPLATE_HEADER.replace('{{SONG_TITLE}}', song_data['title'])
    latex_content = latex_content.replace('{{ARTIST_NAME}}', song_data['artist'])
    latex_content = latex_content.replace('{{SONG_BPM}}', song_data['bpm'])
    latex_content = latex_content.replace('{{SONG_KEY}}', song_data['key'])
    latex_content = latex_content.replace('{{SONG_YEAR}}', song_data['year'])
    latex_content = latex_content.replace('{{SONG_ALBUM}}', song_data['album'])
    latex_content = latex_content.replace('{{SONG_GENRE}}', song_data['genre'])
    latex_content = latex_content.replace('{{PIANO_ROLLS}}', piano_rolls_latex)
    latex_content = latex_content.replace('{{THEORY_ANALYSIS}}', song_data.get('theory_analysis', '\\textit{Theory analysis coming soon...}'))
    latex_content = latex_content.replace('{{ARTIST_BIO}}', song_data['artist_bio'])
    latex_content = latex_content.replace('{{SONG_CONTEXT}}', song_data['song_context'])
    latex_content = latex_content.replace('{{KEY_ELEMENTS}}', key_elements)
    latex_content = latex_content.replace('{{LEARNING_POINTS}}', learning_points)
    latex_content = latex_content.replace('{{COMPARABLES}}', comparables)
    
    # Create filename
    safe_filename = sanitize_filename(f"{song_data['artist']}_{song_data['title']}_complete")
    tex_file = tex_output_dir / f"{safe_filename}.tex"
    
    # Write LaTeX file
    with open(tex_file, 'w', encoding='utf-8') as f:
        f.write(latex_content)
    
    print(f"✓ Generated LaTeX: {tex_file}")
    
    # Compile to PDF
    try:
        subprocess.run(
            ['xelatex', '-interaction=nonstopmode', '-output-directory', '../_build', tex_file.name],
            cwd=str(tex_output_dir),
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✓ Compiled PDF: {safe_filename}.pdf")
        
        # Clean up auxiliary files
        for ext in ['.aux', '.log', '.out']:
            aux_file = pdf_output_dir / f"{safe_filename}{ext}"
            if aux_file.exists():
                aux_file.unlink()
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error compiling {safe_filename}: {e}")
        return False


def main():
    """Main function to generate all complete song packets"""
    songs_file = PROJECT_ROOT / "content" / "songs.json"
    
    with open(songs_file, 'r', encoding='utf-8') as f:
        songs = json.load(f)
    
    print(f"\n🎵 Generating {len(songs)} complete song packet(s)...\n")
    
    success_count = 0
    for song in songs:
        # Try to find MIDI folder (check multiple possible names)
        possible_names = [
            sanitize_filename(f"{song['artist']}_{song['title']}"),
            sanitize_filename(song['title']),
            song['title'].lower().replace(' ', '_').replace('.', '')
        ]
        
        midi_folder = None
        for name in possible_names:
            if (PROJECT_ROOT / "content" / "midi" / name).exists():
                midi_folder = name
                break
        
        if generate_complete_song_packet(song, midi_folder_name=midi_folder):
            success_count += 1
        print()
    
    print(f"\n✅ Successfully generated {success_count}/{len(songs)} complete song packets")
    print(f"📁 LaTeX files: packets/songs/_generated/")
    print(f"📁 PDFs saved in: packets/songs/_build/\n")


if __name__ == "__main__":
    main()

