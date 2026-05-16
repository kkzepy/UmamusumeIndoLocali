import json, re, time
from db import *

MasterDB.Connect("./master.mdb")
cursor = MasterDB.cursor

word_fix = {
    "kapal emas": "Gold Ship",
    "putri kawakami": "Kawakami Princess",
    #"Jarang berangkat!": "Rar'n to go!",
    "raja halo": "King Halo",
    "Kafe Manhattan": "Manhattan Cafe",

    "piala jepang": "Japan Cup",
    "derby jepang": "Japan Derby",
    "Taruhan Musim Semi": "Spring Stakes",
    "taruhan sprinters": "Sprinters Stakes",
    "Taruhan yang Penuh Harapan": "Hopeful Stakes",
    "Taruhan Penuh Harapan": "Hopeful Stakes",
    "Pertaruhan yang Penuh Harapan": "Hopeful Stakes",
    "Taruhan Masa Depan Asahi Hai": "Asahi Hai Futurity Stakes",
    "Pertaruhan Februari": "February Stakes",
    "Taruhan Karir bulan Februari": "February Stakes di Karir",
    "Taruhan G1 Februari": "G1 February Stakes",
    "Taruhan Sprinter G1": "G1 Sprinters Stakes",
    "Taruhan Harapan G1": "G1 Hopeful Stakes",
    "Taruhan Harapan": "Hopeful Stakes",
    "Taruhan Utama": "Principal Stakes",
    "Taruhan Unicorn": "Unicorn Stakes",
    "Taruhan Takamatsunomiya Kinen dan Sprinters": "Takamatsunomiya Kinen and Sprinters Stakes",
    "Taruhan Umamusume": "Umamusume Stakes",
    "Taruhan Leopard": "Leopard Stakes",
    "Taruhan Macan Tutul": "Leopard Stakes",
    "Taruhan Junior": "Junior Stakes",
    "Taruhan Wakagoma": "Wakagoma Stakes",
    "Taruhan Angsa": "Swan Stakes",
    "Taruhan Setelah Sprinters": "Setelah Sprinters Stake",
    "Kehormatan di Taruhan": "Honor at Stake",
    "Taruhan Berlian": "Diamond Stakes",
    "Taruhan Pertanian": "Farming Stakes",
    "Taruhan Stayers": "Stayers Stakes",
    "Taruhan After the Stayers": "Stayers Stakes",
    "Taruhan Elm": "Elm Stakes",
    "Taruhan Negishi": "Negishi Stakes",
    "Taruhan Hanshin Umamusume": "Hanshin Umamusume Stakes",
    "Taruhan Fukushima Umamusume": "Fukushima Umamusume Stakes",
    "Taruhan Flora": "Flora Stakes",
    "Taruhan Centaur": "Centaur Stakes",
    "Taruhan Shion": "Shion Stakes",
    "Taruhan Fuchu": "Fuchu Stakes",
    "Taruhan Fuji": "Fuji Stakes",
    "Taruhan Miyako": "Miyako Stakes",
    "Taruhan Musashino": "Musashino Stakes",
    "Taruhan Tokai": "Tokai Stakes",
    "Taruhan Hanshin Umamusume": "Hanshin Umamusume Stakes",
    "Taruhan Antares": "Antares Stakes",

    "piala persatuan": "Unity Cup",
    "<warna": "<color",
    "</warna>": "</color>",
    "pramuka": "Scout",
    "piala kanker": "Piala Cancer",
    "balapan harian": "Daily Race",
    "mesin cakar": "Claw Machine",
    "kartu dukungan": "Support Card",
    "derby cantik": "Pretty Derby",
    "Uji Coba Tim": "Team Trials",
    
    "(Pemburu Kecepatan)": "(Pace Chaser)",
    "(Bedah Terlambat)": "(Late Surger)",
    "(Berakhir Lebih Dekat)": "(End Closer)",
    "(Pelari Depan)": "(Front Runner)",

    "(Sedang)": "(Medium)",
    "(Lari cepat)": "(Sprint)",
    "(Mil)": "(Mile)",
    "(Panjang)": "(Long)",

    "saya": "aku" #testing
}

t_td = json.load(open("t_td.json","r",encoding="utf-8"))
count = 0

LogInfo(f"t_td length: {len(t_td)}")

for i in t_td:
    id = i["id"]
    category = i["category"]
    index = i["index"]
    text:str = i["text"]
    previous = i["previous"]

    for wk, wv in word_fix.items():
        if text!=previous and wk.lower() in text.lower():
            #text = text.replace(wk, wv)
            text = re.sub(wk, wv, text, flags=re.IGNORECASE)
            LogInfo(f"REPLACED: \"{wk}\" to \"{wv}\"\n\t{text}")

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