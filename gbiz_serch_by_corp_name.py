import streamlit as st

import requests
import json

import time
def now_time():
    now = time.localtime()
    d = time.strftime('%Y%m%d%H%M%S', now)  # YYYYMMDDhhmmssに書式化
    return d

#for search
endpoint_url = "https://info.gbiz.go.jp/api/v1/hojin"

token = st.secrets["gbiz_token"]
st.write(token)

headers = {
            "Accept": "application/json",
            "X-hojinInfo-api-token": token
        }

token = "M3zZzZx8sFaGeQVY78PHgHCliCCIZT8M"

headers = {
            "Accept": "application/json",
            "X-hojinInfo-api-token": token
        }

def search_by_name(corp_name:str):
    params = {"name":corp_name}
    res = requests.get(
        url     = endpoint_url,
        headers = headers,
        params  = params
        )
    #json = res.json()#['hojin-infos']
    #print(json)
    #res.json()でJSONデータに変換して変数へ保存
    json_data = res.json()
    #print(len(json_data['hojin-infos']))
    #print(json_data['hojin-infos'][1])
    #取得したJSONデータが単一のJSONオブジェクトではなく
    #配列みたいになっているときはfor文と組み合わせてやるとよし。

    return_list =[]

    #print(json_data["message"])

    if json_data["message"] !=  "200 - OK.":
        result = {"status":json_data["message"], "body":""}
        
    else:
        for i in range(len(json_data['hojin-infos'])):

            #print(json_data['hojin-infos'][0]["name"])
            return_dic= {
           'search_id'         : "",
            'name'              : "",
            'location'          : "",
            'corporate_number'  : "",
            "update_date"       : ""
            }

            return_dic["search_id"]         = str(now_time()) + "_" + str(i)
            return_dic["name"]              = json_data['hojin-infos'][i]["name"]
            return_dic["location"]          = json_data['hojin-infos'][i]["location"]
            return_dic["corporate_number"]  = json_data['hojin-infos'][i]["corporate_number"]
            return_dic["update_date"]       = json_data['hojin-infos'][i]["update_date"]

            return_list.append(return_dic)

        result = {"status":json_data["message"], "body":json.dumps(return_list, ensure_ascii = False)}
        #result = return_list
     
    return result
   

def main():
    #print(search_by_name("株式会社スペース・アイ"))
    st.write(json.dumps(search_by_name("スペース・アイ"), ensure_ascii = False))
    st.json(search_by_name("スペース・アイ"))
    
if __name__ == '__main__':
    main()
