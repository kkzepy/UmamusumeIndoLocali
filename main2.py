import json, csv

#_cst = json.load(open("t_cst.json","r"))
#out = ""
#
#for i in t_cst:
#    out+=f"{i['character_id']},{i['voice_id']},{i['text']}\n"
#
#with open("t_cst.csv", "w", encoding="utf-8") as f:
#    f.write(out)*/

out = []

with open("t_cst.csv","r",encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        out.append(row)

json.dump(out,open("t_cst.json","w",encoding="utf-8"), indent=4)