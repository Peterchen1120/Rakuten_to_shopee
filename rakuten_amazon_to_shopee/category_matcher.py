import chromadb
import json,requests
from pathlib import Path



def load_category():
    try:
        base = Path(__file__).parent.parent     
        with open(base / "shopee_categories/categories.json","r",encoding="utf-8") as f :
            data = json.load(f)
        return data
    except FileNotFoundError:
        print("File not exist")
    except:    
        raise RuntimeError("Cannot get category file.")

data = load_category()
print(type(data))
"""
leaf_list=[]
def build_tree(text,sub_list,count):
    # 男生衣服
    # 男生衣服 > 上衣
    # 男生衣服 > 上衣 > T-shirt
    # 男生衣服 > 褲子
    # 女生衣服
    # 女生衣服 > 上衣
    # 女生衣服 > 褲子

    node = sub_list[count]
    if text!="":
        new_text = text+ f" > {node["display_name"].strip()}"
    else:
        new_text = text+ f"{node["display_name"].strip()}"
    print(node["display_name"])


    # 遞迴
    if node["has_children"]==False:
        leaf_list.append(new_text)
    else:
        build_tree(new_text,node["children"],0)   
    if count+1 <len(sub_list):
        build_tree(text,sub_list,count+1)
build_tree("",data,0)        
print(leaf_list)
"""
error_list=[]
def error_check(text,sub_list,count):
    node = sub_list[count]
    if text!="":
        new_text = text+ f" > {node["display_name"].strip()}"
    else:
        new_text = text+ f"{node["display_name"].strip()}"

    # 遞迴
    if node["has_children"]==True and node.get("children") is None:
        error_list.append(new_text)
    elif node["has_children"]==True:
        error_check(new_text,node["children"],0)   
    if count+1 <len(sub_list):
        error_check(text,sub_list,count+1)
error_check("",data,0)        
print(error_list)
print(f"共 {len(error_list)} 個缺失點")
