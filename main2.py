import json, csv

#_cst = json.load(open("t_cst.json","r"))
#out = ""
#
#for i in t_cst:
#    out+=f"{i['character_id']},{i['voice_id']},{i['text']}\n"
#
#with open("t_cst.csv", "w", encoding="utf-8") as f:
#    f.write(out)*/

t_cst = json.load(open("t_cst.json", "r" ,encoding="utf-8"))

print(len(t_cst))

seen = set()
dupes = 0
cleaned_list = []

for d in t_cst:
    # Buat identifier unik menggunakan tuple (character_id, voice_id)
    identifier = (d["character_id"], d["voice_id"])
    
    # Jika belum pernah dilihat, masukkan ke list hasil dan tandai di set
    if identifier not in seen:
        seen.add(identifier)
        cleaned_list.append(d)
        continue
    dupes+=1

json.dump(cleaned_list, open("t_cst_final.json","w",encoding="utf-8"), indent=4)
print(f"Before: {len(t_cst)}, After: {len(cleaned_list)}, Dupes: {dupes}")