# Music Theory Analysis Guide

This guide explains the philosophy and approach for writing `theory_analysis` content in `songs.json`.

## Core Philosophy

**Think like a producer teaching students to CREATE, not just analyze.**

The goal is to help students understand:
1. **What's actually happening** in simple, clear terms
2. **Why it works** from a compositional perspective  
3. **How they can apply it** to their own beats

❌ **Avoid**: Academic complexity, jargon overload, purely analytical descriptions  
✅ **Embrace**: Simple language, compositional insights, production wisdom

---

## The Process

### Step 1: Analyze the Actual MIDI Files

**Before writing anything**, examine the MIDI to see what's really there. Create a quick Python script to extract:

```python
# Example analysis script
import mido

midi = mido.MidiFile('path/to/file.mid')
# Extract actual notes, not assumptions
# See what intervals, rhythms, patterns are REALLY used
```

**Don't assume** based on how the song is commonly described. The Still D.R.E. example taught us:
- Common wisdom: "four-note piano riff"  
- Reality: Two-note dyad (C-A) repeated

### Step 2: Find the Simplest Explanation

Ask: **"What's the simplest way to explain this that's still accurate?"**

**Example from Still D.R.E.:**
- ❌ Complex: "A-B-E-G creates i-II-v-bVII with Neapolitan chord implications"
- ✅ Simple: "Two chords (Am-Em) connected by smooth bass notes (B and G)"

**Key insight**: B and G aren't separate chords—they're **connector notes** (walkups/walkdowns).

### Step 3: Think Compositionally, Not Analytically

Frame theory from a **"how to build this"** perspective:

- ❌ Analytical: "The track employs a suspension through harmonic stasis"
- ✅ Compositional: "The piano stays on C-A while the bass moves to E, creating a suspension effect. This is how you get movement from static elements."

---

## Writing Style Guidelines

### 1. Structure Your Analysis

Use clear sections with bold headers:

```latex
\textbf{Key:} [Key and any modal notes]

\textbf{The [Main Element]:} [Describe the most iconic part]

\textbf{The [Bass/Harmony/etc.]:} [Break down other elements]

\textbf{Why It Works:} [The compositional magic]

\textbf{Why This Matters for Production:} [The takeaway lesson]
```

### 2. Use Colored Text for Emphasis

Highlight key concepts with LaTeX color commands:
- `\purple{...}` - Main melodic/harmonic concepts
- `\bluepurple{...}` - Bass lines, foundational elements
- `\greentext{...}` - Technical terms (connector notes, suspension, etc.)
- `\orangetext{...}` - Important effects/techniques

**Example:**
```latex
The bass uses \greentext{smooth connector notes} between the 
\bluepurple{two main notes} (A and E).
```

### 3. Keep Intervals Simple and Clear

When describing intervals, use natural language:
- ✅ "drops down to E, falling a 5th"
- ✅ "rises up to A—just a whole step"  
- ✅ "G is part of the Em chord"

Avoid:
- ❌ "leads up a whole step" (confusing direction)
- ❌ "descends via chromatic passing tone" (too academic)

### 4. Use Bullet Lists for Clarity

When breaking down patterns, use `\begin{itemize}`:

```latex
\begin{itemize}
\item Beats 0-3: \textbf{A} (the iv chord)
\item Beat 3: \textbf{B} (drops down to E, falling a 5th)
\item Beats 4-7: \textbf{E} (the i chord)
\end{itemize}
```

### 5. End with the Production Lesson

Always conclude with practical takeaway:

```latex
\textbf{Why This Matters for Production:} [Summarize the lesson]
```

This should be **actionable**—something students can apply to their own beats.

---

## Key Principles (from Still D.R.E. Example)

### Principle 1: Simplify Without Losing Accuracy

**The Challenge:** Still D.R.E. uses A-B-E-G in the bass.

**Wrong approach:** Call it four separate chords with Roman numeral analysis  
**Right approach:** Two chords (Am, Em) with connector notes (B, G)

**Why it's better:** Students can immediately apply "use connector notes between bass changes."

### Principle 2: Name the Compositional Technique

Identify the **production technique** being used:

- Still D.R.E.: **Suspension** (static top, moving bottom)
- Come Together: **Vamp** (repeated pattern creating groove through repetition)

This gives students a **tool** they can use in their own work.

### Principle 3: Explain "Why It Works"

Don't just describe—explain the **magic**:

> "The contrast between the *static* piano riff (two notes, never changing) and the *moving* bass line creates harmonic interest while maintaining the hypnotic G-Funk vibe."

This teaches **compositional thinking**.

### Principle 4: Consider the Key from a Modal Perspective

