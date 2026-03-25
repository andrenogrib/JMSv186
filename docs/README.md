# Project Docs

This folder is the main documentation home for the project.

The goal is to keep documentation organized by area:

- `idb/`
  - reverse-engineering notes, generated extracts, IDB inventory
- `packets/`
  - packet mapping diffs, opcode notes, protocol comparisons
- `issues/`
  - focused write-ups for concrete bugs and fixes
- `tools/`
  - local tooling notes, reverse-engineering workflow, helper indexes

## Current Index

- `idb/README.md`
  - index for the current BMS v24 IDB research set
- `packets/README.md`
  - packet and opcode investigation index
- `issues/README.md`
  - focused bug and fix notes
- `idb/bms_v24_research.md`
  - curated BMS v24 reverse-engineering summary
- `idb/bms_v8_extension_notes.md`
  - what the older `bms_v8` C++/TSQL extension can still teach us about BMS-specific behavior
- `idb/idb_inventory.md`
  - generated inventory of the local IDB corpus
- `packets/bms_v24_clientpacket_diff.md`
  - comparison between current Java `ClientPacket` mapping and original BMS intent
- `issues/bms_v24_movement_npc_notes.md`
  - root cause and fix notes for the BMS v24 movement decode issue that caused NPC flicker
- `issues/bms_v24_mob_runtime_notes.md`
  - current runtime state after mobs started spawning without disconnecting
- `tools/README.md`
  - tool workflow overview, including IDB and RirePE-related notes

## Source Layout

- `idb_client/idb/`
  - raw client and server IDBs
- `docs/idb/generated/`
  - machine-generated extracts produced by `tools/idb`
- `tools/`
  - scripts, submodules and local reverse-engineering helpers

## Working Rule

Keep raw/generated material separate from curated conclusions:

- generated evidence stays under `docs/idb/generated/`
- human-readable conclusions stay in the area-based folders here
