# RirePE Local Notes

## What is in this project

- `tools/RirePE`
  - Git submodule pointing to the upstream source repository: `https://github.com/Riremito/RirePE`
- `tools/tools`
  - Git submodule pointing to the upstream dependency repository: `https://github.com/Riremito/tools`
- `tools/RirePE_runtime`
  - Local folder reserved for runtime files if you later bring the official binaries

## Current local status

The source tree now builds locally in this workspace.

The missing `Share\Simple` and `Share\Hook` dependencies are supplied through the `tools/tools` submodule.

Current build output:

- `tools/RirePE/Release/RirePE.exe`
- `tools/RirePE/Release/Packet.dll`

## Local launcher

Use:

- `launch_BMS_v24_client_analysis.bat`

That script will:

- check that the BMS client exists
- open the client
- prefer the local build output inside `tools/RirePE/Release`
- fall back to `tools/RirePE_runtime` if you later place external binaries there
- open `RirePE.exe` too if it is present

## Rebuild helper

Use:

- `build_rirepe_x86.bat`

That script runs the full local chain:

- build `tools/tools/Simple`
- build `tools/tools/Hook`
- run `tools/tools/CopyLib.bat`
- run `tools/RirePE/GetLib.bat`
- build `tools/RirePE/RirePE.sln` for `x86`

## Runtime folder

If you later obtain the official runtime files from the upstream author/release, place them in:

- `tools/RirePE_runtime`

Expected filenames:

- `tools/RirePE_runtime/RirePE.exe`
- `tools/RirePE_runtime/Packet.dll`

## Client path used by the launcher

- `..\BMS_v24\BMS_v24.0_L.exe` relative to the repository root

## Current scope

This project now includes:

- the RirePE source submodule under `tools/RirePE`
- the Riremito dependency submodule under `tools/tools`
- a local runtime folder under `tools/RirePE_runtime`
- a click-to-launch batch file for the BMS client
- a local x86 build path for `RirePE.exe` and `Packet.dll`

If you want a larger reverse-engineering workflow after this, it is better to decide that together first.
