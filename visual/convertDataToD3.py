import json

raw = open('test.json').read()

data = json.loads(raw)

out = {"nodes": [], "links": []}
for key, value in data.items():
    out["nodes"].append({"id": value["stationName"], "group": 1})
    for key1, value1 in value["duration"].items():
        out["links"].append({"source": value["stationName"], "target": data[key1]["stationName"], "duration": value1})

f = open("out.json", "w")
f.write(json.dumps(out))
f.close()
print("Data convert done! You can find it in out.json")

