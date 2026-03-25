# Script Migration Study

Created on 2026-03-25 for the current BMS workspace.

## Quick verdict

- The current BMS script engine is structurally close to classic Odin-style servers.
- The safest source for low-risk NPC/quest reuse is `OpenMS`, because it keeps the classic `cm/qm` model, has broad script coverage, and very little non-ASCII script text.
- `odinms` is the cleanest baseline for understanding original GMS logic and validating how a script was meant to behave.
- `Cosmic` is the best source for cleaner English text and later-era content, but it also uses helper methods that do not exist in the current BMS API, so it is not the best repo for blind copy-paste.
- `OpenMS` is the best donor for scripts, not for the live combat/packet core. Core issues such as ranged attack timing, EXP/meso popup visuals, and suspicious drop behavior should be fixed surgically in the current BMS code.

## What this means in practice

Use `OpenMS` or `odinms` first when a target script:

- is an older/simple NPC or quest
- only uses classic helpers such as `sendNext`, `sendSimple`, `sendYesNo`, `gainItem`, `haveItem`, `warp`, `forceStartQuest`, `forceCompleteQuest`, `canHold`
- belongs to Maple Island, Victoria Island, early towns, or other long-stable content

Use `Cosmic` first when a target script:

- exists in later GMS-era content not covered well by v62 repos
- already has clean English dialogue and better flow
- only needs 1 or 2 easy API rewrites

Do not blindly import from any repo when a script uses:

- custom quest progress helpers
- UI/tutorial helpers not present in the current BMS API
- wedding, family, guild, party quest, or event-specific helper methods
- version-specific story systems that may not match the current client data

## Important findings

- The current BMS already loads scripts with Nashorn and preloads `mozilla_compat`, so legacy Odin/OpenMS-style JS scripts are a good structural fit.
- The biggest current problem is not the script engine. It is the script content:
  - a lot of JP/KR or corrupted text
  - placeholder comments such as `テキスト不足`, `適当`, `原文ママ`
  - a few obviously garbled or suspicious quest custom-data strings
- Some current files are complete enough and can stay as-is. Others are better replaced with GMS-based versions.
- The current gameplay bugs reported after mob combat started working again are not good candidates for bulk repo imports:
  - missing EXP/meso visual popup
  - ranged attacks killing mobs before the projectile visually lands
  - drop behavior that feels too generous even while configured rates are still `1x`

## Recommended migration order

1. Replace clearly broken or placeholder beginner scripts first.
2. Replace simple town/transport/helper NPCs next.
3. Replace corrupted tutorial quests after checking API calls one by one.
4. Leave advanced story/event/wedding scripts for manual porting only.
5. Treat packet/combat/drop bugs as core triage work, separate from script migration.

## Folder map

- `repo-comparison.md`: side-by-side repo comparison
- `current-bms-audit.md`: audit of the current BMS scripts and risks
- `candidate-shortlist.md`: scripts worth pulling first
- `porting-rules.md`: what is safe to copy, what needs adaptation, and what to avoid
- `core-systems-triage.md`: what recent mob/combat/drop findings belong to the core instead of scripts
