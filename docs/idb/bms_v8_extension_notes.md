# BMS v8 Extension Notes

## Purpose

These notes summarize what the old `bms_v8` C++/TSQL project is useful for when investigating BMS behavior in the current Java project.

Reference folder:

- [Extension](/C:/Users/andre/Dropbox/games/ms_server/bms_v8/bms-v8/Extension)

## What It Is Good For

- historical evidence about BMS-specific quirks
- hints about which systems were already known to diverge from GMS/JMS baselines
- confirming that some packet/layout problems are real BMS differences, not Java-port mistakes

## Most Useful Findings

### Movement Was Already Known To Be Different

In:

- [WvsGame.cpp](/C:/Users/andre/Dropbox/games/ms_server/bms_v8/bms-v8/Extension/WvsGame/WvsGame.cpp)

there is a hook around the user movement inspection path, with comments indicating that the original BMS behavior could disconnect users on specific maps if movement validation stayed untouched.

That strongly supports the current BMS v24 finding that movement cannot be assumed to match nearby JMS/GMS branches.

### BMS Often Differs By A Small Decode Mismatch

In:

- [Addy.cpp](/C:/Users/andre/Dropbox/games/ms_server/bms_v8/bms-v8/Extension/WvsClient/Addy.cpp)

there is an explicit note about a `GW_CharacterStat_Decode` fix involving an extra `Decode4()`.

That is important because the same pattern appeared again in the current BMS v24 work:

- `LP_MobEnterField`
- `LP_MobChangeController`

Both needed one more trailing `Encode4(0)` to match what the BMS client decodes.

### The Old Project Is Better As Reference Than As Drop-In Logic

The `Extension` tree is mostly:

- hooks
- patches
- wrappers around original binary behavior

It is not a full reimplementation of the server/client protocol in readable standalone code.

That means it is useful to:

- confirm suspicions
- narrow down likely packet families
- spot known BMS-only quirks

But it is not enough by itself to replace IDB-based packet work.

## What It Did Not Directly Solve

The old `Extension` folder did not provide a ready-made readable `CMobPool` packet layout for:

- mob spawn
- mob controller change
- mob movement

So for the current BMS v24 work, the IDB still remains the primary source of truth for exact packet structure.

## Takeaway

The old `bms_v8` project is valuable because it confirms the pattern:

- BMS differs in packet decode details
- movement is a known fragile area
- a one-field mismatch like an extra `Decode4()` is realistic and should be expected

That makes it a strong supporting reference, even when the exact final layout still has to come from the IDB and runtime logs.
