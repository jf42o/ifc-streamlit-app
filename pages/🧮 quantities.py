import streamlit as st
from tools import ifchelper
from tools import pandashelper
from tools import graph_maker

session = st.session_state


def initialize_session_state():
    session["DataFrame"] = None
    session["Classes"] = []
    session["IsDataFrameLoaded"] = False

def load_data():
    if "ifc_file" in session:
        session["DataFrame"] = get_ifc_pandas()
        session.Classes = session.DataFrame["Class"].value_counts().keys().tolist()
        session["IsDataFrameLoaded"] = True

def get_ifc_pandas():
    data, pset_attributes = ifchelper.get_objects_data_by_class(
        session.ifc_file, 
        "IfcBuildingElement"
    )
    frame = ifchelper.create_pandas_dataframe(data, pset_attributes)
    return frame

def download_csv_qto():
    pandashelper.download_csv(session.file_name,session["filtered_frame_qto"])

def download_csv_df():
    pandashelper.download_csv(session.file_name,session["filtered_frame_df"])

def download_excel_qto():
    pandashelper.download_excel(session.file_name,session["filtered_frame_qto"])

def download_excel_df():
    pandashelper.download_excel(session.file_name,session["filtered_frame_df"])

def execute():

    st.set_page_config(
        layout="wide",
        initial_sidebar_state="expanded",
        page_title="quantities",
        page_icon="📊",
    )
    
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """

    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

   #with open("./styles/main2.css") as f:
        #st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

    st.header(" 🧮 model quantities")
    if not "IsDataFrameLoaded" in session:
        initialize_session_state()
    if not session.IsDataFrameLoaded:
        load_data()
    if session.IsDataFrameLoaded:    
        tab1, tab2 = st.tabs(["dataframe", "quantity takeoff"])
        with tab1:
            ## DATAFRAME REVIEW  
            st.header("dataframe")
            class_selector_dataframe = st.multiselect("select all classes", session.Classes, default = session.Classes, key="class_selector_dataframe")
            session["filtered_frame_df"] = pandashelper.filter_dataframe_per_class_df(session.DataFrame, class_selector_dataframe)
            st.write(session["filtered_frame_df"])
            st.button("📄 download csv", key="download_csv_dataframe", on_click=download_csv_df)
            st.button("📗 download excel", key="download_excel_dataframe", on_click=download_excel_df)
        with tab2:
            row2col1, row2col2 = st.columns(2)
            with row2col1:
                if session.IsDataFrameLoaded:
                    class_selector_qto = st.selectbox("select class", session.Classes, key="class_selector_qto")
                    session["filtered_frame_qto"] = pandashelper.filter_dataframe_per_class_qto(session.DataFrame, class_selector_qto)
                    session["qtos"] = pandashelper.get_qsets_columns(session["filtered_frame_qto"])
                    if session["qtos"] is not None:
                        qto_selector = st.selectbox("select Quantity Set", session.qtos, key='qto_selector')
                        quantities = pandashelper.get_quantities(session.filtered_frame_qto, qto_selector)
                        st.selectbox("select quantity", quantities, key="quantity_selector_qto")
                        st.radio('split per', ['Level', 'Type'], key="split_options")
                    else:
                        st.warning("no quantities to look at !")
            ## DRAW FRAME
            with row2col2: 
                if "quantity_selector" in session and session.quantity_selector == "Count":
                    total = pandashelper.get_total(session.filtered_frame_qto)
                    st.write(f"The total number of {session.class_selector_qto} is {total}")
                else:
                    if session.qtos is not None:
                        st.subheader(f"{session.class_selector_qto} {session.quantity_selector}")
                        graph = graph_maker.load_graph(
                            session.filtered_frame_qto,
                            session.qto_selector,
                            session.quantity_selector,
                            session.split_options                            
                        )
                        st.plotly_chart(graph)
            st.button("📄 download csv", key="download_csv_qto", on_click=download_csv_qto)
            st.button("📗 download excel", key="download_excel_qto", on_click=download_excel_qto)
    else: 
        st.header("please load a file from the home menu")
    
execute()