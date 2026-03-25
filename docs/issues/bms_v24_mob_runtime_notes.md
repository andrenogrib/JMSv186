# BMS v24 Mob Runtime Notes

## Current State

- mobs now enter the map
- the client no longer disconnects on map enter
- mob spawn/control packets are reaching the client with valid headers
- mobs still do not behave correctly yet:
  - they stay still
  - attacking them does not do anything yet

## What Changed

This was the sequence that moved the issue forward:

1. `CMobPool` server packet headers were mapped for BMS v24.
2. `MobEnterField` / `MobChangeController` were aligned to the client-side BMS decode path.
3. An extra trailing `Decode4()` expected by the BMS client was added to both packets.

That changed the runtime from:

- `@FFFF` mob packets
- invisible mobs
- disconnect on map enter

to:

- `@00B3` / `@00B5` mob packets
- visible mob spawn traffic
- stable map entry

## Confirmed By Runtime Log

Example server-side trace after the fix:

- `@00B3 ...` for `LP_MobEnterField`
- `@00B5 ...` for `LP_MobChangeController`

Example debug lines:

- `[BMS][MobEnterField] mobId=1210102 oid=100001 ...`
- `[BMS][MobChangeController] mobId=1210102 oid=100001 ...`

This confirms that the Java server is now spawning real mobs with valid object ids and mob ids.

## New Blocking Signals

After mobs started entering correctly, the next missing client-to-server packets became visible:

- `@00A1 ...`
  - strong runtime evidence that this is the BMS mob movement/control packet family
  - it starts with the mob object id and appears exactly when the field starts simulating mobs
- `@002C ...`
  - strong runtime evidence that this is one of the player attack packets for BMS
  - it appears when the player attacks
- `@002F ...`
  - likely another combat-related user packet in the same area

These packets are currently not mapped in:

- [BMS_v24_ClientPacket.properties](/C:/Users/andre/Dropbox/games/ms_server/bms_v024/JMSv186/properties/packet/BMS_v24_ClientPacket.properties)

## Practical Meaning

The problem is no longer:

- map XML
- mob spawn logic
- unresolved mob server headers
- immediate crash on map enter

The problem is now mainly:

- BMS `client -> server` mob packet mapping
- BMS `client -> server` attack packet mapping

## Next Targets

- identify and map the BMS opcode used for `CP_MobMove`
- identify and map the BMS opcode used for the user attack packet family
- once those are mapped, validate:
  - mob movement
  - mob reaction to attacks
  - damage application
