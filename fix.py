import json

t_td = json.load(open("t_td.json","r",encoding="utf-8"))

for i in t_td:
    if "\\n" in i["text"]:
        fixed_text = i["text"].replace("\\n","\n")
        print(fixed_text)