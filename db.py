import sqlite3, os, shutil
from pathlib import Path
from util import *

class MasterDB:
    connection:sqlite3.Connection = None
    cursor:sqlite3.Cursor = None

    def Connect(path:str = "C:\\Users\\%username%\\AppData\\LocalLow\\Cygames\\Umamusume\\master\\master.mdb"):
        if "%" in path: path = os.path.expandvars(path)

        exist = os.path.exists(path)
        if not exist: LogError(f"The path {path} not found!"); return

        MasterDB.connection = sqlite3.connect(path)
        MasterDB.connection.row_factory = sqlite3.Row
        MasterDB.cursor = MasterDB.connection.cursor()

    def CreateBackup(path:str = "C:\\Users\\%username%\\AppData\\LocalLow\\Cygames\\Umamusume\\master\\master.mdb", backup_fname = "master.mdb.bak"):
        if "%" in path: path = os.path.expandvars(path)

        exist = os.path.exists(path)
        if not exist: LogError(f"The path {path} not found!"); return

        backup_path = Path.joinpath(Path(path).parent, backup_fname)
        if os.path.exists(backup_path): LogInfo(f"Backup {backup_path} already existed!"); return;

        shutil.copy(path, backup_path)
        LogInfo(f"Created backup of master.mdb to {backup_fname}")


    def Close():
        MasterDB.connection.close()