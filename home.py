import ifcopenshell
import streamlit as st
from tools import ifchelper
import json
from pathlib import Path                                                    
from re import L                                                           
from typing import Optional                                                
import streamlit.components.v1 as components     



def callback_upload():
    session["file_name"] = session["uploaded_file"].name
    session["array_buffer"] = session["uploaded_file"].getvalue()
    session["ifc_file"] = ifcopenshell.file.from_string(session["array_buffer"].decode("utf-8"))
    session["is_file_loaded"] = True
    
    ### Empty Previous Model Data from Session State
    session["isHealthDataLoaded"] = False
    session["HealthData"] = {}
    session["Graphs"] = {}
    session["SequenceData"] = {}
    session["CostScheduleData"] = {}

    ### Empty Previous DataFrame from Session State
    session["DataFrame"] = None
    session["Classes"] = []
    session["IsDataFrameLoaded"] = False

def main():
    st.set_page_config(
        layout= "wide",
        page_title="no-BIM app",
        page_icon="📈",
    )

    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

    with open("./styles/main.css") as f:
        st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

    st.header("no-BIM app 📈")
    st.markdown("""
        view and analyze your BIM-data on the web
        and prepare you data for further processing
        trough converting it into open formats
        """)
    st.markdown("""
        just drop your IFC! 👇
            """)

    ## Add File uploader
    st.file_uploader(" ",type=['ifc'], key="uploaded_file", on_change=callback_upload)

    ## Add File Name and Success Message
    if "is_file_loaded" in session and session["is_file_loaded"]:
        filename = session.file_name
        st.sidebar.success(f"{filename} succesfully loaded!")

if __name__ == "__main__":
    session = st.session_state
    main()