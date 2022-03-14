import requests
import pandas as pd
import streamlit as st
#from annotated_text import annotated_text

#text_input = "10日イオンモールは、名古屋市熱田区の商業施設「イオンモール熱田」で、開業以来初の全面改装を実施すると発表した。今春から秋にかけて、専門店約30店を刷新する。秋に診療やリハビリといった総合医療施設を導入予定で、地域住民の生活に密着した商業.."
@st.cache
def req(query,TARGET):
    """ requests . that use qiita search api
    >>> 'title' in req('python')
    True
    >>> 'totle' in req('python')
    False
    """
    q = {'input_text':  query}
    r = requests.get(
        url = 'https://pjnr7zdda3.execute-api.ap-northeast-1.amazonaws.com/dev/comprehend/',
        params=q
        )
    #print(r.json()['response'])
    #return list(r.json()['response'][0].keys())

    #return r.json()['response'][0]['Type']


    # Filter python objects with list comprehensions
    input_dict =  r.json()['response']
    #print(input_dict)
    
    #output_dict = [x for x in input_dict if x['Type'] == ["ORGANIZATION"] ] # ORGANIZATION だけ抽出
    output_dict = [x for x in input_dict if x['Type'] in TARGET ] # 選択対象抽出

    response = output_dict

    return response

@st.cache
def convert_df_to_csv(df):
    return df.to_csv().encode('utf-8')

def res_2_df_csvdownload_button(response):
    df = pd.DataFrame(response)
    csv = convert_df_to_csv(df)
    st.download_button(
        "Download .csv",
        csv,
        "file.csv",
        "text/csv",
        key='download-csv'
    )

st.title("Pick up organizations from News📝")
text_input = st.text_input("Enter some text", placeholder= "i.e. 10日イオンモールは、名古屋市熱田区の商業施設「イオンモール熱田」で、開業以来初の全面改装を実施すると発表した。今春から秋にかけて、専門店約30店を刷新する。")

if text_input != "":
    st.subheader("input_text📝")
    st.info(text_input)

select_entities = st.multiselect(
    'Choose entities you looking for ',
    ['COMMERCIAL_ITEM', 'DATE', 'EVENT', 'LOCATION', 'ORGANIZATION', 'PERSON', 'QUANTITY', 'TITLE', 'OTHER'],
    ['ORGANIZATION'])  #  default only 'ORGANIZATION'

#st.text(select_entities)

check = st.button("Pick-up Entities🔎")


if check:
    TARGET = select_entities
    #st.info("Now analyzing your text...")
    
    # call api to amazon comprehend  & filtering keywords with in multipul setelctor 
    response = req(text_input,TARGET)
    #print(response)
    #st.info(response)

    # show result 
    st.text("result : " +  str( len(response) )  )
    st.write(pd.DataFrame(response))

    #input_dict = req(text_input)
    #str_position_dic = [x for x in input_dict if x['BeginOffset'] == TARGET ] # ORGANIZATION だけ抽出

    #str_position_dic = []
    #for i in response:
    #    str_position_dic.append(i['BeginOffset'])
    #    str_position_dic.append(i['EndOffset'])
    
    # show csv download button
    res_2_df_csvdownload_button(response)
    
