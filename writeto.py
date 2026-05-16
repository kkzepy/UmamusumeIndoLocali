from db import *
import json

MasterDB.Connect("./master.mdb")

cursor = MasterDB.cursor

t_cst = json.load(open("t_cst_final.json","r",encoding="utf-8"))
count = 0

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
        print(f"Successfully updated {cursor.rowcount} row(s) to {new_data}")
        count+=1

    except sqlite3.Error as error:
        print("Failed to update data:", error)
        # Rollback in case of an error to keep database consistent
        MasterDB.connection.rollback()


if MasterDB.connection:
    #cursor.close()
    MasterDB.Close()
    print(f"SQLite connection is closed. {count}")