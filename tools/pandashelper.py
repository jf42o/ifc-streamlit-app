
from pathlib import Path
import xlsxwriter
import os

def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')

CLASS = "Class"
LEVEL = "Level"

def filter_dataframe_per_class_df(dataframe, class_name_list):
    return dataframe[dataframe["Class"].isin(class_name_list)].dropna(axis=1, how="all")

def filter_dataframe_per_class_qto(dataframe, c):
    return dataframe[dataframe["Class"] == c].dropna(axis=1, how="all")

def get_total(dataframe):
    count = dataframe[CLASS].value_counts().sum()
    return count

def get_qsets_columns(dataframe):
    qset_columns = set()
    [qset_columns.add(column.split(".", 1)[0]) for column in dataframe.columns if "Qto" in column]
    return list(qset_columns) if qset_columns else None

def get_quantities(frame, quantity_set):
    columns = []
    [columns.append(column.split(".", 1)[1]) for column in frame.columns if quantity_set in column]
    columns.append("Count")
    return columns

def download_csv(file_name, dataframe):
    file_name = file_name.replace('.ifc', '.csv')
    dataframe.to_csv(file_name)

def download_excel(file_name, dataframe):
    import pandas
    file_name = file_name.replace('.ifc', '.xlsx')
    writer = pandas.ExcelWriter(f'./{file_name}', engine="xlsxwriter") ## pip install xlsxwriter
    for object_class in dataframe[CLASS].unique():
        df_class = dataframe[dataframe[CLASS] == object_class].dropna(axis=1, how="all")
        df_class.to_excel(writer, sheet_name=object_class)
    writer.save()