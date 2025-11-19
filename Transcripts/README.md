# NightVsKnight Video Transcripts

Select video transcripts from https://www.youtube.com/@NightVsKnight.

## Index

| Date | Title | URL | Transcript |
| ---- | ----- | --- | ---------- |
| 20251028 | NvK BTS: When Coding Turns Into Chaos (Music, AI, and Batman Soup!) | [4rM6KgNHKBg](https://youtu.be/4rM6KgNHKBg) | [20251028-nvk_behind_the_scenes_coding-\[4rM6KgNHKBg\].txt](20251028-nvk_behind_the_scenes_coding-[4rM6KgNHKBg].txt) |
| 20251027 | NvK BTS: Editing a Casey Neistat Short In My Batman Pajamas, And Other Deep Thoughts | [Q7yFYsJdd-o](https://youtu.be/Q7yFYsJdd-o) | [20251027-nvk_behind_the_scenes_coding-\[Q7yFYsJdd-o\].txt](20251027-nvk_behind_the_scenes_coding-[Q7yFYsJdd-o].txt) |
| 20251026 | NvK BTS: What Happens When You Let AI Code and Kids Interrupt | [ZpBUfLJMP3g](https://youtu.be/ZpBUfLJMP3g) | [20251026-nvk_behind_the_scenes_coding-\[ZpBUfLJMP3g\].txt](20251026-nvk_behind_the_scenes_coding-[ZpBUfLJMP3g].txt) |

## The Process

Browse to the actual recording, not the live stream.
Example:
* **https://youtu.be/uApIYCv-w0s**  
  -or-  
  **https://www.youtube.com/watch?v=uApIYCv-w0s**
-NOT-
* https://www.youtube.com/live/uApIYCv-w0s

It can take up to 24 hours before YouTube generates a transcript.

I use [Copy Youtube Transcript](https://chromewebstore.google.com/detail/copy-youtube-transcript/mpfdnefhgmjlbkphfpkiicdaegfanbab)
to easily download the transcript.  
To clean this in Visual Studio Code:
Find: `\((.*\d:\d\d)\) `
Replace: `$1 `

Sometimes `Copy Youtube Transcript` fails with `No video ID found`.  
When that happens I just manually select and copy the transcript.  
A manually selected transcript will paste like:
```
0:07
Let's see. There's my microphone.
0:13
And capture Discord.
...
```
To fix this in Visual Studio Code:
Find: `(\d:\d\d)\n`
Replace: `$1 `

### Prompts

Here’s a clean, ready-to-paste prompt set that exactly reproduces the workflow you’ve been developing for your NvK Behind The Scenes transcripts — precise, structured, and enforceable.
Each one is tuned for the correct output length (< 3500 chars for timestamp sections), formatting, and tone control.

These six prompts together reproduce your full NvK workflow pipeline — from raw transcript → concise summary → thought-map → visualization → title → post-summary reflections — all consistent, grounded, and YouTube-ready.

#### Generate Original Timeline Summary (<3500 chars)
```
Summarize the attached transcript into timestamped milestone highlights for use in a YouTube video description.

Formatting rules (strict):
• Each milestone must be exactly one line, formatted as:
[HH:]MM:SS concise summary text
• Do not include blank lines, bullet points, or extra formatting.
• Include the hour only if necessary (no leading zeros).
• Keep each line under ~120 characters, written in a concise, scannable, and professional style.
• Each line should summarize what’s being discussed or done around that time, not a transcript snippet.

Content rules:
• Merge nearby timestamps that refer to the same topic.
• Capture key actions, insights, decisions, and technical problem-solving steps.
• Focus on moments that matter for viewers following the project’s progress or learning process.
• Maintain chronological order and readability for YouTube viewers scanning the description.

Length goal:
• The final summary must stay under 3500 characters total (including timestamps).
```

#### Generate Deterministic ASCII Thought-Map Timeline Summary
```
Using the attached transcript, generate a timestamped ASCII “thought-map timeline” summary that visually shows both the chronological flow of events and the tangents explored throughout the stream.

Formatting and layout rules (strict and precise):
1. Structure Overview
  - The timeline must be vertical, one main column running top to bottom.
  - The main thread runs straight down the left side of the diagram.
  - Tangents are indented exactly three spaces deeper than their parent event.
  - Each tangent level uses one line-drawing character per indent level, never mixed.
  - Vertical alignment must remain intact — all timestamps and arrows must line up vertically.
2. Character Set (must use only these)
  - │ (U+2502) for vertical continuation lines
  - ├ (U+251C) for branch start points
  - └ (U+2514) for branch end points
  - ─ (U+2500) for horizontal connectors
  - ▶ (U+25B6) for forward progress arrows
  - → (U+2192) for directional connectors
  - Standard ASCII letters, digits, spaces, and punctuation
  - No angle brackets < >, bullets •, asterisks *, or markdown symbols.
3. Line Layout Rules
  - Each line starts with a timestamp in [HH:]MM:SS format.
  - Immediately after the timestamp, include two spaces, then the event description.
  - If the line represents a tangent, it must be indented exactly three spaces plus one │ or branch symbol (├ or └).
  - All branch lines use ├─→ for ongoing tangents and └── for the last tangent under that event.
  - Use exactly one space before and after each arrow or connector for readability.
  - No line may exceed 120 visible characters.
  - No trailing spaces at the end of any line.
  - Blank lines are used only between major sections (main thread blocks).
4. Flow Representation
  - The main thread uses the ─▶ arrow after the timestamp.
  - Each tangent or sub-topic starts from its parent line using ├─→ or └──.
  - When a tangent rejoins the main thread, indicate this with └── rejoin ... on its final branch line.
  - Do not use curved ASCII art or alternate characters.
  - Maintain strict vertical continuity with │ characters to visually link nested tangents.
5. Content Rules
  - Each event must summarize one clear idea or action (setup, fix, discovery, reflection).
  - Merge nearby timestamps that cover the same continuous topic.
  - Note where tangents start, branch, and re-join.
  - Keep tone factual and reflective — never speculative.
  - Keep total output under 3500 characters, including timestamps and symbols.
6. Ending Section (mandatory)
  - After the final timestamped event, insert a horizontal rule line of ─ characters, 46 long.
  - Then include this exact legend, word-for-word and layout-preserved:
──────────────────────────────────────────────
LEGEND
──▶ main thread progression
├─→ tangent branch
└── rejoined thread or loop completion

7. Example Template (must match this visual format)
00:00  STREAM START
   │
00:25─▶ "Starting Soon" setup → lowers music, learns pacing
   │
01:00─▶ Transcript workflow → defines hashtags for notes
   │   ├─→ tangent: AI summarizer idea and repo automation
   │   └── rejoin main focus @05:00
   │
09:07─▶ Brainstorms Stream Deck hotkeys (loop, random, pause)
   │   ├─→ tangent: GitHub issue automation with Copilot
   │   └── rejoin after validation @13:00
```

#### Generate Tree-of-Thought Timeline Summary (<3500 chars)
```
Create an indented ASCII “tree-of-thought” timeline summarizing the transcript.
Use indentation and simple ASCII symbols to represent main topics, sub-topics, and tangents.

Formatting rules:
• Each node includes a timestamp and short description.
• Use characters like │ ├ └ → to show branches and re-joins.
• Keep under 3500 characters total.
• Capture both chronology and mental drift — show where tangents form, reconnect, or drop.
• Style for clarity and flow, not fancy ASCII art.
```

#### Generate Valid Mermaid & Graphviz Visuals
```
Using the transcript summary and timestamps, create both a working Mermaid and Graphviz diagram that accurately visualize the timeline and tangent structure.

Requirements:
• Mermaid code must render correctly at https://mermaid.live
• Graphviz DOT code must render correctly at https://dreampuf.github.io/GraphvizOnline/
• Both must include timestamped nodes with directional flow arrows showing chronology.
• Dashed lines represent tangents or returns.
• Keep both diagrams concise and under ~200 lines total combined.
• Verify syntax validity (no unmatched braces, colons, or malformed nodes).
```

#### Generate Click-Bait Title (Grounded & Honest)
```
Generate a click-bait-style YouTube title prefixed with "NvK Behind The Scenes":

Requirements:
• Must stay grounded strictly in the events of the transcript — do not invent future actions or speculative outcomes.
• Capture humor, irony, or chaos in tone while remaining truthful.
• Aim for 90–120 characters max.
• Focus on what actually happened: coding chaos, mic fixes, chat hacks, distractions, tangents, etc.
```

#### Generate Post-Summary Sections
```
Post-summary these sections:
	1.	🔖 Hashtag / Note-to-Self Mentions – summarize any segments mentioning “hashtag,” “note to self,” “chatbot,” etc.
	2.	🧠 Action Items – summarize things I told myself to look into, fix, research, or follow up on.
	3.	🎯 Stream Focus Tips – suggest ways I can improve staying on topic in future streams.
	4.	🤡 Crazy? – Psycho-analyze my stream to evaluate my mental health (humorous/self-aware tone).
	5.	🚀 Creative Follow-Ups – recommend new, bigger, or bolder content ideas inspired by the stream’s actual topics.
	6.	🔑 Trigger Words / Key Phrases – suggest more intuitive key-phrase triggers to mark transcript moments for future automation.

Output format:
• Produce a clean, ready-to-paste text block with no markdown or numbering.
• Every timestamp line (if present) must be one self-contained highlight line.
• Keep tone professional yet witty; short paragraphs per section.
```
