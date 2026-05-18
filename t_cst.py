from util import *
from deep_translator import GoogleTranslator, exceptions
from db import *
import config, json, time

MasterDB.Connect(config.MASTER_DB)
cursor = MasterDB.cursor

cursor.execute("SELECT * FROM character_system_text")
character_system_text = cursor.fetchall()

translator = GoogleTranslator(config.TRANSLATOR_SOURCE, config.TRANSLATOR_TARGET)

translated_character_system_text = []
try:
    translated_character_system_text = json.load(open(config.CHARACTER_SYSTEM_TEXT_EXPORT, "r", encoding="utf-8"))
except FileNotFoundError:
    LogInfo(f"File {config.CHARACTER_SYSTEM_TEXT_EXPORT} not found! Will be created once program finished.")

def TranslateCST(start_from = 0):
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

        if id in config.CHARACTER_SYSTEM_TEXT_ID_EXCLUSIONS:
            exists = any(
                d["character_id"] == id# and d["index"] == index 
                for d in translated_character_system_text
            )
            if exists:
                LogWarning(f"id {id} was excluded but exists in result!")
                #if fix_touched_exclusions:
                matches = [d for d in translated_character_system_text if id == d.get("character_id", "")]

                translated_character_system_text.remove(matches[0])
                LogInfo(f"Removed {id}, {voice_id} from result.")

            LogInfo(f"Skipping character_id: {id}")
            continue

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

if __name__ == "__main__":
    try:
        start_time = time.perf_counter()
        LogInfo(f"Rows to process: {len(character_system_text)}, Current translated_character_system_text: {len(translated_character_system_text)}")
        time.sleep(3)
        TranslateCST(config.CHARACTER_SYSTEM_TEXT_LAST_ITERATION_INDEX)

    except KeyboardInterrupt:
        print()
        LogInfo("Cancelled by user.")
    except Exception as e:
        print()
        LogError(f"Unhandled exception: {e}")
        raise e

    finally:
        print()

        end_time = time.perf_counter()
        execution_time = end_time - start_time
        LogInfo(f"Execution time: {execution_time:.6f} seconds")
        
        LogInfo(f"To retry, set CHARACTER_SYSTEM_TEXT_LAST_ITERATION_INDEX to index + 1 from {config.CHARACTER_SYSTEM_TEXT_EXPORT}")
        LogInfo(f"Saving to {config.CHARACTER_SYSTEM_TEXT_EXPORT}")
        json.dump(translated_character_system_text, open(config.CHARACTER_SYSTEM_TEXT_EXPORT , "w", encoding="utf-8"), indent=4)