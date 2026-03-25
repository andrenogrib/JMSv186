# BMS v24 Combat / Drop Follow-Up

This note tracks the current server-side state after the first BMS v24 combat and pickup fixes.

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

Relevant files:

- `properties/packet/BMS_v24_ServerPacket.properties`

### 2. Ranged timing

Status:

- improved, but not fully solved

What changed:

- ranged damage is no longer applied fully immediate on receipt
- request parsing now keeps the earliest positive `tDelay` from the shot targets
- the server resolves ranged damage with a reduced delay window:
  - first-hit `tDelay`
  - minus a small network cushion
  - capped so stale shots do not linger too long
- delayed hits are also cancelled if the player is no longer alive or already changed map

Relevant files:

- `src/tacos/packet/request/ReqCUser.java`
- `src/odin/handling/channel/handler/PlayerHandler.java`

Remaining issue:

- the user still reports cases where the local client appears to keep shooting into a mob that is already dead

Interpretation:

- the current change improves kill timing
- but the BMS v24 ranged sync is still not perfectly matched
- the remaining gap is likely in one of these areas:
  - exact meaning of per-target `tDelay`
  - whether BMS needs a skill-specific ranged timing table instead of one generic rule
  - attack packet broadcast timing versus mob death timing
  - local-client prediction continuing briefly before the death packet arrives

Recommended next debug step:

1. capture packet traces for one simple single-target bow attack and one star attack
2. log `attack.skill`, `attack.nAttackSpeed`, `attack.tAttackTime`, `attack.nHitDelay`
3. compare:
   - attack send time
   - mob death send time
   - client visual impact timing
4. if needed, move from the generic heuristic to:
   - per-skill timing offsets, or
   - a different source field for ranged impact timing

### 3. Drop formula

Status:

- formula adjusted
- live validation still needed

What changed:

- BMS no longer inherits the old GMS/SEA equip-chance x10 behavior
- BMS bosses no longer force-pass every drop entry
- BMS boss drops now use normal chance flow with a smaller bonus instead of unconditional drop behavior
- BMS meso no longer gets additionally inflated by `dropMod`

Relevant files:

- `src/odin/server/life/MapleMonsterInformationProvider.java`
- `src/tacos/server/map/MonsterDrop.java`

What still needs checking ingame:

1. normal mob common drops
2. boss drop quantity
3. equip frequency
4. meso amount per kill
5. whether rare drops still feel reachable at `server.rate.drop = 1`

## Git / Workspace Notes

This workspace currently has a lot of documentation and tooling churn in addition to the runtime fixes.

To avoid noisy local junk coming back into `git status`, `.gitignore` was extended for:

- `tmp_compile_lib/`
- temporary local compile output folders at repo root:
  - `odin/`
  - `tacos/`
- local packet-property backup snapshots:
  - `backup/20260324_serverpacket_before_mob_sync/`
  - `backup/20260324_serverpacket_before_userpool_sync/`
- local probe logs:
  - `tmp_client_probe.log`
  - `tmp_client_probe.err`

## Short Conclusion

Right now the server-side state is:

- pickup popup: working
- ranged timing: materially better, still needs one more sync pass
- drop formula: corrected on the server side, still needs gameplay validation
