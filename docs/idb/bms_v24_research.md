# BMS v24 Research Notes

## Confirmed By Client Log

The following items are confirmed from the user-provided server log on 2026-03-24:

- Unknown client packet `@00C4` was observed
- Unknown client packet `@005F` was observed with payload `DD EB B8 00 01 00`
- Unknown client packet `@0056` was observed repeatedly
- Repeating `@0056` payload variant A:
  - `00 14 00 00 46 00 00 00 00`
- Repeating `@0056` payload variant B:
  - `00 14 00 00 00 00 17 00 00`

Current server-side packet mapping gaps:

- `properties/packet/BMS_v24_ClientPacket.properties` does not currently define `@0056`
- `properties/packet/BMS_v24_ClientPacket.properties` does not currently define `@005F`
- `properties/packet/BMS_v24_ClientPacket.properties` does not currently define `@00C4`

## Extracted From IDB

The main client IDB already exposes named packet-related functions:

- `CClientSocket::SendPacket`
- `CClientSocket::ProcessPacket`
- `CLogin::OnPacket`
- `CField::OnPacket`
- `CUserPool::OnPacket`
- `CUserPool::OnUserCommonPacket`
- `CUserPool::OnUserRemotePacket`
- `CUserPool::OnUserLocalPacket`
- `CMobPool::OnPacket`
- `CNpcPool::OnPacket`
- `CWvsContext::OnPacket`

These names are a strong base for:

- locating client-side packet dispatch
- mapping packet handler groups by system
- comparing client packet routing against the server enums and `.properties` files

Generated extracts live in:

- `generated/BMS_v24.0_U_DEVM_names.md`
- `generated/BMS_v24.0_U_DEVM_dispatch.md`
- `generated/BMS_WvsGame_focus.md`
- `generated/BMS_WvsGame_user_packet_switch.md`
- `generated/BMS_WvsLogin_focus.md`

## What Each IDB Is Good For

Use the local IDBs in different roles:

- `BMS_v24.0_U_DEVM.idb`
  - best for client receive-side packet routing
  - best for field render flow, pool handlers, UI handlers, stage transitions
- `BMS_srv/BMS_WvsGame.idb`
  - best for client to server packet intent
  - best for resolving `UNKNOWN` packets printed by the Java server
  - best for matching opcodes to `CUser::*Request` handlers
- `BMS_srv/BMS_WvsLogin.idb`
  - best for login and world-select flow
  - useful later when confirming account, character and migration behavior

For the current `UNKNOWN` packets from the Java server, `BMS_WvsGame.idb` is the priority source.

## High-Confidence Opcode Findings From WvsGame IDB

The `BMS_WvsGame.idb` server binary contains `CClientSocket::ProcessUserPacket` and `CUser::OnPacket`.

From the decoded `CUser::OnPacket` switch:

- `0x56` routes to `CUser::OnShopScannerItemUseRequest`
- `0x5F` routes to `CUser::OnAntiMacroItemRequest`
- `0xC4` does **not** fall inside the primary `CUser::OnPacket` compressed switch

This does not yet prove the Java server should use those exact names, but it is strong evidence for the intended behavior in the original server line.

## Resolved: NPC Flicker While Moving

The Henesys NPC flicker issue was traced to movement decoding, not to NPC scripts or missing NPC data.

Confirmed behavior:

- repeated `@00C6` during movement meant the server was sending `LP_NpcLeaveField`
- this only happened while the player moved near NPCs
- the player position used for visibility checks was being decoded incorrectly for BMS v24

The final fix was:

- handle BMS move headers like the older pre-JMS180 branch in `ReqCUser::OnUserMove`
- decode BMS move end-position offsets with the older layout in `ParseCMovePath`

Detailed notes:

- `../issues/bms_v24_movement_npc_notes.md`

## Client Field Packet Families

The client-side `CField::OnPacket` routing in `BMS_v24.0_U_DEVM.idb` is useful for map, mob and NPC rendering issues.

Important ranges already visible in the client dispatch:

- `0x7A` to `0xB2` routes into `CUserPool::OnPacket`
- `0xB3` to `0xC4` routes into `CMobPool::OnPacket`
- `0xC5` to `0xCC` routes into `CNpcPool::OnPacket`
- `0xCD` to `0xCF` routes into `CEmployeePool::OnPacket`
- `0xD0` to `0xD1` routes into `CDropPool::OnPacket`
- `0xD2` to `0xD4` routes into `CMessageBoxPool::OnPacket`
- `0xD5` to `0xD6` routes into `CAffectedAreaPool::OnPacket`
- `0xD7` to `0xD8` routes into `CTownPortalPool::OnPacket`
- `0xD9` to `0xDC` routes into `CReactorPool::OnPacket`

This is especially relevant for the "mobs are not visible" issue, because it shows that mob appearance on the client depends on the server sending the correct `MobPool` family packets, not only on the map data existing.

## Resolved: Mob Packets Were Going Out As `@FFFF`

The mob invisibility issue was traced to missing BMS v24 `ServerPacket` mappings for the `CMobPool` family.

Confirmed behavior:

- the Java server was building `CMobPool` packets through `ResCMobPool`
- `BMS_v24_ServerPacket.properties` had no opcode values for the main `LP_Mob*` entries
- missing packet properties fall back to `@FFFF`
- client-side IDB routing already showed that mob packets belong in the `0xB3` to `0xC4` range

The applied fix mapped the main BMS v24 mob packet family beginning at:

- `LP_MobEnterField = @00B3`
- `LP_MobLeaveField = @00B4`
- `LP_MobChangeController = @00B5`
- `LP_MobMove = @00B6`

Detailed notes:

- `../issues/bms_v24_mob_spawn_packets.md`

## Map And Mob Logic

The IDB is useful for:

- mob pool packet formats
- controller changes
- field enter/leave behavior
- render/update packet flow

The IDB is **not** the source of truth for which mobs belong to which map.

That comes from the map data:

- map XML/WZ `life` entries
- server map loading
- server spawn point and respawn logic

For this project, mob investigation should stay split into:

- packet/protocol validation via IDB
- spawn/data validation via map XML and server code

In practice, the mob problem can come from either side:

- the map XML loads no `life` entries or no valid monster spawn points
- the server loads spawns but sends wrong or incomplete `MobPool` packets
- the client expects a slightly different `MobPool` opcode family than the Java server currently uses

## Recommended Investigation Order

1. Document the full `CUser::OnPacket` switch from `BMS_WvsGame.idb`
2. Resolve the repeating `@0056` packet using the extracted switch map
3. Resolve the one-shot `@005F` packet using the extracted switch map
4. Find the handler path for `@00C4`, which is outside the primary `CUser::OnPacket` switch
5. Compare client `CField`/`CMobPool`/`CNpcPool` routing with the Java server packet enums
6. Pick a single map as the baseline case for "mobs do not appear"
7. Audit `MapleMapFactory` plus the chosen map XML `life` entries against actual spawn behavior

## Next Useful Sources

Local IDBs already available and likely useful:

- `idb_client/idb/BMS_v24.0_U_DEVM.idb`
- `idb_client/idb/BMS_srv/BMS_WvsGame.idb`
- `idb_client/idb/BMS_srv/BMS_WvsLogin.idb`
- `idb_client/idb/BMS_srv/BMS_WvsShop.idb`

For client to server `UNKNOWN` packets, `BMS_WvsGame.idb` should lead.
For field rendering, mobs, NPCs and pool behavior, `BMS_v24.0_U_DEVM.idb` should lead.
