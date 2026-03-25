# Repo Comparison

## Snapshot

| Repo | Version bias | NPC scripts | Quest scripts | Script files with non-ASCII text | Engine fit with current BMS | Best use | Main risk |
|---|---:|---:|---:|---:|---|---|---|
| Current BMS | Current project | 659 | 184 | 225 | Native | Keep working scripts, replace broken ones selectively | Mixed language, placeholders, corrupted strings |
| `odinms` | v62 GMS | 369 | 149 | 18 | Very high | Original logic reference, simple legacy ports | Older coverage, smaller script set |
| `OpenMS` | v62 GMS | 841 | 445 | 2 | Very high | Best low-risk donor for classic NPC/quest ports | Some scripts use older object/job checks that still need tiny rewrites |
| `Cosmic` | v83 GMS | 708 | 253 | 14 | Medium to high | Cleaner English content, better text, later-era references | Uses helpers absent from the current BMS API |

## Current BMS engine notes

The current workspace uses:

- `src/tacos/script/TacosScript.java`
- `src/tacos/script/TacosScriptNPC.java`
- `src/tacos/script/TacosScriptQuest.java`
- `src/tacos/odin/OdinNPCConversationManager.java`

Important observations:

- Scripts are loaded through Nashorn.
- The engine explicitly runs `load('nashorn:mozilla_compat.js');` before evaluating script files.
- NPC scripts use classic `cm` access and `start()/action(...)`.
- Quest scripts use classic `qm` access and `start(mode, type, selection)/end(...)`.

That is why `odinms` and `OpenMS` are such a good fit structurally.

## Compatibility by repo

## `odinms`

Strengths:

- Very close to the classic script model used by the current BMS.
- Good for validating the original intended flow of basic NPCs and quests.
- Easy to reason about because the script layer is minimal and direct.

Weaknesses:

- Smaller script library than `OpenMS`.
- Aged content coverage.
- Some scripts still include legacy Nashorn boilerplate and package imports.

Best use:

- Logic reference
- Beginner scripts
- Simple town, taxi, helper, shop, and starter quest flows

## `OpenMS`

Strengths:

- Largest overall script pool among the studied donor repos.
- Very low non-ASCII incidence in scripts.
- Stays close to classic Odin-style `cm/qm` interaction.

Weaknesses:

- Some scripts assume older Java-side types or enums in job checks.
- Still tied to v62-era content coverage.

Best use:

- First donor for direct or near-direct NPC/quest reuse
- Replacing placeholder beginner/helper scripts
- Replacing simple town service NPCs

## `Cosmic`

Strengths:

- Cleaner English dialogue and better script polish.
- Better for later-era content than v62 repos.
- Includes useful base templates for NPC and quest scripts.

Weaknesses:

- Uses helpers not currently exposed by the BMS scripting API.
- Examples found in scripts include `showInfo`, `getQuestProgressInt`, `setQuestProgress`, `canHoldAll`, `getJobId()`, and other richer helpers.
- Safer as a content donor than as a blind copy donor.

Best use:

- English text donor
- Flow donor for scripts already close to current BMS content
- Later-era content where v62 repos have nothing useful

## Practical recommendation

If the goal is "pull scripts without bugging the client":

1. Start from `OpenMS`.
2. Cross-check with `odinms` when you want the original/simple version.
3. Borrow text and later-content flow from `Cosmic` only after checking unsupported helpers.

