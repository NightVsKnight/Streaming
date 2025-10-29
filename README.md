# NightVsKnight Video Transcripts

Select video transcripts from https://www.youtube.com/@NightVsKnight.

## Index

| Date | Title | URL | Transcript |
| ---- | ----- | --- | ---------- |
| 20251028 | NvK BTS: When Coding Turns Into Chaos (Music, AI, and Batman Soup!) | [4rM6KgNHKBg](https://youtu.be/4rM6KgNHKBg) | [20251028-nvk_behind_the_scenes_coding-\[4rM6KgNHKBg\].txt](20251028-nvk_behind_the_scenes_coding-[4rM6KgNHKBg].txt) |
| 20251027 | NvK BTS: Editing a Casey Neistat Short In My Batman Pajamas, And Other Deep Thoughts | [Q7yFYsJdd-o](https://youtu.be/Q7yFYsJdd-o) | [20251027-nvk_behind_the_scenes_coding-\[Q7yFYsJdd-o\].txt](20251027-nvk_behind_the_scenes_coding-[Q7yFYsJdd-o].txt) |
| 20251026 | NvK BTS: What Happens When You Let AI Code and Kids Interrupt | [ZpBUfLJMP3g](https://youtu.be/ZpBUfLJMP3g) | [20251026-nvk_behind_the_scenes_coding-\[ZpBUfLJMP3g\].txt](20251026-nvk_behind_the_scenes_coding-[ZpBUfLJMP3g].txt) |

## Info

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

### Prompt
This one seems to work ok:
```
Summarize the attached transcript into timestamped milestone titles for use in a YouTube video description.
* Each row is formatted as `[HH:]MM:SS text`, where the hour is optional.
* Summarize the transcript by meaning, not line-by-line.
* Merge related sections, remove filler or repetition, and capture all key insights, decisions, and takeaways.
* Output as one clean list where each line follows the format `[HH:]MM:SS text`; add the hour only if needed (do not format "00:MM:SS")
* Keep phrasing concise, professional, and easy to scan.

Do not reformat timestamps (keep as-is) or include any Markdown, numbering, or extra commentary.

Condense to be under 4500 characters (5000 YouTube description limit - ~500 for misc boilerplate)
```

Title:
```
Generate a click bait title for this prefixed with "NvK Behind The Scenes: "
```