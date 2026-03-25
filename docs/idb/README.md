# IDB Research

This folder is the documentation home for the BMS v24 reverse-engineering work.

## Principles

- Separate what is **confirmed by client/server log** from what is **extracted from the IDB**
- Keep raw generated material under `generated/`
- Keep curated conclusions in human-written Markdown files here or in related folders under `docs/`
- Treat opcode names as tentative until they are backed by either:
  - a working handler match in the client/server
  - repeated log evidence
  - or a clear dispatch/disassembly trail in the IDB

## Current Files

- `bms_v24_research.md`
  - current curated summary
- `bms_v8_extension_notes.md`
  - notes on what the old C++/TSQL `bms_v8` extension is useful for as BMS-specific reference
- `idb_inventory.md`
  - generated inventory of the local IDB corpus
- `generated/BMS_WvsGame_user_packet_switch.md`
  - extracted switch map for `CUser::OnPacket` in the original game server IDB
- `generated/BMS_WvsGame_focus.md`
  - quick index of useful packet-related functions in `BMS_WvsGame.idb`
- `generated/BMS_v24.0_U_DEVM_dispatch.md`
  - raw disassembly walk for named client packet routers
- `generated/`
  - machine-generated extracts from `tools/idb`

## Related Docs Outside This Folder

- `../packets/bms_v24_clientpacket_diff.md`
  - packet mapping comparison for the current Java server
- `../issues/bms_v24_movement_npc_notes.md`
  - movement decode issue that caused NPC flicker and `LP_NpcLeaveField` spam
- `../tools/README.md`
  - tool workflow overview for IDB extraction and RirePE helpers
