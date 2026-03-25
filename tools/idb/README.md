# IDB Tools

These scripts help extract reusable information from the local IDB set under `idb_client/idb`.

Generated output now lives under:

- `docs/idb/`
- `docs/idb/generated/`

## Scripts

- `inventory_idbs.py`
  - creates `docs/idb/idb_inventory.md`
- `extract_names.py`
  - extracts useful named functions and symbols from an IDB
- `extract_dispatch.py`
  - dumps disassembly for packet-facing dispatch functions that are already named in the IDB
- `extract_function_matches.py`
  - quickly filters named functions in large IDBs by substring patterns
- `extract_unknown_log.py`
  - groups `UNKNOWN` packet logs by opcode and payload
- `extract_wvsgame_user_opcodes.py`
  - decodes the main `CUser::OnPacket` opcode switch from `BMS_WvsGame.idb`
- `build_docs.py`
  - runs the current default documentation pipeline

## Usage

From the repo root:

```bat
python tools\idb\build_docs.py
```

For a custom log file:

```bat
python tools\idb\extract_unknown_log.py path\to\server.log
```

For a custom IDB:

```bat
python tools\idb\extract_names.py --idb idb_client\idb\BMS_v24.0_U_DEVM.idb
python tools\idb\extract_dispatch.py --idb idb_client\idb\BMS_v24.0_U_DEVM.idb
python tools\idb\extract_function_matches.py --idb idb_client\idb\BMS_srv\BMS_WvsGame.idb --pattern ProcessUserPacket --pattern Request@CUser
python tools\idb\extract_wvsgame_user_opcodes.py
```

## Notes

- The current default target is the main client IDB: `BMS_v24.0_U_DEVM.idb`
- For unknown packets sent by the client, `BMS_srv/BMS_WvsGame.idb` is often the highest-value server-side IDB
- The scripts are intentionally conservative: they dump named evidence and disassembly first, then we curate conclusions in Markdown under `docs/`
