import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
import textwrap
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import argparse


from elsevier_fetch import ElsevierFetcher



st.set_page_config(page_title='Elsevier Fetcher',layout='wide')
#按钮样式定义
st.markdown("""
<style>
.stButton>button {
    color: white;
    background-color: red;
    border: none;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 24px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)
#table样式定义
st.markdown("""
<style>
table {
    font-family: Arial, sans-serif;
    font-size: 20px;
    border-collapse: collapse;
    width: 100%;
}
td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 10px;
}
tr:nth-child(even) {
    background-color: #dddddd;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
h1 {
    color: red;
    font-size: 80px;
}
.st-ay {
    font-size: 1.5rem;
}  
</style>
""", unsafe_allow_html=True)



st.title('Elsevier Fetcher')

def app():
    col1, col2 = st.columns(2)

    with col1:
        # 创建一个输入框，用于输入期刊名称
        st.markdown("<p style='font-size: 28px; font-weight: bold;'>请输入要爬取的期刊名称：</p>", unsafe_allow_html=True)
        journal = st.text_input('')
        journal_fetcher = ElsevierFetcher(journal)
    
        if 'clicked' not in st.session_state:
            st.session_state.clicked = False
        def click_button():
            st.session_state.clicked = True

        st.button('获取期刊',on_click=click_button)

        Elsevier_Data = {'1':['landscape-and-urban-planning','cities','urban-forestry-and-urban-greening','computers-environment-and-urban-systems'],
                         '2':['building-and-environment','sustainable-cities-and-society','urban-climate','remote-sensing-of-environment']}
        st.table(Elsevier_Data)
    
    with col2:
        col3, col4 = st.columns(2)
        with col3:
            st.markdown(f"<p style='font-size: 28px; font-weight: bold;'>《{journal}》all issues</p>", unsafe_allow_html=True)
            img = None 
            if st.session_state.clicked:
                df ,img = journal_fetcher.fetch_journal()
                df= df[3:]
                st.markdown("<p style='font-size: 18px; font-weight: bold;'>{}</p>".format('<br>'.join(df)), unsafe_allow_html=True)
        with col4:
            if img is not None:
                st.image(img, use_column_width=True)

    # 创建一个输入框，用于输入卷号
    st.markdown("<p style='font-size: 28px; font-weight: bold;'>请输入要爬取的卷号：</p>", unsafe_allow_html=True)
    volume = st.text_input(' ')

    if st.button('获取文章'):
        df,df2 = journal_fetcher.fetch_articles(volume)

        #AgGrid修饰表格显示
        js_code = """
        function(params) {
            if (params.node.rowIndex % 2 === 0) {
                return {'backgroundColor': 'rgb(245, 255, 250)'}
            } else {
                return {'backgroundColor': 'rgb(255, 255, 255)'}
            }
        }
        """
        js_func = JsCode(js_code)

        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_grid_options(getRowStyle=js_func,domLayout='autoHeight')
        
        
        gb.configure_column(headerName="标题", field= "标题", flex= 0.8,  cellStyle={'fontWeight': 'bold', 'fontSize': '20px', 'color': 'black', 'whiteSpace': 'normal'}, autoHeight=True,resizable=True,wrapText=True)
        gb.configure_column('关键词', flex= 0.7, cellRenderer='agTextCellRenderer', cellStyle={'fontSize': '18px', 'color': 'black', 'whiteSpace': 'pre-wrap'}, autoHeight=True,resizable=True,wrapText=True)
        gb.configure_column('亮点', flex= 1.5, cellRenderer='agTextCellRenderer', cellStyle={'fontSize': '18px', 'color': 'black', 'whiteSpace': 'pre-wrap'}, autoHeight=True,resizable=True,wrapText=True)
        gb.configure_column('摘要', flex= 3, cellStyle={'fontSize': '18px', 'color': 'black', 'whiteSpace': 'normal'}, autoHeight=True,resizable=True,wrapText=True)
        gb.configure_column('链接', flex= 0.5, cellStyle={'fontSize': '18px', 'color': 'black', 'whiteSpace': 'normal'}, autoHeight=True,resizable=True,wrapText=True)
        
        gridOptions = gb.build()
        AgGrid(df, gridOptions=gridOptions, allow_unsafe_jscode=True, enable_browser_side_modules=True)
        
        if df2 != []:
            AgGrid(df2, gridOptions=gridOptions, allow_unsafe_jscode=True)
        else:
            st.text('没有第二页')

if __name__ == '__main__':
    app()
