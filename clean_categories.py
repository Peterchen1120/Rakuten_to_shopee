import json


def clean_node(node: dict) -> dict:
    result = {
        "id": node["id"],
        "display_name": node["display_name"],
        "has_children": node["has_children"],
    }
    if node["has_children"] and node.get("children"):
        result["children"] = [clean_node(child) for child in node["children"]]
    return result


with open("classification_tree.json", encoding="utf-8") as f:
    raw = json.load(f)

categories = [clean_node(item) for item in raw["data"]["list"]]

with open("categories.json", "w", encoding="utf-8") as f:
    json.dump(categories, f, ensure_ascii=False, indent=2)

print(f"完成，共 {len(categories)} 個頂層分類")
