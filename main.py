from db import *
import deep_translator
from deep_translator import GoogleTranslator
from util import *
import json, time

character_system_text: list
text_data: list
translated_character_system_text: list = json.load(open("t_cst.json", "r", encoding="utf-8"))
translated_text_data: list = json.load(open("t_td.json", "r", encoding="utf-8"))
translator = GoogleTranslator(source='en', target='id')

MasterDB.Connect("./master.mdb")

cursor = MasterDB.cursor
#MasterDB.CreateBackup("")

cursor.execute("SELECT * FROM character_system_text")
character_system_text = cursor.fetchall()

text_data_exclusions = [
    4, 5, # characters codename (eg: Hot Rod)
    6, 170, 75, 182, 77, 78, 95, # characters name (eg: Maruzensky)
    76, #character titles
    163, #88, #character introduction (could be confusing if translated?)
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
    16 # song names
]

#cursor.execute(f"SELECT * FROM text_data WHERE id NOT IN {str(text_data_exclusions).replace("[","(").replace("]",")")}")
cursor.execute("SELECT * FROM text_data")
text_data = cursor.fetchall()

def TranslateCST(limit = 0, start_from = 0):
    cst = character_system_text[start_from:]
    #if limit!=0 or limit!= -1:
    #    cst = character_system_text[:limit]

    #print(cst)

    for row in cst:
        id = row["character_id"]
        voice_id = row["voice_id"]
        text = row["text"]
        row_index = character_system_text.index(row)
        
        if voice_id == 11 or voice_id == 12: continue

        exists = any(
            d["character_id"] == id and d["voice_id"] == voice_id 
            for d in translated_character_system_text
        )
        if exists:
            LogInfo(f"Dupe! {id}, {voice_id}, {text}")
            continue

        matches = [d for d in translated_character_system_text if text == d.get("previous", "")]#exist = any(d.get('text') == text for d in translated_character_system_text)
        if len(matches)!=0:
            obj = {"index":row_index,"character_id": id, "voice_id": voice_id, "text":matches[0]["text"], "previous":text}
            translated_character_system_text.append(obj)
            LogInfo("Found copy!, Index: " + str(row_index) + " " + str(obj))
            continue

        translated_text=translator.translate(text)
        if translated_text==None or "Error 500 (Server Error)" in translated_text:
            retries = 0
            while translated_text==None or "Error 500 (Server Error)" in translated_text:
                LogInfo(f"{text}: Retrying translate...")
                translated_text = translator.translate(text)
                retries+=1
                if retries>=10:
                    LogWarning(f"Skipping: \"{text}\", defaulting to its own value.")
                    translated_text = text

        obj = {"index":row_index,"character_id": id, "voice_id": voice_id, "text":translated_text, "previous":text}
        translated_character_system_text.append(obj)
        LogInfo("Index: " + str(row_index) + " " + str(obj))
        
