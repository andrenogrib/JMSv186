# BMS v24 Movement And NPC Visibility

## Symptom

While walking in Henesys, nearby NPCs would:

- disappear and reappear while the player moved
- sometimes become clickable only after forcing receive-side visibility
- generate repeated server-side `@00C6` packets

Observed examples:

- `@00C6 A1 86 01 00`
- `@00C6 A2 86 01 00`
- `@00C6 AA 86 01 00`

## What `@00C6` Means

In [properties/packet/BMS_v24_ServerPacket.properties](C:/Users/andre/Dropbox/games/ms_server/bms_v024/JMSv186/properties/packet/BMS_v24_ServerPacket.properties), `@00C6` is:

- `LP_NpcLeaveField`

So this was not the client randomly hiding NPCs.
The server was explicitly telling the client to remove them from the field.

## Root Cause

The NPC flicker was caused by the server decoding the BMS v24 movement packet with the wrong move-path layout.

That bad decode caused the server-side player position to drift away from the real client position.
Once the server believed the player had moved out of range, [TacosMap.java](C:/Users/andre/Dropbox/games/ms_server/bms_v024/JMSv186/src/tacos/server/map/TacosMap.java) would send `NpcLeaveField` through its normal visibility logic.

Relevant flow:

1. `CP_UserMove` is handled in [ReqCUser.java](C:/Users/andre/Dropbox/games/ms_server/bms_v024/JMSv186/src/tacos/packet/request/ReqCUser.java)
2. movement bytes are decoded by [ParseCMovePath.java](C:/Users/andre/Dropbox/games/ms_server/bms_v024/JMSv186/src/tacos/packet/request/parse/ParseCMovePath.java)
3. the resulting position is applied to the player
4. [TacosMap.java](C:/Users/andre/Dropbox/games/ms_server/bms_v024/JMSv186/src/tacos/server/map/TacosMap.java) recalculates visible objects
5. if distance is wrong, NPCs are removed with `LP_NpcLeaveField`

## Why This Was Suspected

The strongest clues were:

- `@00C6` was a server packet for NPC removal, not a client packet
- the issue only happened while moving
- the original author had already said: `character movement packet is not coded for bms yet`
- the old local `bms_v8` project contained a native hook note for `CField::OnUserMove` / `CVecCtrlUser::InspectUserMove`, which strongly suggested BMS movement differences are real and known

That old reference did not contain the Java fix directly, but it confirmed the investigation should focus on movement parsing rather than scripts or NPC data.

## The Actual Fix

Two Java-side changes were enough to stabilize NPC visibility:

1. In [ReqCUser.java](C:/Users/andre/Dropbox/games/ms_server/bms_v024/JMSv186/src/tacos/packet/request/ReqCUser.java), treat BMS move packets like the older pre-JMS180 move header layout before entering `ParseCMovePath`.
2. In [ParseCMovePath.java](C:/Users/andre/Dropbox/games/ms_server/bms_v024/JMSv186/src/tacos/packet/request/parse/ParseCMovePath.java), decode BMS end-position offsets using the older pre-JMS180 layout.

## Important Detail

The older logic was not sitting in the code as a commented-out BMS fix.

What already existed was:

- an older move-path branch for `KMS <= 65`, `JMS <= 165`, `GMS <= 83`
- a newer `JMS180+` branch

The fix was recognizing that `BMS v24` belongs with the older branch for movement end-position decoding, even though other parts of the project still treat BMS v24 as closer to later JMS-era content.

## Result

After applying the BMS-specific movement handling:

- NPCs near Henesys stopped flickering while walking
- the repeated `LP_NpcLeaveField` behavior stopped being the dominant symptom
- NPC interaction became stable again

## Follow-Up

This fix addresses the most visible symptom, but it does not prove the entire BMS movement format is fully mapped.

If movement issues remain elsewhere, the next step should be:

- instrumenting `CP_UserMove` decode values for BMS
- comparing parsed start/end/fh/action against client behavior
- then validating remote player movement against the same path data
