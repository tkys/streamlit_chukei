import streamlit as st

import requests
import json

import pandas as pd

import time

@st.cache
def now_time():
    now = time.localtime()
    d = time.strftime('%Y%m%d%H%M%S', now)  # YYYYMMDDhhmmssに書式化
    return d


### search_by_name 

endpoint_url = "https://info.gbiz.go.jp/api/v1/hojin"
token = st.secrets["gbiz_token"]
#token = "M3zZzZx8sFaGeQVY78PHgHCliCCIZT8M"
headers = {
            "Accept": "application/json",
            "X-hojinInfo-api-token": token
        }



@st.cache
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

    return res.json()

@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

#############
import streamlit as st


st.title("Search companys-info")
#sideb = st.sidebar
#check1 = sideb.button("Check or not?")
textbyuser = st.text_input("Enter some text", placeholder= "i.e. 中部経済新聞社")
check2 = st.button("Search Company-info")

#if check1:
#    st.info("Code is analyzing your text.")
#    #Your code to analyze the sentiment that only works when the button is clicked.


if check2:
    response = search_by_name(textbyuser)
    if  len(response["hojin-infos"]) == 0:     
        st.info(len(response["hojin-infos"]))
    else:
        st.text("result : " +  str(len(response["hojin-infos"])) )
        #st.info(search_by_name(textbyuser)["hojin-infos"])
        st.write(pd.DataFrame(response["hojin-infos"]))

       
        df = pd.DataFrame(response["hojin-infos"])
        csv = convert_df(df)

        st.download_button(
            "Download .csv",
            csv,
            "file.csv",
            "text/csv",
            key='download-csv'
        )