def TranslateTD(limit = 0, start_from = 0, fix_touched_exclusions = False):
    td = text_data[start_from:]
    #if limit!=0 or limit!= -1:
    #    cst = character_system_text[:limit]

    #print(cst)

    for row in td:
        id = row["id"]
        category = row["category"]
        index = row["index"]
        text = row["text"]
        row_index = text_data.index(row)
        
        #if voice_id == 11 or voice_id == 12: continue

        if id in text_data_exclusions:# or category in text_data_exclusions:
            #LogInfo(f"{id}, {index}, {text}")
            exists = any(
                d["id"] == id# and d["index"] == index 
                for d in translated_text_data
            )
            if exists:
                LogWarning(f"id {id} was excluded but exists in result!")
                if fix_touched_exclusions:
                    matches = [d for d in translated_text_data if id == d.get("id", "")]
                    """to_fix_index = translated_text_data.index(matches)
                    matches["text"] = matches["previous"]
                    translated_text_data[to_fix_index] = matches 
                    LogInfo(f"Fixed touched exclusions id {id} index {index}: {translated_text_data[to_fix_index]}")
                    time.sleep(.1)"""
                    translated_text_data.remove(matches[0])
                    LogInfo(f"Removed {id}, {index} from result.")

            continue
        #continue

        exists = any(
            d["id"] == id and d["index"] == index 
            for d in translated_text_data
        )
        if exists:
            LogInfo(f"Dupe! {id}, {index}, {text}")
            continue

        matches = [d for d in translated_text_data if text == d.get("previous", "")]
        if len(matches)!=0:
            obj = {"i_index":row_index,"id": id, "category": category, "index":index, "text":matches[0]["text"], "previous":text}
            translated_text_data.append(obj)
            LogInfo("Found copy!, Index: " + str(row_index) + " " + str(obj))
            continue

        translated_text=None
        translated_text = translator.translate(text)

        while translated_text == None:
            try:
                if translated_text==None or "Error 500 (Server Error)" in translated_text:
                    retries = 0
                    while translated_text==None or "Error 500 (Server Error)" in translated_text:
                        LogInfo(f"{text}: Retrying translate...")
                        translated_text = translator.translate(text)
                        retries+=1
                        if retries>=10:
                            LogWarning(f"Skipping: \"{text}\", defaulting to its own value.")
                            translated_text = text
                            break
            except deep_translator.exceptions.TranslationNotFound:#translator.translate(text)
                LogWarning("deep_translator.exceptions.TranslationNotFound, retrying...")

        translated_text = translated_text.replace("\\n","\n")
        obj = {"i_index":row_index,"id": id, "category": category, "index":index, "text":translated_text, "previous":text}
        translated_text_data.append(obj)
        LogInfo("Index: " + str(row_index) + " " + str(obj))

def TranslateCertainChar(char_id:int, source_lang:str, target_lang:str, start_from:int = 0):
    translator = GoogleTranslator(source_lang, target_lang)
    cst = character_system_text[start_from:]
    result = []

    try:
        for row in cst:
            character_id = row["character_id"]
            voice_id = row["voice_id"]
            text = row["text"]
            row_index = character_system_text.index(row)

            if character_id == char_id:
                if voice_id == 11 or voice_id == 12: continue

                exists = any(
                    d["character_id"] == id and d["voice_id"] == voice_id 
                    for d in result
                )
                if exists:
                    LogInfo(f"Dupe! {id}, {voice_id}, {text}")
                    continue

                matches = [d for d in result if text == d.get("previous", "")]#exist = any(d.get('text') == text for d in result)
                if len(matches)!=0:
                    obj = {"index":row_index,"character_id": character_id, "voice_id": voice_id, "text":matches[0]["text"], "previous":text}
                    result.append(obj)
                    LogInfo("Found copy!, Index: " + str(row_index) + " " + str(obj))
                    continue

                translated_text=translator.translate(text)
                if translated_text==None or "Error 500 (Server Error)" in translated_text:
                    retries = 0
                    while translated_text==None or "Error 500 (Server Error)" in translated_text:
                        LogInfo(f"{text}: Retrying translate...")
                        translated_text = translator.translate(text)
                        retries+=1
                        if retries>=10:
                            LogWarning(f"Skipping: \"{text}\", defaulting to its own value.")
                            translated_text = text

                obj = {"index":row_index,"character_id": character_id, "voice_id": voice_id, "text":translated_text, "previous":text}
                result.append(obj)
                LogInfo("Index: " + str(row_index) + " " + str(obj))
    except KeyboardInterrupt:
        return result

        
    return result

tama:list

try:
    #LogInfo("Rows to process: "+str(len(character_system_text)))
    #TranslateCST(0,0)
    LogInfo("Rows to process: "+str(len(text_data)))
    TranslateTD(0, 0, True)
    #tama = TranslateCertainChar(1021, "id", "su")
    #json.dump(tama,open("tama.json","W",encoding="utf-8"))
    pass
except KeyboardInterrupt:
    pass
except Exception as e:
    raise e
finally:
    #json.dump(translated_character_system_text, open("t_cst.json","w"), indent=4)
    json.dump(translated_text_data, open("t_td.json","w"), indent=4)
    #json.dump(tama,open("tama.json","w",encoding="utf-8"),indent=4)
    MasterDB.Close()