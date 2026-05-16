import json, re, time
from db import *

MasterDB.Connect("./master.mdb")
cursor = MasterDB.cursor

word_fix = {
    "kapal emas": "Gold Ship",
    "piala jepang": "Japan Cup",
    "piala persatuan": "Unity Cup",
    "<warna": "<color",
    "</warna>": "</color>",
    "pramuka": "Scout",
    
    "(Pemburu Kecepatan)": "(Pace Chaser)",
    "(Bedah Terlambat)": "(Late Surger)",
    "(Berakhir Lebih Dekat)": "(End Closer)",
    "(Pelari Depan)": "(Front Runner)",

    "(Sedang)": "(Medium)",
    "(Lari cepat)": "(Sprint)",
    "(Mil)": "(Mile)",
    "(Panjang)": "(Long)"
}

t_td = json.load(open("t_td.json","r",encoding="utf-8"))
count = 0

LogInfo(len(t_td))

for i in t_td:
    id = i["id"]
    category = i["category"]
    index = i["index"]
    text:str = i["text"]
    previous = i["previous"]

    for wk, wv in word_fix.items():
        if wk.lower() in text.lower():
            #text = text.replace(wk, wv)
            text = re.sub(wk, wv, text, flags=re.IGNORECASE)
            LogInfo(f"Replaced: \"{wk}\" to \"{wv}\"\n\t{text}")

    update_query = f"UPDATE text_data SET text=? WHERE id=? AND `index`=?"
    new_data = (text, id, index)
    try:
        # 5. Execute the query
        cursor.execute(update_query, new_data)
        
        # 6. COMMIT the changes to the database (Crucial step!)
        MasterDB.connection.commit()
        LogInfo(f"Successfully updated {cursor.rowcount} row(s) to {new_data}")
        count+=1

    except sqlite3.Error as error:
        LogError("Failed to update data: "+str(error))
        # Rollback in case of an error to keep database consistent
        MasterDB.connection.rollback()


if MasterDB.connection:
    #cursor.close()
    MasterDB.Close()
    LogInfo(f"SQLite connection is closed. {count}")