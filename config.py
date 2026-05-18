TRANSLATOR_SOURCE = "en"
TRANSLATOR_TARGET = "id"

MASTER_DB = "./master.mdb"
CREATE_MASTER_DB_BACKUP = True
FIX_WORD_BEFORE_COMMIT = True

TEXT_DATA_EXPORT = "t_td.json"
TEXT_DATA_LAST_ITERATION_INDEX = 0
TEXT_DATA_FIX_TOUCHED_EXCLUSIONS = True
TEXT_DATA_WORD_FIX = {
    "kapal emas": "Gold Ship",
    "putri kawakami": "Kawakami Princess",
    #"Jarang berangkat!": "Rar'n to go!",
    "raja halo": "King Halo",
    "Kafe Manhattan": "Manhattan Cafe",
    "topi oguri": "Oguri Cap",
    "kota emas": "Gold City",
    "bunga nishino": "Nishino Flower",
    "Hari Minggu yang Luar Biasa": "Marvelous Sunday",
    "Alam yang Bagus": "Nice Nature",
    "alam bagus": "Nice Nature",
    "gerakan halus": "Fine Motion",
    "kagumi vega": "Admire Vega",

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
    "arena balap": "Racecourse",

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
TEXT_DATA_EXCLUSIONS = [
    4, 5, # characters codename (eg: Hot Rod)
    6, 170, 75, 182, 77, 78, 95, # characters name (eg: Maruzensky)
    76, #character titles
    #163, #88, #character introduction (could be confusing if translated?)
    7, 59, 152, 264, # NPC/Mob names
    173, 174, # NPC names (ura finale)
    28, 29, 31, 32, 33, 34, 35, 36, 38, 111, 206, # race names
    39, 40, 42, #menu info (like daily things, not necessary)
    47, # skills name
    #48, # skills desc
    #48, # carats amount
    55, # training ui
    64, 65, #69, #63,  # could be confusing if translated
    #67,  # missions (could be confusing if translated)
    66,
    68, # comic panels/loading panels (could be confusing if translated)
    113, # star pieces names
    121, # fans level (could be confusing if translated)
    130, 132, 133, 136, 138, 147, 148, 150, 151, 172, 238, 241, 243, 244, 247, # some career/training/race things (could be confusing if translated/unecessary)
    42, # bad trainee conditions (could be confusing if translated)
    157, # date
    158, # heights
    159, # running types (eg: pace, end)
    160, # track types (eg: dirt, turf)
    161, # distances (eg: long 3000, sprint 1200)
    162, # divisions (eg: junior/senior)
    #203, # skill names
    16, # song names
    23 # items names
]

CHARACTER_SYSTEM_TEXT_EXPORT = "t_cst.json"
CHARACTER_SYSTEM_TEXT_LAST_ITERATION_INDEX = 0
CHARACTER_SYSTEM_TEXT_ID_EXCLUSIONS = [
    # Exclude certain characters here, seek charaname.txt
]
CHARACTER_SYSTEM_TEXT_WORD_FIX = TEXT_DATA_WORD_FIX