# Tool Notes

This folder indexes the local tooling workflow used around the project.

## Main Tool Areas

- `../../tools/idb/`
  - Python scripts for extracting names, dispatch tables, opcode switches and unknown packet summaries from the local IDBs
- `../../tools/RirePE/`
  - upstream `RirePE` source submodule
- `../../tools/tools/`
  - upstream dependency submodule required to build `RirePE`
- `../../tools/RirePE_runtime/`
  - local runtime drop folder for `RirePE.exe` and `Packet.dll`

## Local Entry Points

- `../../tools/README.md`
  - top-level index for the `tools/` folder
- `../../packet_trace_live.bat`
  - tails `log/PacketTrace.log` in a separate console so packet traffic can be watched without `RirePE`
- `../../tools/README_RirePE.md`
  - detailed local notes for building and launching `RirePE`
- `../../build_rirepe_x86.bat`
  - one-click local x86 build chain for `RirePE`
- `../../launch_BMS_v24_client_analysis.bat`
  - helper that opens the BMS client and the local `RirePE` UI

## Output Relationship

- raw IDB input stays under `idb_client/idb/`
- generated extraction output is written to `docs/idb/generated/`
- curated conclusions belong under `docs/`, split by area

## Packet Trace

The Java server can now emit a full packet trace when:

- `debug.show_network_log = true` in [test.properties](/C:/Users/andre/Dropbox/games/ms_server/bms_v024/JMSv186/properties/test.properties)

The trace is written to:

- `log/PacketTrace.log`

and can be tailed live with:

- [packet_trace_live.bat](/C:/Users/andre/Dropbox/games/ms_server/bms_v024/JMSv186/packet_trace_live.bat)
