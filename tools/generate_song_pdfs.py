#!/usr/bin/env python3
"""
Song Packet Generator for Beatmaking: Learn By Doing

This script generates individual PDF packets for each song from the songs.json file.
"""

import json
import os
import subprocess
import re
from pathlib import Path

# Get the project root directory (parent of tools/)
PROJECT_ROOT = Path(__file__).parent.parent

# Template for the song packet
TEMPLATE = r'''\documentclass[11pt,letterpaper]{article}

% Packages
\usepackage[margin=0.85in]{geometry}
\usepackage{fontspec}
\usepackage{xcolor}
\usepackage{tikz}
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

% HEADER
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
    # Remove special characters and replace spaces with underscores
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'[-\s]+', '_', filename)
    return filename.lower()


def generate_song_packet(song_data, tex_output_dir=None, pdf_output_dir=None):
    """Generate LaTeX file and compile to PDF for a single song"""
    
    # Set default directories relative to project root
    if tex_output_dir is None:
        tex_output_dir = PROJECT_ROOT / "packets" / "songs" / "_generated"
    if pdf_output_dir is None:
        pdf_output_dir = PROJECT_ROOT / "packets" / "songs" / "_build"
    
    # Create output directories if they don't exist
    os.makedirs(tex_output_dir, exist_ok=True)
    os.makedirs(pdf_output_dir, exist_ok=True)
    
    # Format the data
    key_elements = "\n".join([f"\\item {elem}" for elem in song_data['key_elements']])
    learning_points = "\n".join([f"\\item {point}" for point in song_data['learning_points']])
    
    comparables = "\n".join([
        f"\\item \\textbf{{\"{comp['song']}\" - {comp['artist']}}} \\\\\n    \\textit{{{comp['reason']}}}"
        for comp in song_data['comparables']
    ])
    
    # Replace placeholders in template
    latex_content = TEMPLATE.replace('{{SONG_TITLE}}', song_data['title'])
    latex_content = latex_content.replace('{{ARTIST_NAME}}', song_data['artist'])
    latex_content = latex_content.replace('{{SONG_BPM}}', song_data['bpm'])
    latex_content = latex_content.replace('{{SONG_KEY}}', song_data['key'])
    latex_content = latex_content.replace('{{SONG_YEAR}}', song_data['year'])
    latex_content = latex_content.replace('{{SONG_ALBUM}}', song_data['album'])
    latex_content = latex_content.replace('{{SONG_GENRE}}', song_data['genre'])
    latex_content = latex_content.replace('{{ARTIST_BIO}}', song_data['artist_bio'])
    latex_content = latex_content.replace('{{SONG_CONTEXT}}', song_data['song_context'])
    latex_content = latex_content.replace('{{KEY_ELEMENTS}}', key_elements)
    latex_content = latex_content.replace('{{LEARNING_POINTS}}', learning_points)
    latex_content = latex_content.replace('{{COMPARABLES}}', comparables)
    
    # Create filename
    safe_filename = sanitize_filename(f"{song_data['artist']}_{song_data['title']}")
    tex_file = tex_output_dir / f"{safe_filename}.tex"
    
    # Write LaTeX file
    with open(tex_file, 'w', encoding='utf-8') as f:
        f.write(latex_content)
    
    print(f"✓ Generated LaTeX: {tex_file}")
    
    # Compile to PDF
    # Change to the directory containing the .tex file so relative paths work correctly
    try:
        subprocess.run(
            ['xelatex', '-interaction=nonstopmode', '-output-directory', '../_build', tex_file.name],
            cwd=str(tex_output_dir),
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✓ Compiled PDF: {safe_filename}.pdf")
        
        # Clean up auxiliary files from build directory
        for ext in ['.aux', '.log', '.out']:
            aux_file = pdf_output_dir / f"{safe_filename}{ext}"
            if aux_file.exists():
                aux_file.unlink()
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error compiling {safe_filename}: {e}")
        return False


def main():
    """Main function to generate all song packets"""
    # Load songs data from content directory
    songs_file = PROJECT_ROOT / "content" / "songs.json"
    
    with open(songs_file, 'r', encoding='utf-8') as f:
        songs = json.load(f)
    
    print(f"\n🎵 Generating {len(songs)} song packet(s)...\n")
    
    success_count = 0
    for song in songs:
        if generate_song_packet(song):
            success_count += 1
        print()  # Empty line between songs
    
    print(f"\n✅ Successfully generated {success_count}/{len(songs)} song packets")
    print(f"📁 LaTeX files: packets/songs/_generated/")
    print(f"📁 PDFs saved in: packets/songs/_build/\n")


if __name__ == "__main__":
    main()

