# Current BMS Audit

## High-level result

The current BMS script engine is usable. The main risk sits in the script content itself.

## Main problems found

## 1. Mixed encoding and untranslated script content

There are many script files with non-ASCII content. A lot of them are Japanese comments or dialogue, and some are visibly corrupted strings.

Examples:

- `scripts/scripts_BMS/npc/2003.js`
- `scripts/scripts_BMS/npc/2013001.js`
- `scripts/scripts_BMS/npc/9020001.js`
- `scripts/scripts_BMS/quest/21000.js`

## 2. Placeholder or partially reconstructed scripts

Multiple scripts contain comments that show the content is incomplete or guessed:

- `テキスト不足`
- `適当`
- `原文ママ`
- `TODO`
- `Idk what data lol..`

Examples:

- `scripts/scripts_BMS/npc/1002000.js`
- `scripts/scripts_BMS/npc/1002103.js`
- `scripts/scripts_BMS/npc/1013207.js`
- `scripts/scripts_BMS/quest/21000.js`

## 3. Stub behavior where a real GMS script exists

Example:

- `scripts/scripts_BMS/npc/2003.js` is only a placeholder for Robin.
- The same NPC in all three donor repos already has a complete beginner-helper conversation tree in readable text.

## 4. Corrupted custom data / tutorial flow risk

Example:

- `scripts/scripts_BMS/quest/21000.js` contains `qm.forceStartQuest(21000, "..w?PGﾃ・・");`

That string is a strong indicator of encoding or data corruption. Even if the script does not hard-crash immediately, it is not something we should preserve blindly.

## What is probably safe to keep

- Scripts that are already in readable English and only use classic helpers
- Scripts whose flow matches the intended content and do not show placeholder comments
- Scripts already tested in-game without broken dialogue or progression

## What should be prioritized for replacement

Priority 1:

- Placeholder NPC dialogue
- Garbled beginner and tutorial scripts
- Early quests that write suspicious custom data

Priority 2:

- Simple town service NPCs with JP text only
- Helper NPCs that are readable in donor repos

Priority 3:

- Advanced quests that need API adaptation rather than direct replacement

## Why this matters for client stability

Bad script text does not always crash the server, but it can still create client-visible breakage:

- unreadable or blank dialogue
- wrong accept/decline flow
- broken tutorial prompts
- bad quest progress strings
- scripts that are functionally "there" but incomplete

## Boundary of this audit

This audit focuses on script-content quality.

It does not mean every current gameplay bug should be solved by importing scripts from donor repos.

During the live mob-combat debugging session, three notable issues were identified as core-facing rather than script-facing:

- missing EXP/meso popup visuals
- ranged attacks resolving before the projectile visually lands
- suspiciously generous drop behavior

Current state after the first server-side pass:

- EXP / meso / item pickup popup is now working again
- ranged timing is improved but still not fully aligned
- drop formula was reduced on the BMS server side but still needs ingame verification

Those belong to packet/combat/drop triage in the current BMS codebase, not to simple NPC/quest replacement work.

See `core-systems-triage.md` for the final split between safe script migration work and surgical core debugging.