Don't force traditional harmonic analysis. Consider:
- Songs that start on non-tonic chords (iv-i instead of i-iv)
- Modal borrowing and mixolydian/dorian/aeolian feels
- Vamps and grooves that don't follow functional harmony

**Example:** Still D.R.E. starts on Am (the iv) in E minor—this creates a different feel than starting on Em.

---

## Common Patterns to Look For

When analyzing a song, look for these production techniques:

### 1. **Suspension/Pedal Tones**
One element stays static while another moves
- Example: Still D.R.E. (piano stays, bass moves)

### 2. **Connector Notes/Passing Tones**
Notes that smooth the transition between chord tones
- Example: B connecting A to E, G connecting E to A

### 3. **Two-Chord Grooves**
Many great songs use just two chords with variation
- Look for how they create interest (rhythm, timbre, suspension)

### 4. **Dyads/Intervals Instead of Full Chords**
Minimal voicings that leave space
- Example: C-A dyad instead of full Am7 chord

### 5. **Modal Interchange**
Borrowing from parallel modes (major/minor, dorian/mixolydian)
- Look for raised/lowered scale degrees

### 6. **Rhythmic/Melodic Motifs**
Simple patterns that repeat (hypnotic, memorable)
- Analyze the rhythm as much as the harmony

---

## LaTeX Formatting Cheatsheet

```latex
% Bold section headers
\textbf{Key:} E minor

% Colored emphasis
\purple{four notes}
\bluepurple{bass pattern}
\greentext{suspension}
\orangetext{tension}

% Italics for contrast/emphasis
\textit{static} top, \textit{moving} bottom

% Bullet lists
\begin{itemize}
\item First point
\item Second point
\end{itemize}

% Line breaks between paragraphs
Use \n\n in the JSON string

% Special characters that need escaping
\# for #
\& for &
```

---

## Red Flags to Avoid

### ❌ Too Academic
"The Neapolitan II chord creates chromatic mediant relationships"

### ❌ Too Vague  
"The harmony creates an interesting sound"

### ❌ Assumes Prior Knowledge
"Using the Lydian mode's raised 4th" (without explaining what that means)

### ❌ Overthinking Simple Things
Treating connector notes as complex chord substitutions

---

## The "Still D.R.E." Gold Standard

Use this as a reference for the ideal approach:

```json
"theory_analysis": "\\textbf{Key:} E minor (starting on the iv chord)

\\textbf{The Piano Riff:} The iconic riff is brilliantly simple—just 
two notes played together: \\purple{C and A}. This dyad repeats in 
steady 8th notes throughout the entire track without ever changing...

\\textbf{The Bass Pattern—Keep It Simple:} The bass alternates between 
just \\bluepurple{two main notes}: A and E (the iv and i in E minor). 
But here's the magic: instead of jumping directly between them, the 
bass uses \\greentext{smooth connector notes}:
\\begin{itemize}
\\item Beats 0-3: \\textbf{A} (the iv chord)
\\item Beat 3: \\textbf{B} (drops down naturally to E, falling a 5th)
\\item Beats 4-7: \\textbf{E} (the i chord)
\\item Beat 7: \\textbf{G} (part of the Em chord, rises up to A)
\\end{itemize}

\\textbf{The Suspension Effect:} Here's what makes this progression so 
hypnotic: the piano dyad (C-A) \\textit{doesn't change} when the bass 
moves from A to E...

\\textbf{Why This Matters for Production:} This track shows you don't 
need complex chords or progressions. Two simple chords (Am and Em), 
smooth bass connector notes, and a suspension effect—that's the whole 
harmonic foundation of one of hip-hop's most iconic beats."
```

**What makes this good:**
1. ✅ Starts with key (provides context)
2. ✅ Analyzes from most to least prominent element
3. ✅ Uses clear, simple language
4. ✅ Identifies the compositional technique (suspension)
5. ✅ Ends with actionable production wisdom
6. ✅ Accurate to the actual MIDI content
7. ✅ Accessible to beginners, interesting to advanced students

---

## Quick Checklist

Before finalizing a `theory_analysis`, ask:

- [ ] Did I analyze the actual MIDI files first?
- [ ] Is this the simplest accurate explanation?
- [ ] Does it teach a compositional technique?
- [ ] Would a student know how to apply this to their own beat?
- [ ] Did I use colored text for emphasis?
- [ ] Did I end with "Why This Matters for Production"?
- [ ] Is the language accessible (no unnecessary jargon)?
- [ ] Are interval descriptions clear and natural?

---

## Remember

**Your audience is beatmakers who want to create, not music theory students who want to analyze.**

Every theory concept should serve the goal: **"How can I use this in my own production?"**

When in doubt, choose clarity over complexity.

