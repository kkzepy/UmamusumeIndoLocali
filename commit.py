from db import *
from util import *
import json, time, config, re

t_td:list = json.load(open(config.TEXT_DATA_EXPORT, "r", encoding="utf-8"))
t_cst:list = json.load(open(config.CHARACTER_SYSTEM_TEXT_EXPORT, "r", encoding="utf-8"))

if __name__ == "__main__":
    start_time = time.perf_counter()
    try:
        MasterDB.Connect(config.MASTER_DB)
        cursor = MasterDB.cursor

        if config.CREATE_MASTER_DB_BACKUP:
            MasterDB.CreateBackup(config.MASTER_DB)

        if config.FIX_WORD_BEFORE_COMMIT:
            LogInfo("Fixing words before committing")
            time.sleep(3)

            for row in t_cst:
                character_id = row["character_id"]
                voice_id = row["voice_id"]
                text = row["text"]
                previous = row["previous"]

                for wk, wv in sorted(config.CHARACTER_SYSTEM_TEXT_WORD_FIX.items(), key=lambda x: len(x[0]), reverse=True):
                    if text!=previous and wk.lower() in text.lower():
                        text = re.sub(re.escape(wk), wv, text, flags=re.IGNORECASE)

                        t_cst[ t_cst.index(row) ]["text"] = text

                        LogInfo(f"CST_REPLACED: \"{wk}\" to \"{wv}\"\n\t{text}")

            for row in t_td:
                id = row["id"]
                category = row["category"]
                index = row["index"]
                text = row["text"]
                previous = row["previous"]

                for wk, wv in sorted(config.TEXT_DATA_WORD_FIX.items(), key=lambda x: len(x[0]), reverse=True):
                    if text!=previous and wk.lower() in text.lower():
                        text = re.sub(re.escape(wk), wv, text, flags=re.IGNORECASE)

                        t_td[ t_td.index(row) ]["text"] = text

                        LogInfo(f"TD_REPLACED: \"{wk}\" to \"{wv}\"\n\t{text}")

            print()
            LogInfo("Word fix complete.")

        confirm = ""

        while confirm != "y" or confirm != "n":
            confirm = input("Are you sure want to commit changes? (y/n): ").lower()
            if confirm == "y":
                break
            elif confirm == "n":
                LogInfo("Cancelling...")
                quit(0)
        

        LogInfo(f"Committing to {config.MASTER_DB} will be started in 5 seconds...")
        time.sleep(5)

        t_cst_icount = 0
        for i in t_cst:
            character_id = i["character_id"]
            voice_id = i["voice_id"]
            text = i["text"]
            previous= i["previous"]

            update_query = f"UPDATE character_system_text SET text=? WHERE character_id=? AND voice_id=?"
            new_data = (text, character_id, voice_id)
            try:
                # 5. Execute the query
                cursor.execute(update_query, new_data)
                
                # 6. COMMIT the changes to the database (Crucial step!)
                MasterDB.connection.commit()
                LogInfo(f"CST_Successfully updated {cursor.rowcount} row(s) to {new_data}")
                t_cst_icount += 1

            except sqlite3.Error as error:
                print("CST_Failed to update data:", error)
                # Rollback in case of an error to keep database consistent
                MasterDB.connection.rollback()

        print()
        LogInfo(f"Done committing translated character system text. {t_cst_icount} Changes made.")
        time.sleep(3)

        t_td_icount = 0
        for i in t_td:
            id = i["id"]
            category = i["category"]
            index = i["index"]
            text:str = i["text"]
            previous = i["previous"]

            update_query = f"UPDATE text_data SET text=? WHERE id=? AND `index`=?"
            new_data = (text, id, index)
            try:
                # 5. Execute the query
                cursor.execute(update_query, new_data)
                
                # 6. COMMIT the changes to the database (Crucial step!)
                MasterDB.connection.commit()
                LogInfo(f"TD_Successfully updated {cursor.rowcount} row(s) to {new_data}")
                t_td_icount += 1

            except sqlite3.Error as error:
                LogError("TD_Failed to update data: "+str(error))
                # Rollback in case of an error to keep database consistent
                MasterDB.connection.rollback()

        print()
        LogInfo(f"Done committing translated text data. {t_td_icount} Changes made.")

    except KeyboardInterrupt:
        print()
        LogInfo("Cancelled by user.")

    finally:
        print()

        end_time = time.perf_counter()
        execution_time = end_time - start_time
        LogInfo(f"Execution time: {execution_time:.6f} seconds")

        MasterDB.Close()