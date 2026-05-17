from util import *
from deep_translator import GoogleTranslator, exceptions
from db import *
import config, json, time

MasterDB.Connect(config.MASTER_DB)
cursor = MasterDB.cursor

cursor.execute("SELECT * FROM text_data")
text_data = cursor.fetchall()

translator = GoogleTranslator(config.TRANSLATOR_SOURCE, config.TRANSLATOR_TARGET)
translated_text_data = []
try:
    translated_text_data = json.load(open(config.TEXT_DATA_EXPORT, "r", encoding="utf-8"))
except FileNotFoundError:
    LogInfo(f"File {config.TEXT_DATA_EXPORT} not found! Will be created once program finished.")

def TranslateTD(start_from = 0, fix_touched_exclusions = False):
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

        if id in config.TEXT_DATA_EXCLUSIONS:# filters unwanted
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

        exists = any(
            d["id"] == id and d["index"] == index 
            for d in translated_text_data
        )
        if exists:
            LogInfo(f"Exists, skipping! {id}, {index}, {text}")
            continue

        matches = [d for d in translated_text_data if text == d.get("previous", "")]
        if len(matches)!=0: # if copy found, use that same value
            obj = {"i_index":row_index,"id": id, "category": category, "index":index, "text":matches[0]["text"], "previous":text}
            translated_text_data.append(obj)
            LogInfo("Found copy!, Index: " + str(row_index) + " " + str(obj))
            continue

        translated_text=None
        translated_text = translator.translate(text)

        while translated_text == None: # sometimes it fails to translate
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
            except exceptions.TranslationNotFound:#translator.translate(text)
                LogWarning("deep_translator.exceptions.TranslationNotFound, retrying...")

        translated_text = translated_text.replace("\\n","\n")
        obj = {"i_index":row_index,"id": id, "category": category, "index":index, "text":translated_text, "previous":text}
        translated_text_data.append(obj)
        LogInfo("Index: " + str(row_index) + " " + str(obj))

if __name__ == "__main__":
    try:
        start_time = time.perf_counter()
        LogInfo(f"Rows to process: {len(text_data)}, Current translated_text_data: {len(translated_text_data)}")
        time.sleep(3)
        TranslateTD(config.TEXT_DATA_LAST_ITERATION_INDEX, config.TEXT_DATA_FIX_TOUCHED_EXCLUSIONS)

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

        LogInfo(f"To retry, set TEXT_DATA_LAST_ITERATION_INDEX to i_index + 1 from {config.TEXT_DATA_EXPORT}")
        LogInfo(f"Saving to {config.TEXT_DATA_EXPORT}")
        json.dump(translated_text_data, open(config.TEXT_DATA_EXPORT , "w", encoding="utf-8"), indent=4)