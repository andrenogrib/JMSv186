# BMS v24 Combat / Drop Follow-Up

This note tracks the current server-side state after the BMS v24 pickup, ranged, and Monster Book fixes.

## Current Status

### 1. Pickup popup

Status:

- fixed

What changed:

- `properties/packet/BMS_v24_ServerPacket.properties` now maps the missing headers that were still resolving to `@FFFF`
- that restored:
  - item pickup popup
  - meso pickup popup
  - EXP / message-style popup paths used by the client

Relevant file:

- `properties/packet/BMS_v24_ServerPacket.properties`

### 2. Monster Book / Monster Card

Status:

- hard-disabled for BMS v24
- latest logs no longer show the old crash packet path

Why it was disabled:

- BMS v24 disconnects when it receives the later Monster Book pickup/update flow used by newer JMS-family clients
- the old bad sequence was:
  - `LP_MonsterBookSetCard`
  - `LP_Message` for card gain
  - `LP_UserEffectLocal` / card-gain effect

What the latest logs show:

- session `logs/PacketTrace_20260325_111335.log` contains no `LP_MonsterBookSetCard`
- the matching server log `logs/Server_BMS_24_0_20260325_111335.log` ends with a normal `sessionClosed`, not a Java-side crash

Code-level changes:

- `src/tacos/config/ServerConfig.java`
  - `MonsterBookSupported()` returns `false` for `Region.IsBMS() && Version.getVersion() <= 24`
  - this is now the single feature gate for BMS v24 Monster Book support
- `src/tacos/server/map/MonsterDrop.java`
  - normal DB drop generation skips Monster Card entries entirely when `MonsterBookSupported()` is false
  - that prevents mob kills from producing pickup-crash cards
- `src/tacos/unofficial/CustomMonsterBookDrop.java`
  - the custom fallback Monster Book reward path now returns immediately when the feature gate is off
  - this avoids reintroducing card drops outside the normal DB drop flow
- `src/odin/server/MapleStatEffect.java`
  - item-use logic only calls `applyto.getMonsterBook().addCard(...)` when Monster Book is supported
  - manual use of Monster Card items no longer enters the add-card packet/effect flow on BMS v24
- `src/odin/client/MonsterBook.java`
  - `updateCard(...)` now returns immediately when Monster Book is unsupported
  - `addCard(...)` now returns immediately when Monster Book is unsupported
  - this blocks both cover-change packets and add-card packets/effects on BMS v24
- `src/odin/handling/channel/handler/PlayerHandler.java`
  - `ChangeMonsterBookCover(...)` now ignores the request entirely while the feature is disabled

Net effect:

- BMS v24 no longer drops Monster Cards
- BMS v24 no longer tries to update Monster Book state from item use
- BMS v24 no longer sends the cover-change/update flow that used to lead into the disconnect path

### 3. Ranged timing

Status:

- improved, but still heuristic
- Triple Throw / multi-projectile sync still needs one more pass

What changed:

- ranged damage is not applied fully immediate on receipt
- request parsing now keeps the earliest positive `tDelay` from the shot targets
- the server resolves ranged damage from that first impact marker with a forward offset and a cap
- delayed hits are cancelled if the player is no longer alive or already changed map

Relevant files:

- `src/tacos/packet/request/ReqCUser.java`
- `src/odin/handling/channel/handler/PlayerHandler.java`

What the latest logs show:

- in `logs/PacketTrace_20260325_111335.log`, the ranged kill pattern is still:
  - `CP_UserShootAttack`
  - `LP_MobHPIndicator`
  - `LP_Message`
  - `LP_MobLeaveField`
  - `LP_DropEnterField`
- examples:
  - lines `5984 -> 6007`
  - lines `6479 -> 6527`
  - lines `6594 -> 6640`
  - lines `6685 -> 6732`
- the important part is that kill + drop still arrive as one tight block after the delayed ranged damage resolves

Interpretation:

- the latest logs do not show a Monster Book packet problem
- the remaining visual mismatch is in ranged sync itself
- the reported early `MISS` on Triple Throw is not explained by a Monster Book flow
- OpenMS applies ranged damage immediately and also drops immediately after kill, so its stock flow is not a direct fit for BMS v24
- for BMS v24 we still need a client-specific sync solution, likely around projectile-impact timing rather than general drop logic

