# Candidate Shortlist

This is the first batch I would target if the goal is to clean the script set without causing new client-side issues.

## Tier A: very good early targets

## `npc/2003.js`

Current state:

- Current BMS file is only a placeholder.

Recommended donor:

- `Cosmic/scripts/npc/2003.js`
- `OpenMS/scripts/npc/2003.js`
- `odinms/scripts/npc/2003.js`

Why:

- Same NPC role
- Clean GMS dialogue exists in all donor repos
- Uses only classic `cm.send*` flow
- Very likely to be a safe replacement candidate

Import level:

- Near-direct copy

## `npc/1002000.js`

Current state:

- Works as a taxi, but comments explicitly say the text is incomplete and partially guessed.

Recommended donor:

- `Cosmic/scripts/npc/1002000.js` for better content flow
- `OpenMS/scripts/npc/1002000.js` or `odinms/scripts/npc/1002000.js` as logic references

Why:

- Same NPC role
- Donor versions include the explanatory Victoria Island text, not just the movement menu

Import level:

- Small adaptation needed

Notes:

- `Cosmic` uses `cm.getJobId()`, while the current BMS exposes `cm.getJob()`
- `OpenMS/odinms` job checks also need a quick compatibility pass

## Tier B: good, but adapt before using

## `quest/21000.js`

Current state:

- Current BMS script contains suspicious corrupted custom data
- It is a high-value cleanup target

Recommended donor:

- `Cosmic/scripts/quest/21000.js`

Why:

- Cosmic version has a clean Aran tutorial flow
- Same quest intent

Import level:

- Medium adaptation

Notes:

- `Cosmic` uses `qm.showInfo(...)`
- The current BMS has `qm.AranTutInstructionalBubble(...)` but no `showInfo(...)`
- Port the effect call instead of blindly copying it

## `quest/1021.js`

Current state:

- Current BMS version is already readable and mostly usable

Recommended donor:

- Keep current version unless you specifically want the `Cosmic` polish

Why:

- Not every script needs replacement
- This one is a good example of a script that is already serviceable

Import level:

- Optional only

Notes:

- `Cosmic` adds nice touches, but also uses `updateHp(...)` and `showInfo(...)`

## Tier C: do not bulk-copy

Avoid blind imports for scripts that use:

- `showInfo(...)`
- `setQuestProgress(...)`
- `getQuestProgressInt(...)`
- `canHoldAll(...)`
- `getJobId()`
- wedding or marriage gift helpers
- event-instance-specific helpers
- rich party/guild/family APIs

These are most common in `Cosmic`, and some exist because Cosmic exposes a richer scripting API than the current BMS.

## Best donor by category

| Category | Best source | Why |
|---|---|---|
| Placeholder beginner NPCs | `OpenMS` or `Cosmic` | Both have readable full scripts |
| Original/simple logic check | `odinms` | Best reference baseline |
| Rich English text | `Cosmic` | Cleanest dialogue |
| Low-risk bulk cleanup | `OpenMS` | Biggest classic-compatible pool |

