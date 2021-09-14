import json

json_data = {"name": "Midi satin skirt", "price": 89.99, "color": "black", "size": ["XS", "S - Not available I want it!", "M", "L - Not available I want it!", "XL"]}

# saving json file with parties dictionary
with open("data_test_set.json".format(1), "w", encoding="utf-8") as file:
    json.dump(json_data, file, ensure_ascii=False, indent=4, sort_keys=True)

# schema save to json file
schema_json = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "price": {"type": "number"},
        "color": {"type": "string"},
        "size": {"type": "array"},
    },
    "required": ["name", "price", "color", "size"]
}

with open("json_schema.json".format(1), "w", encoding="utf-8") as file:
    json.dump(schema_json, file, ensure_ascii=False, indent=4, sort_keys=True)