Most likely remaining causes:

- the current generic ranged delay rule is still not skill-accurate for Triple Throw
- BMS v24 may need per-skill or per-weapon timing offsets instead of one generic ranged heuristic
- the client may be showing a local placeholder / validation miss before the real projectile impact reaches the mob

Recommended next debug step:

1. capture one clean Triple Throw packet trace with only one target on screen
2. log `attack.skill`, `attack.nAttackSpeed`, `attack.tAttackTime`, `attack.nHitDelay`
3. compare:
   - attack send time
   - mob leave time
   - when the projectile visually reaches the mob
4. if needed, tune BMS ranged delay per skill family instead of using only the current generic rule

### 4. Death / drop timing

Status:

- improved again for BMS v24
- still tied to the ranged sync work above
- latest disconnect logs point to one more drop packet compatibility issue that is now fixed in code

What changed:

- `src/odin/server/maps/MapleMap.java` now gives the BMS v24 kill animation a brief head start before entering the drop
- this delay is BMS-only and only applies when the mob uses a non-zero death animation
- the current BMS-only head-start is `220ms`

Why this was added:

- once delayed ranged damage resolves, the stock flow still does:
  - mob death
  - drop enter
- on BMS v24 that makes the drop feel too close to the death sprite, especially on projectile kills

Latest packet issue found from live logs:

- in `logs/PacketTrace_20260325_114351.log`, the client disconnected right after tight `mob leave -> drop enter` sequences
- the strongest mismatch was in `LP_DropEnterField` for mob drops:
  - the packet field `dwSourceID` was being filled with the monster runtime object id
  - BMS v24 expects the monster template id (`mob.getId()`) there
- example bad packets before the disconnect included source values like `A6 86 01 00` and `A1 86 01 00`, which are map object ids, not monster ids

Code fix applied:

- `src/odin/server/maps/MapleMap.java`
  - `spawnMobDrop(...)` now sends `mob.getId()` into `ResCDropPool.DropEnterField(...)`
  - before this fix it was sending `mob.getObjectId()`

Second live issue found after that fix:

- in `logs/PacketTrace_20260325_115124.log`, the disconnect no longer matched the old wrong-source-id pattern
- instead, the trace showed duplicate drop object ids being reused in the same burst
- example:
  - three different `LP_DropEnterField` packets reused the same drop object id `1A 87 01 00`
  - see the block around line `4174`

Root cause:

- `src/tacos/server/map/TacosMap.java`
  - map object ids were generated from a plain `int runningOid`
  - `addMapObject(...)` incremented that field without synchronization
  - map object insertion/removal also happened against `LinkedHashMap` instances without taking the existing per-type map locks
- under concurrent mob death / delayed drop scheduling, that allowed duplicated object ids and unsafe writes into the map object pool

Code fix applied:

- `src/tacos/server/map/TacosMap.java`
  - `runningOid` now uses `AtomicInteger`
  - `addMapObject(...)` now uses `incrementAndGet()` under the per-type write lock
  - `removeMapObject(...)` now uses the per-type write lock
  - `getMapObject(...)`, `getMapObjects(...)`, and both `getMapObjectsInRange(...)` paths now snapshot/read under the matching read lock

Why this matters:

- duplicate `drop.getObjectId()` values are fatal for client-side object tracking
- once two live drops share the same id, later enter/leave/pickup state becomes ambiguous and can disconnect the client

Why this matters:

- the server log for that session only showed normal `sessionClosed`, not a Java exception
- that strongly suggests a client-side disconnect caused by malformed or incompatible packet contents
- this fix targets the most suspicious field in the death/drop path without changing the broader drop timing logic

OpenMS comparison:

- OpenMS also enters drops immediately after `killMonster(...)`
- so the immediate death-to-drop sequence is normal in the base server flow
- the BMS-only delay is a compatibility polish layer on top of that base flow

Third live issue found after both fixes:

- in `logs/PacketTrace_20260325_115819.log`, another disconnect still happened during a multi-kill burst
- the drop object ids were now unique, so the previous duplicate-oid bug was no longer the active failure
- however, the burst still contained a mixed sequence of:
  - item drops with `dwSourceID = mob.getId()`
  - meso drops still entering with `dwSourceID = 0`

