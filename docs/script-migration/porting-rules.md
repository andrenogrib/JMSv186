# Porting Rules

## Safe copy rules

A donor script is a good direct candidate when it only uses:

- `start()` and `action(...)` for NPCs
- `start(...)` and `end(...)` for quests
- `sendNext`, `sendNextPrev`, `sendSimple`, `sendYesNo`, `sendOk`
- `haveItem`, `gainItem`, `gainMeso`, `warp`
- `forceStartQuest`, `forceCompleteQuest`
- `canHold`
- basic `getPlayer()` checks

## Small rewrite rules

These are usually easy to port:

- `cm.getJobId()` -> rewrite to `cm.getJob()`
- donor Nashorn bootstrap lines -> optional because the current BMS already preloads `mozilla_compat`
- old enum-based job checks -> replace with numeric job checks if needed

## Medium rewrite rules

These need manual review before importing:

- `qm.showInfo(...)`
- `qm.getPlayer().updateHp(...)`
- scripts that assume newer tutorial/UI effect helpers

Typical handling:

- map the effect to an existing BMS helper
- or remove the cosmetic effect and keep the quest logic

## Red-flag rules

Do not bulk-copy scripts that use:

- `setQuestProgress(...)`
- `getQuestProgressInt(...)`
- `canHoldAll(...)`
- `getNpcObjectId(...)`
- `npcTalk(...)`
- wedding, family, guild, or custom gift APIs
- custom event instance internals

Those scripts are not automatically bad, but they are not "drop into `scripts_BMS` and test once" level safe.

## Import checklist

Before importing a script:

1. Confirm the file id still makes sense for the current client data.
2. Compare the donor helper calls against `src/tacos/odin/OdinNPCConversationManager.java` and `src/tacos/odin/OdinAbstractPlayerInteraction.java`.
3. Remove or adapt unsupported helper methods.
4. Keep the first port small and test only one NPC/quest at a time.
5. Prefer replacing obvious placeholders before touching already-stable scripts.

## Good first-wave targets

- beginner helper NPCs
- taxi and simple transport NPCs
- simple item reward quests
- early tutorial quests after effect-call cleanup

## Bad first-wave targets

- wedding scripts
- multi-party event scripts
- family/guild scripts
- scripts depending on newer quest-progress helper APIs

