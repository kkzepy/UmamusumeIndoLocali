from db import *
from util import *
import os, config, shutil

if __name__ == "__main__":
    backup_path = Path.joinpath(Path(config.MASTER_DB).parent, "master.mdb.bak")

    if not os.path.exists(backup_path):
        LogError(f"Backup file {backup_path} doesn't exist!")
        quit(1)
    
    if not os.path.exists(config.MASTER_DB):
        LogError(f"Master database file {config.MASTER_DB} doesn't exist!")
        quit(1)

    LogInfo(f"Backup file found {backup_path}")
    LogInfo(f"Master database file found {config.MASTER_DB}")

    confirm = ""

    while confirm != "y" or confirm != "n":
        confirm = input("Are you sure want to revert changes? This will rewrite the entire the master database. (y/n): ").lower()
        if confirm == "y":
            break
        elif confirm == "n":
            LogInfo("Cancelling...")
            quit(0)

    os.remove(config.MASTER_DB)
    shutil.copy(backup_path, config.MASTER_DB)
    
    LogInfo(f"Master database {config.MASTER_DB} successfully reverted based on backup file.")