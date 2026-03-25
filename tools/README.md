# Tools Index

This folder contains local reverse-engineering helpers, build helpers and upstream submodules used by the project.

## Main Entries

- `idb/`
  - Python extraction scripts for the local IDB corpus
- `RirePE/`
  - upstream `RirePE` source submodule
- `tools/`
  - upstream dependency submodule required by `RirePE`
- `RirePE_runtime/`
  - local runtime drop folder for `RirePE.exe` and `Packet.dll`
- `README_RirePE.md`
  - local notes for building and using `RirePE` in this workspace

## Related Project Docs

- `../docs/tools/README.md`
  - curated tooling overview
- `../docs/idb/README.md`
  - IDB research index

## Local-Only Helper Folders

Some folders here are local helper/runtime folders and are not the same as the tracked upstream submodules:

- `GH_Injector/`
- `ExtremeInjector/`
- `RirePE_runtime/`

Treat those as local workspace support folders unless the repository explicitly starts versioning them later.
