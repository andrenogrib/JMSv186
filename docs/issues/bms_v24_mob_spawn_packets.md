# BMS v24 Mob Spawn Packet Notes

## Symptom

- Mobs do not appear in the field
- Mobs do not appear in the minimap
- The client analysis log shows repeated `receive @FFFF ...` packets near Henesys hunting maps

Example payloads captured during the issue:

- `@FFFF 01 A1 86 01 00 01 54 F0 10 00 ...`
- `@FFFF 01 A2 86 01 00 01 F6 76 12 00 ...`
- `@FFFF 01 A3 86 01 00 01 54 F0 10 00 ...`

## Root Cause

The BMS v24 server packet properties were missing the `CMobPool` opcode family.

That meant the Java server was building mob packets with unresolved headers, which the packet loader turns into `@FFFF`.

Relevant files:

- [`properties/packet/BMS_v24_ServerPacket.properties`](/C:/Users/andre/Dropbox/games/ms_server/bms_v024/JMSv186/properties/packet/BMS_v24_ServerPacket.properties)
- [`src/tacos/property/Property_Packet.java`](/C:/Users/andre/Dropbox/games/ms_server/bms_v024/JMSv186/src/tacos/property/Property_Packet.java)

## Why `@FFFF` Was The Key Clue

The mob payloads looked valid even though the header was invalid:

- `A1 86 01 00` = object id `100001`
- `54 F0 10 00` = mob id `1110100`
- `F6 76 12 00` = mob id `1210102`

Those mob ids exist in the local mob strings:

- `1110100` = `Cogumelo Verde`
- `1210102` = `Cogumelo Laranja`

So the server was not failing to spawn mobs logically. It was sending mob packets with an invalid header.

## IDB Evidence

Client-side packet routing already showed that:

- `0xB3` to `0xC4` routes into `CMobPool::OnPacket`
- `0xC5` to `0xCC` routes into `CNpcPool::OnPacket`

The decoded `CMobPool::OnPacket` dispatch further showed:

- `0xB3` = mob pool packet
- `0xB4` = mob pool packet
- `0xB5` = mob pool packet
- `0xB6` to `0xC3` = mob packet family

That aligns with the BMS v24 NPC opcodes already present:

- `LP_NpcEnterField = @00C5`
- `LP_NpcLeaveField = @00C6`
- `LP_NpcChangeController = @00C7`

## Fix Applied

The following BMS v24 server packet opcodes were defined:

- `LP_MobEnterField = @00B3`
- `LP_MobLeaveField = @00B4`
- `LP_MobChangeController = @00B5`
- `LP_MobMove = @00B6`
- `LP_MobCtrlAck = @00B7`
- `LP_MobCtrlHint = @00B8`
- `LP_MobStatSet = @00B9`
- `LP_MobStatReset = @00BA`
- `LP_MobSuspendReset = @00BB`
- `LP_MobAffected = @00BC`
- `LP_MobDamaged = @00BD`
- `LP_MobSpecialEffectBySkill = @00BE`
- `LP_MobCrcKeyChanged = @00C0`
- `LP_MobHPIndicator = @00C1`

## Scope

This fix targets the mob packet family that the Java server already emits today:

- spawn
- leave
- controller change
- movement ack
- status set/reset
- damage
- hp indicator

It does not claim that every later mob-related enum in the Java code is already confirmed for BMS v24.
