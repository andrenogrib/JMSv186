# Issue Notes

This folder is for focused write-ups of concrete bugs, regressions and fixes.

## Current Files

- `bms_v24_movement_npc_notes.md`
  - root cause and fix notes for the BMS v24 movement decode issue that caused NPC flicker and repeated `LP_NpcLeaveField`
- `bms_v24_mob_spawn_packets.md`
  - root cause and fix notes for the BMS v24 mob invisibility issue caused by unresolved `CMobPool` packet headers
- `bms_v24_mob_runtime_notes.md`
  - current runtime state after the spawn/DC fixes, including the new `@00A1` and combat packet blockers
- `bms_v24_combat_drop_followup.md`
  - current state of the pickup popup fix, the partial ranged-delay fix, and the BMS-specific drop-formula adjustment

## Related Sources

- `../idb/bms_v24_research.md`
  - higher-level reverse-engineering summary
- `../packets/bms_v24_clientpacket_diff.md`
  - packet mapping notes that may interact with runtime behavior
