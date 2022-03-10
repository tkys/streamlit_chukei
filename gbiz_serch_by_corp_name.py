import streamlit as st

import requests
import json


#for search
endpoint_url = "https://info.gbiz.go.jp/api/v1/hojin"

token = st.secrets["gbiz_token"]
st.write(token)

headers = {
            "Accept": "application/json",
            "X-hojinInfo-api-token": token
        }

def search_by_name(corp_name:str):
    params = {"name":corp_name}
    res = requests.get(
        url = endpoint_url,
        headers = headers,
        params = params
        )
    #json = res.json()#['hojin-infos']
    #print(json)
    #res.json()でJSONデータに変換して変数へ保存
    json_data = res.json()
    #print(json_data['hojin-infos'])
    #取得したJSONデータが単一のJSONオブジェクトではなく
    #配列みたいになっているときはfor文と組み合わせてやるとよし。
    return_dic= {
        'name': "",
        'location': "",
        'corporate_number': "",
        "update_date":""
        }
    #print(json_data["message"])
    for jsonObj in json_data['hojin-infos']:
        #print(jsonObj["corporate_number"],jsonObj["name"],jsonObj["location"])        
        return_dic["name"] = jsonObj["name"]
        return_dic["location"] = jsonObj["location"]
        return_dic["corporate_number"] = jsonObj["corporate_number"]
        return_dic["update_date"] = jsonObj["update_date"]
    
    return return_dic#json_data['hojin-infos']
   

def main():
    #print(search_by_name("スペース・アイ株式会社"))
    st.write(search_by_name("スペース・アイ株式会社"))
    
    
if __name__ == '__main__':
    main()
