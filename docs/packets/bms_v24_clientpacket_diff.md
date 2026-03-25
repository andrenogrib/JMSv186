# BMS v24 ClientPacket Diff

This note compares the current Java packet mapping against the original BMS packet intent recovered from:

- `idb_client/idb/BMS_srv/BMS_WvsGame.idb`
- `../idb/generated/BMS_WvsGame_user_packet_switch.md`

Scope of this diff:

- only `client -> server` user packets
- only mappings with direct name matches or very strong semantic matches
- no movement-logic rewrite yet

## Backup

Backup created before edits:

- `backup/20260324_clientpacket_before_sync/BMS_v24_ClientPacket.properties`

## Applied High-Confidence Changes

| Java packet | Current | BMS real | Evidence |
| --- | --- | --- | --- |
| `CP_UserTrunkRequest` | `@003D` | `@0020` | `OnTrunkRequest@CUser` |
| `CP_UserScriptMessageAnswer` | `@003B` | `@0021` | `OnScriptMessageAnswer@CUser` |
| `CP_UserShopRequest` | `@003C` | `@0022` | `OnShopRequest@CUser` |
| `CP_UserSelectNpc` | `@0039` | `@0023` | `OnSelectNpc@CUser` |
| `CP_UserTransferChannelRequest` | `@0026` | `@0027` | `OnTransferChannelRequest@CUser` |
| `CP_UserMigrateToCashShopRequest` | `@0027` | `@0028` | `OnMigrateToCashShopRequest@CUser` |
| `CP_UserChat` | `@0030` | `@002C` | `OnChat@CUser` |
| `CP_UserTransferFieldRequest` | `@0025` | `@002F` | `OnTransferFieldRequest@CUser` |
| `CP_UserMove` | `@0028` | `@0035` | `OnMove@CUser` |
| `CP_UserPortalScriptRequest` | `@0061` | `@0047` | `OnPortalScriptRequest@CUser` |
| `CP_UserSkillPrepareRequest` | `@005A` | `@0048` | `OnSkillPrepareRequest@CUSkill` |
| `CP_UserSkillUpRequest` | `@0057` | `@004D` | `OnSkillUpRequest@CUSkill` |
| `CP_UserSkillCancelRequest` | `@0059` | `@004E` | `OnSkillCancelRequest@CUSkill` |
| `CP_UserPortalTeleportRequest` | `@0062` | `@004F` | `OnPortalTeleportRequest@CUser` |
| `CP_UserSkillUseRequest` | `@0058` | `@0051` | `OnSkillUseRequest@CUSkill` |
| `CP_UserConsumeCashItemUseRequest` | `@004D` | `@0053` | `OnConsumeCashItemUseRequest@CUser` |
| `CP_UserShopScannerItemUseRequest` | missing | `@0056` | `OnShopScannerItemUseRequest@CUser` |
| `CP_UserMapTransferItemUseRequest` | missing | `@005E` | `OnMapTransferItemUseRequest@CUser` |
| `CP_UserChangeSlotPositionRequest` | `@0045` | `@0062` | `OnChangeSlotPositionRequest@CQWUInventory` |
| `CP_UserStatChangeItemUseRequest` | `@0046` | `@0063` | `OnStatChangeItemUseRequest@CUser` |
| `CP_UserPortalScrollUseRequest` | `@0052` | `@0064` | `OnPortalScrollUseRequest@CUser` |
| `CP_UserUpgradeItemUseRequest` | `@0053` | `@0065` | `OnUpgradeItemRequest@CQWUInventory` |
| `CP_UserAbilityUpRequest` | `@0054` | `@0066` | `OnAbilityUpRequest@CUser` |
| `CP_UserDropMoneyRequest` | `@005B` | `@0068` | `OnDropMoneyRequest@CUser` |

## Identified But Not Applied Yet

These were intentionally left alone for now:

| Packet or opcode | Reason |
| --- | --- |
| `CP_UserRemoteShopOpenRequest` | The closest BMS entry is not a direct one-to-one name match, so this needs a separate pass |
| `CP_UserAbilityMassUpRequest` | No direct high-confidence match from the recovered `CUser::OnPacket` switch |
| `0x5F` / `0x60` anti-macro flow | The BMS IDB shows `OnAntiMacroItemRequest` and `OnAntiMacroQuestionResult`, but the current Java request switch does not implement them yet |
| login-side packets | Login currently works, so this pass avoided touching `BMS_WvsLogin` mappings without a dedicated login diff |

## Why This Pass Is Safe

This pass only changes:

- packet numbers already backed by the original `BMS_WvsGame.idb`
- packets that already have matching Java enums
- packets that already have a Java-side request handler

This pass does **not** change:

- movement decoding format
- mob or npc spawn logic
- server-to-client packet layout
- login packet mappings
