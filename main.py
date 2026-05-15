from db import *
from deep_translator import GoogleTranslator
from util import *
import json, csv

def LoadT_CSTFromCSV(path):
    with open(path,"r") as f:
        raw = f.read()
        rows = raw.split("\n")

        for i in rows:
            i = i.split(",",3)

character_system_text: list
text_data: list
translated_character_system_text: list = [{'character_id': 1001, 'voice_id': 10000, 'text': 'Aku akan menjadi lebih kuat... bersama dengan semua rivalku!', 'previous': "I'm gonna get stronger... together with all of my rivals!"}]
translated_text_data: list = []
translator = GoogleTranslator(source='auto', target='id')

MasterDB.Connect()

cursor = MasterDB.cursor
MasterDB.CreateBackup()

cursor.execute("SELECT * FROM character_system_text")
character_system_text = cursor.fetchall()
cursor.execute("SELECT * FROM text_data")
text_data = cursor.fetchall()

def TranslateCST(limit = 0):
    for row in character_system_text[:limit]:
        id = row["character_id"]
        voice_id = row["voice_id"]
        text = row["text"]
        
        if voice_id == 11 or voice_id == 12: continue

        matches = [d for d in translated_character_system_text if text in d.get("previous", "")]#exist = any(d.get('text') == text for d in translated_character_system_text)
        if len(matches)!=0:
            obj = {"character_id": id, "voice_id": voice_id, "text":matches[0]["text"], "previous":text}
            translated_character_system_text.append(obj)
            LogInfo("Found copy!, Index: " + str(character_system_text.index(row)) + " " + str(obj))
            continue

        translated_text=translator.translate(text)
        if "Error 500 (Server Error)" in translated_text:
            while "Error 500 (Server Error)" in translated_text:
                LogInfo("Retrying translate...")
                translated_text = translator.translate(text)

        obj = {"character_id": id, "voice_id": voice_id, "text":translated_text, "previous":text}
        translated_character_system_text.append(obj)
        LogInfo("Index: " + str(character_system_text.index(row)) + " " + str(obj))
        

try:
    LogInfo("Rows to process: "+str(len(character_system_text)))
    TranslateCST(-1)
except KeyboardInterrupt:
    pass
except Exception as e:
    LogError(e)
finally:
    json.dump(translated_character_system_text, open("t_cst.json","w"), indent=4)
    MasterDB.Close()