Final compatibility fix applied:

- `src/odin/server/maps/MapleMap.java`
  - `spawnMobMesoDrop(...)` is now overridden so monster meso drops also send the monster template id in `dwSourceID`
  - BMS mob drops now use a short burst-aware stagger (`35ms` steps, capped at `210ms`) so several drops from the same multi-kill are not all entered in the same millisecond

Why this matters:

- for BMS v24, the `dwSourceID` expectation appears to apply to monster meso drops too, not only item drops
- the extra burst pacing reduces client-side pressure in the exact scenario where the user was still reproducing disconnects: one skill killing multiple mobs in the same frame

Fourth live issue found after the packet-field and oid fixes:

- in `logs/PacketTrace_20260325_120843.log`, a multi-kill still disconnected the client
- the final burst no longer showed duplicate drop oids or zeroed mob source ids
- however, the same second still contained:
  - `LP_MobLeaveField` for the killed pack
  - immediate regular `LP_MobEnterField` respawns (`E2`..`EF`)
  - then the full `LP_DropEnterField` burst (`F0`..`F9`)

Final compatibility fix applied for that pattern:

- `src/odin/server/maps/MapleMap.java`
  - BMS now places a short respawn hold (`1800ms`) after a kill that produces drops
  - regular `respawn(false)` calls are skipped during that hold window

Why this matters:

- the remaining crash pattern was no longer about malformed individual drop packets
- it was about mixing a death/drop burst with fresh regular respawns in the same visual window
- BMS v24 appears to be more sensitive to that overlap than the older Odin/OpenMS timing model

Latest follow-up from `logs/PacketTrace_20260325_121819.log` / `logs/Server_BMS_24_0_20260325_121819.log`:

- the respawn overlap improved after the hold window change
- the disconnect still happened, but the final server burst was now mostly:
  - kill acknowledgements / mob leave
  - then a dense `LP_DropEnterField` run (`DC`..`E9`)
- this narrowed the remaining instability to drop burst timing rather than respawn overlap

Additional timing adjustment applied:

- `src/odin/server/maps/MapleMap.java`
  - BMS death animation head start increased from `220ms` to `420ms`
  - BMS drop burst reset window increased from `150ms` to `350ms`
  - BMS drop burst spacing increased from `35ms` to `90ms`
  - BMS drop burst cap increased from `210ms` to `1350ms`

Why this matters:

- the previous cap caused large multi-kill bursts to collapse back into the same send window
- the new timing keeps the same packet format but spreads the visual drop burst over a safer interval for BMS v24

### 5. Drop formula

Status:

- formula adjusted
- user feedback is positive so far

What changed:

- BMS no longer inherits the old GMS/SEA equip-chance x10 behavior
- BMS bosses no longer force-pass every drop entry
- BMS boss drops now use normal chance flow with a smaller bonus instead of unconditional drop behavior
- BMS meso no longer gets additionally inflated by `dropMod`

Relevant files:

- `src/odin/server/life/MapleMonsterInformationProvider.java`
- `src/tacos/server/map/MonsterDrop.java`

### 6. Global rates

Global world rates currently come from:

- `properties/kaede.properties`

Keys:

- `server.rate.exp`
- `server.rate.meso`
- `server.rate.drop`

These values are loaded by:

- `src/tacos/property/Property_World.java`
- then exposed per channel by `src/tacos/server/TacosChannel.java`

Changing the property values requires a server restart.

### 7. Movement crash note

Observed in runtime logs:

- `ArrayIndexOutOfBoundsException` in `tacos.server.map.TacosMap.movePlayer`

Mitigation applied:

- `visibleMapObjects` now uses a concurrent set implementation to avoid unstable snapshot conversion while the set is changing during movement visibility updates

Relevant file:

- `src/odin/client/MapleCharacter.java`

## Short Conclusion

Right now the server-side state is:

- pickup popup: working
- Monster Book / Monster Card on BMS v24: intentionally disabled and no longer entering the old crash flow
- ranged timing: better, but Triple Throw still needs a BMS-specific sync pass
- death / drop timing: now delayed slightly on BMS v24 so the drop does not sit as tightly on top of the death packet
- drop formula: materially improved and already feeling more natural in live play
