from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from common import DEFAULT_CLIENT_IDB, REPO_ROOT


TOOLS_ROOT = Path(__file__).resolve().parent


def run(script_name: str, *args: str) -> None:
    script_path = TOOLS_ROOT / script_name
    cmd = [sys.executable, str(script_path), *args]
    print("RUN", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=str(REPO_ROOT))


def main() -> int:
    run("inventory_idbs.py")
    run("extract_names.py", "--idb", str(DEFAULT_CLIENT_IDB))
    run("extract_dispatch.py", "--idb", str(DEFAULT_CLIENT_IDB))
    run(
        "extract_function_matches.py",
        "--idb",
        str(REPO_ROOT / "idb_client" / "idb" / "BMS_srv" / "BMS_WvsGame.idb"),
        "--out-name",
        "BMS_WvsGame_focus.md",
        "--title",
        "WvsGame Packet Surface",
        "--pattern",
        "ProcessUserPacket",
        "--pattern",
        "OnPacket@CUser",
        "--pattern",
        "Request@CUser",
        "--pattern",
        "MakeEnterFieldPacket",
        "--pattern",
        "MakeLeaveFieldPacket",
        "--pattern",
        "SummonMob",
        "--pattern",
        "DestroyMob",
        "--pattern",
        "MobCtrl",
        "--pattern",
        "OnMove",
    )
    run(
        "extract_function_matches.py",
        "--idb",
        str(REPO_ROOT / "idb_client" / "idb" / "BMS_srv" / "BMS_WvsLogin.idb"),
        "--out-name",
        "BMS_WvsLogin_focus.md",
        "--title",
        "WvsLogin Packet Surface",
        "--pattern",
        "OnPacket",
        "--pattern",
        "CLogin",
        "--pattern",
        "CheckPassword",
        "--pattern",
        "World",
        "--pattern",
        "SelectChar",
        "--pattern",
        "DeleteChar",
    )
    run("extract_wvsgame_user_opcodes.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
