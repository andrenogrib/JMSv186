# WvsGame User Packet Switch

This document is extracted from `CUser::OnPacket` in `BMS_WvsGame.idb`.

- Function: `?OnPacket@CUser@@QAEXJAAVCInPacket@@@Z`
- Function start: `0x00590986`
- Function end: `0x0059127E`
- Opcode base: `0x12`
- Opcode max: `0xB6`
- Byte table: `0x0059115D`
- Jump table: `0x00590FFD`

## Focus Opcodes

| Opcode | Result | Case | Case Target | Handler |
| --- | --- | --- | --- | --- |
| `0x56` | Routed by `CUser::OnPacket` | `53` | `0x00590B82` | `0x005A05E9` `?OnShopScannerItemUseRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x5F` | Routed by `CUser::OnPacket` | `60` | `0x00590C6C` | `0x0059E204` `?OnAntiMacroItemRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0xC4` | Outside primary `CUser::OnPacket` switch |  |  |  |

## Full Switch Map

| Opcode | Case | Case Target | Handler |
| --- | --- | --- | --- |
| `0x12` | `0` | `0x00590CA0` | `0x0059E6F4` `?OnGuardInspectProcessResult@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x13` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x14` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x15` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x16` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x17` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x18` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x19` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x1A` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x1B` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x1C` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x1D` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x1E` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x1F` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x20` | `1` | `0x00590AA4` | `0x005CC388` `?OnTrunkRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x21` | `2` | `0x00590A8A` | `0x005A62E8` `?OnScriptMessageAnswer@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x22` | `3` | `0x00590A97` | `0x005C622E` `?OnShopRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x23` | `4` | `0x00590A7D` | `0x005A59B6` `?OnSelectNpc@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x24` | `5` | `0x00590AB1` | `0x005C8EF8` `?OnEntrustedShopRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x25` | `6` | `0x00590ABE` | `0x005C904B` `?OnStoreBankRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x26` | `7` | `0x00590D97` | `0x005B9B91` `?OnParcelRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x27` | `8` | `0x005909E7` | `0x005923A0` `?OnTransferChannelRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x28` | `9` | `0x005909F1` | `0x00592541` `?OnMigrateToCashShopRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x29` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x2A` | `10` | `0x00590A24` | `0x00597061` `?OnHit@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x2B` | `11` | `0x00590A05` | `0x00592ED5` `?OnSitRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x2C` | `12` | `0x00590A2E` | `0x00595627` `?OnChat@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x2D` | `13` | `0x00590A0F` | `0x00592F8F` `?OnPortableChairSitRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x2E` | `14` | `0x00590A19` | `0x0059587D` `?OnAttack@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x2F` | `15` | `0x005909CD` | `0x005918B1` `?OnTransferFieldRequest@CUser@@IAEXHAAVCInPacket@@@Z` |
| `0x30` | `16` | `0x00590D2F` | `0x0059A5D8` `?OnAdmin@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x31` | `17` | `0x00590CFB` | `0x005BCA70` `?OnPartyRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x32` | `18` | `0x00590D3C` | `0x0059B8AB` `?OnLog@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x33` | `19` | `0x00590D49` | `0x005BD3C5` `?OnFriendRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x34` | `20` | `0x00590D22` | `0x005B600E` `?OnGuildResult@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x35` | `21` | `0x005909FB` | `0x0059272B` `?OnMove@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x36` | `14` | `0x00590A19` | `0x0059587D` `?OnAttack@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x37` | `22` | `0x00590A70` | `0x005A13A7` `?OnBanMapByMob@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x38` | `23` | `0x00590AD8` | `0x005A87A2` `?OnShopScannerRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x39` | `24` | `0x00590AE5` | `0x005A8840` `?OnShopLinkRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x3A` | `25` | `0x00590A42` | `0x0059A35E` `?OnGroupMessage@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x3B` | `26` | `0x00590A4C` | `0x0059A231` `?OnCoupleMessage@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x3C` | `27` | `0x00590D15` | `0x005B4BF4` `?OnGuildRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x3D` | `28` | `0x00590CE1` | `0x00589D53` `?OnMessenger@CUMessenger@@QAEXAAVCInPacket@@@Z` |
| `0x3E` | `29` | `0x00590CEE` | `0x0058BE5B` `?OnMiniRoom@CUMiniRoom@@QAEXAAVCInPacket@@@Z` |
| `0x3F` | `30` | `0x00590D08` | `0x005BD0DC` `?OnPartyResult@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x40` | `31` | `0x00590D63` | `0x0059BF03` `?OnMemoFlagRequestFromHacker@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x41` | `32` | `0x00590D70` | `0x0059BF13` `?OnEnterTownPortalRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x42` | `33` | `0x00590CC7` | `0x0059A077` `?OnSlideRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x43` | `34` | `0x00590CBA` | `0x00599E7D` `?OnBroadcastMsg@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x44` | `35` | `0x00590C11` | `0x0059476E` `?OnCharacterInfoRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x45` | `36` | `0x00590C1E` | `0x005C08BA` `?OnActivatePetRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x46` | `37` | `0x00590C2B` | `0x0059C13F` `?OnTemporaryStatUpdateRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x47` | `38` | `0x00590C38` | `0x005A6082` `?OnPortalScriptRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x48` | `39` | `0x00590BEA` | `0x005D214B` `?OnSkillPrepareRequest@CUSkill@@QAEXAAVCInPacket@@@Z` |
| `0x49` | `40` | `0x00590B27` | `0x00593BFB` `?OnStatChangeItemCancelRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x4A` | `41` | `0x00590B34` | `0x00593DEC` `?OnUserStatChangeByPortableChairRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x4B` | `42` | `0x00590B41` | `0x005941E8` `?OnMobSummonItemUseRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x4C` | `43` | `0x00590B4E` | `0x005BFEB1` `?OnPetFoodItemUseRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x4D` | `44` | `0x00590BC3` | `0x005D16AC` `?OnSkillUpRequest@CUSkill@@QAEXAAVCInPacket@@@Z` |
| `0x4E` | `45` | `0x00590BDD` | `0x005D233C` `?OnSkillCancelRequest@CUSkill@@QAEXAAVCInPacket@@@Z` |
| `0x4F` | `46` | `0x00590C45` | `0x005A62E5` `?OnPortalTeleportRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x50` | `47` | `0x00590C52` | `0x0059DF52` `?OnMapTransferRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x51` | `48` | `0x00590BD0` | `0x005D193A` `?OnSkillUseRequest@CUSkill@@QAEXAAVCInPacket@@@Z` |
| `0x52` | `49` | `0x00590B5B` | `0x0059FD74` `?OnTamingMobFoodItemUseRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x53` | `50` | `0x00590B9C` | `0x005ABAF7` `?OnConsumeCashItemUseRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x54` | `51` | `0x00590B68` | `0x0059FFF8` `?OnBridleItemUseRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x55` | `52` | `0x00590B75` | `0x005A0957` `?OnSkillLearnItemUseRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x56` | `53` | `0x00590B82` | `0x005A05E9` `?OnShopScannerItemUseRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x57` | `54` | `0x00590D56` | `0x0059BB44` `?OnMemoRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x58` | `55` | `0x00590CD4` | `0x0059A0D5` `?OnWhisper@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x59` | `14` | `0x00590A19` | `0x0059587D` `?OnAttack@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x5A` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x5B` | `56` | `0x00590A38` | `0x0059580A` `?OnADboardClose@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x5C` | `57` | `0x00590A56` | `0x00593068` `?OnEmotion@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x5D` | `58` | `0x00590A63` | `0x005930FF` `?OnSetActiveEffectItem@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x5E` | `59` | `0x00590B8F` | `0x005AC367` `?OnMapTransferItemUseRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x5F` | `60` | `0x00590C6C` | `0x0059E204` `?OnAntiMacroItemRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x60` | `61` | `0x00590C79` | `0x0059E37A` `?OnAntiMacroQuestionResult@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x61` | `62` | `0x00590C86` | `0x0059E7E6` `?OnClaimRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x62` | `63` | `0x00590AF2` | `0x0052209D` `?OnChangeSlotPositionRequest@CQWUInventory@@IAEXAAVCInPacket@@@Z` |
| `0x63` | `64` | `0x00590B19` | `0x00593667` `?OnStatChangeItemUseRequest@CUser@@QAEXAAVCInPacket@@H@Z` |
| `0x64` | `65` | `0x00590BA9` | `0x00593ECE` `?OnPortalScrollUseRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x65` | `66` | `0x00590AFF` | `0x005218EA` `?OnUpgradeItemRequest@CQWUInventory@@IAEXAAVCInPacket@@@Z` |
| `0x66` | `67` | `0x00590B0C` | `0x005934F1` `?OnAbilityUpRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x67` | `68` | `0x00590BB6` | `0x00593264` `?OnChangeStatRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x68` | `69` | `0x00590BF7` | `0x00594485` `?OnDropMoneyRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x69` | `70` | `0x00590C04` | `0x00594669` `?OnGivePopularityRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x6A` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x6B` | `71` | `0x00590ACB` | `0x005A660B` `?OnQuestRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x6C` | `72` | `0x00590C93` | `0x0059127E` `?OnCalcDamageStatSetRequest@CUser@@QAEXAAVCInPacket@@@Z` |
| `0x6D` | `73` | `0x00590C5F` | `0x0059EEB9` `?OnSueCharacterRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x6E` | `74` | `0x00590DA4` | `0x0059C1AD` `?OnMarriageRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x6F` | `75` | `0x00590DB1` | `0x005CF003` `?OnWeddingGiftRequest@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x70` | `76` | `0x00590DBE` | `0x0059C6ED` `?OnWeddingProgress@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x71` | `77` | `0x00590DCB` | `0x0059C733` `?OnGuestBless@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x72` | `78` | `0x00590CAD` | `0x0059E596` `?OnBoobyTrapAlert@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x73` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x74` | `79` | `0x00590DD8` | `0x005B66B8` `?OnGuildBBSPacket@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x75` | `80` | `0x00590D7D` | `0x0059B952` `?OnFuncKeyMappedModified@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x76` | `81` | `0x00590D8A` | `0x005C43EB` `?OnRPSGamePacket@CUser@@IAEXAAVCInPacket@@@Z` |
| `0x77` | `82` | `0x00590E1D` | `0x005A16B3` `?OnMigrateToITCRequest@CUser@@QAEXAAVCInPacket@@@Z` |
| `0x78` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x79` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x7A` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x7B` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x7C` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x7D` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x7E` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x7F` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x80` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x81` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x82` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x83` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x84` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x85` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x86` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x87` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x88` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x89` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x8A` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x8B` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x8C` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x8D` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x8E` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x8F` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x90` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x91` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x92` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x93` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x94` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x95` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x96` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x97` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x98` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x99` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x9A` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x9B` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x9C` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x9D` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x9E` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0x9F` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0xA0` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0xA1` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0xA2` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0xA3` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0xA4` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0xA5` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0xA6` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0xA7` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0xA8` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0xA9` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0xAA` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0xAB` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0xAC` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0xAD` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0xAE` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0xAF` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0xB0` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0xB1` | `83` | `0x00590E03` | `0x0059C741` `?OnPlantRefresh@CUser@@IAEXAAVCInPacket@@@Z` |
| `0xB2` | `84` | `0x00590E10` | `0x0059C759` `?OnPlantUIState@CUser@@IAEXAAVCInPacket@@@Z` |
| `0xB3` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0xB4` | `87` | `0x00590E2A` | `0x005BFE4B` `?OnPetPacket@CUser@@IAEXJAAVCInPacket@@@Z` |
| `0xB5` | `85` | `0x00590DE5` | `0x005A101E` `?OnMapleTVSendMessage@CUser@@QAEXAAVCInPacket@@@Z` |
| `0xB6` | `86` | `0x00590DF2` | `0x004D2763` `?OnPacket@CMapleTVViewCountUpdater@@QAEXAAVCInPacket@@@Z` |
