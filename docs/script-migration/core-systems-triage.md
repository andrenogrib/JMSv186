# Core Systems Triage

Created on 2026-03-25 after the live mob-combat debugging session.

## Why this file exists

The repository comparison showed that `OpenMS`, `odinms`, and `Cosmic` are useful script donors.

However, the newest round of in-game issues showed that not every visible bug should be solved by importing script logic from another server.

This file separates:

- what can be improved safely by reusing NPC/quest scripts
- what should stay inside the current BMS core and be debugged packet-by-packet

## Summary

The safest strategy is hybrid:

1. Reuse `OpenMS` and `odinms` for NPC/quest cleanup.
2. Use `Cosmic` selectively for cleaner English text and later-content flow.
3. Fix combat, packet, UI, and drop anomalies directly in the current BMS implementation.

This is the lowest-risk path for avoiding regressions.

## Important correction

`OpenMS` is not "more current" than the current BMS network/core stack.

It is more compatible for script migration because:

- it uses the classic `cm/qm` model
- it has broad script coverage
- it avoids most of the JP/KR/garbled text currently present in BMS

That does **not** mean it is a safe donor for live packet/combat behavior.

## Findings from the latest mob-combat session

### 1. Missing EXP/meso popup visuals

Observed behavior:

- mobs now die correctly
- EXP is granted
- the client does not show the visual gain popup near the skill/hotkey area

Current BMS code path already exists:

- `MapleMonster` calls `gainExpMonster(..., true, ...)`
- `MapleCharacter` sends `GainEXP_Monster(...)`
- `MapleCharacter.gainMeso(..., true, ...)` sends `showMesoGain(...)`
- those messages are serialized in `ResCWvsContext.Message(...)`

Interpretation:

- this does **not** look like a missing gameplay rule
- it strongly suggests a packet-layout or version-field mismatch in the current message encoding

Practical conclusion:

- do not try to fix this by pulling script logic
- debug the current message packets directly

## 2. Ranged attacks killing before the projectile visually lands

Observed behavior:

- ranged attack works again
- mob dies before the visual projectile appears to connect

Relevant current area:

- `src/odin/handling/channel/handler/PlayerHandler.java`
- request parsing in the current BMS packet layer
- remote attack broadcast / hit timing

Interpretation:

- this is combat sync / packet timing territory
- it is likely caused by how the current BMS parses or emits ranged-attack data, not by NPC/quest content

Practical conclusion:

- fix surgically using packet traces and code traces
- do not replace combat logic wholesale with `OpenMS` or `Cosmic`

## 3. Drops feel too generous

Observed behavior:

- mobs appear to drop too much

Current findings:

- `properties/kaede.properties` currently sets:
  - `server.rate.exp = 1`
  - `server.rate.meso = 1`
  - `server.rate.drop = 1`
- the drop formula in `src/tacos/server/map/MonsterDrop.java` multiplies:
  - DB chance
  - channel drop rate
  - player drop modifier
  - drop buff
  - showdown modifier
- meso drops also multiply meso and drop modifiers

Interpretation:

- this does not look like a simple config-rate problem
- likely causes are:
  - inflated DB drop chances
  - formula scaling mismatch
  - custom player/drop modifiers

Practical conclusion:

- audit formula and DB tables before changing server rates
- do not assume script migration will improve this

## What the donor repos are good for

### `OpenMS`

Best use:

- low-risk NPC and quest ports
- beginner scripts
- town service NPCs
- classic quests with standard `cm/qm` helpers

Not the right tool for:

- BMS packet layout issues
- v24/v186-style client message mismatches
- combat sequencing problems

### `odinms`

Best use:

- checking intended original behavior
- validating simple quest/NPC flow
- comparing against a smaller and cleaner baseline

Not the right tool for:

- bulk modern content import
- packet/core adoption in the current BMS stack

### `Cosmic`

Best use:

- cleaner English text
- nicer dialogue flow
- later-content script references

Not the right tool for:

- blind copy-paste
- fixing current core gameplay sync issues
- safe bulk imports without API adaptation

## Recommended workflow from here

### Safe bulk work

Do in controlled batches:

- import or rewrite NPC/quest scripts from `OpenMS`
- cross-check with `odinms`
- borrow text selectively from `Cosmic`

### Surgical core work

Do issue-by-issue:

1. fix EXP/meso popup packet behavior
2. fix ranged attack timing / parse / broadcast behavior
3. audit and rebalance drop formula and drop data

## Final recommendation

If the goal is "do not ruin the whole project", the safest path is:

- bulk migration for scripts only
- packet-by-packet debugging for combat/UI/drop issues

That keeps the current BMS core intact while still letting the project benefit from the cleaner GMS-based repos.
