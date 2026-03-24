# IDB Research

This folder is the documentation home for the BMS v24 reverse-engineering work.

## Principles

- Separate what is **confirmed by client/server log** from what is **extracted from the IDB**
- Keep raw generated material under `generated/`
- Keep curated conclusions in human-written Markdown files here
- Treat opcode names as tentative until they are backed by either:
  - a working handler match in the client/server
  - repeated log evidence
  - or a clear dispatch/disassembly trail in the IDB

## Current files

- `bms_v24_research.md`
  - current curated summary
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
