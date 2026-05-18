from db import *
from util import *
import os, config, shutil, sqlite3

backup_path = Path.joinpath(Path(config.MASTER_DB).parent, "master.mdb.bak")

def HardReset():
    os.remove(config.MASTER_DB)
    shutil.copy(backup_path, config.MASTER_DB)
    
    LogInfo(f"Master database {config.MASTER_DB} successfully reverted based on backup file.")

def RestoreTables():
    MasterDB.Connect(config.MASTER_DB)
    cursor = MasterDB.cursor

    backup_mdb = sqlite3.connect(backup_path)
    backup_mdb.row_factory = sqlite3.Row
    backup_cursor = backup_mdb.cursor()

    backup_cursor.execute("SELECT character_id, voice_id, text FROM character_system_text")
    o_cst_rows = backup_cursor.fetchall()
    cst_count = 0

    for o_cst_row in o_cst_rows:
        cursor.execute("SELECT character_id, voice_id, text FROM character_system_text WHERE character_id=? AND voice_id=?", (o_cst_row["character_id"], o_cst_row["voice_id"]))
        t_cst_row = cursor.fetchone()

        if (
            t_cst_row is None or
            t_cst_row["text"] != o_cst_row["text"]
        ):
            LogInfo(f"Fixing {t_cst_row["character_id"]}, {t_cst_row["voice_id"]}, {t_cst_row["text"]}")

            cursor.execute("""
                UPDATE character_system_text
                SET text = ? 
                WHERE character_id = ? AND voice_id = ?
            """, (
                o_cst_row["text"],
                o_cst_row["character_id"],
                o_cst_row["voice_id"]
            ))

            cst_count+=1

    MasterDB.connection.commit()
    print()
    LogInfo(f"Done fixing character_system_text. {cst_count} changes made.")

    backup_cursor.execute("SELECT id, `index`, text FROM text_data")
    o_td_rows = backup_cursor.fetchall()
    td_count = 0

    for o_td_row in o_td_rows:
        cursor.execute("SELECT id, `index`, text FROM text_data WHERE id=? AND `index`=?", (o_td_row["id"], o_td_row["index"]))
        t_td_row = cursor.fetchone()

        if (
            t_td_row is None or
            t_td_row["text"] != o_td_row["text"]
        ):
            LogInfo(f"Fixing {t_td_row["id"]}, {t_td_row["index"]}, {t_td_row["text"]}")

            cursor.execute("""
                UPDATE text_data
                SET text = ? 
                WHERE id = ? AND `index` = ?
            """, (
                o_td_row["text"],
                o_td_row["id"],
                o_td_row["index"]
            ))

            td_count+=1
    
    MasterDB.connection.commit()
    print()
    LogInfo(f"Done fixing text_data. {td_count} changes made.")

    MasterDB.Close()
    backup_mdb.close()

if __name__ == "__main__":
    

    if not os.path.exists(backup_path):
        LogError(f"Backup file {backup_path} doesn't exist!")
        quit(1)
    
    if not os.path.exists(config.MASTER_DB):
        LogError(f"Master database file {config.MASTER_DB} doesn't exist!")
        quit(1)

    LogInfo(f"Backup file found {backup_path}")
    LogInfo(f"Master database file found {config.MASTER_DB}")

    reset_type = ""

    while True:
        reset_type = input("Pick reset type (o = overwrite with existing backup file, t = only revert affected tables, n = cancel): ").lower()
        if reset_type == "o":
            break
        elif reset_type == "t":
            break
        elif reset_type == "n":
            LogInfo("Cancelling...")
            quit(0)

    confirm = ""

    while True:
        if reset_type=="o": confirm = input("Are you sure want to revert changes? This will overwrite the entire the master database. (y/n): ").lower()
        if reset_type=="t": confirm = input("Are you sure want to revert changes? This will replace affected tables with it's original value. (y/n): ").lower()
        if confirm == "y":
            if reset_type == "o": HardReset()
            elif reset_type == "t": RestoreTables()
            break

        elif confirm == "n":
            LogInfo("Cancelling...")
            quit(0)

    