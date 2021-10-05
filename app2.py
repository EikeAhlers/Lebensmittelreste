# @Email:  contact@pythonandvba.com
# @Website:  https://pythonandvba.com
# @YouTube:  https://youtube.com/c/CodingIsFun
# @Project:  Lebensmittelabfall Dashboard w/ Streamlit



from re import template
import pandas as pd
import plotly  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import plotly.graph_objects as go
import datetime

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Lebensmittelabfall Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
df_kennzahlen = pd.read_excel(
        io="Lebensmittelabfall.xlsx",
        engine="openpyxl",
        sheet_name="Kennzahlen",
)

@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io="Lebensmittelabfall.xlsx",
        engine="openpyxl",
        sheet_name="Abfalldokumentation",
  #      skiprows=0,
  #      usecols="A:Q",
  #      nrows=1000,
    )
    # Add 'hour' column to dataframe
    
    df['date'] = df['Datum'].dt.date
    
    return df



df = get_data_from_excel()




#Zeitraumfilter
date = st.sidebar.date_input('Startdatum', datetime.date(2021,8,23))
date2 = st.sidebar.date_input('Enddatum', datetime.date(2021,9,23))
mask = (df['date'] >= date) & (df['date'] <= date2)
df = df.loc[mask]
zeitraum=date2-date
st.sidebar.write('Zeitraum: ',zeitraum)   


# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
BU = st.sidebar.multiselect(
    "Select the BU:",
    options=df["BU"].unique(),
    default=df["BU"].unique()
)
Symptom = st.sidebar.multiselect(
    "Wähle das Symptom aus:",
    options=df["Symptom"].unique(),
    default=df["Symptom"].unique(),
)
Grund = st.sidebar.multiselect(
    "Select the Grund:",
    options=df["Grund"].unique(),
    default=df["Grund"].unique()
)
df_selection = df.query(
   "BU == @BU & Symptom ==@Symptom & Grund == @Grund"
)
#Sunburst Gründe
#Definition Variable
a = df_selection["BU"]
b = df_selection["Symptom"]
c = df_selection["Grund"]
d = df_selection["Produktgruppe"]
e = df_selection["Produktname"]
f = df_selection["Datum"]
g = df_selection["genauer Grund"]
z = df_selection["filter_a"]
zz = df_selection["filter_b"]
zzz = df_selection["filter_c"]

menge = df_selection["Menge"]
df_sunburst = pd.DataFrame(
    dict(a=a, b=b, c=c, d=d , e=e ,f=f, g=g , z=z , zz=zz , zzz=zzz ,menge=menge)
)

gesamt_grund = px.sunburst(df_sunburst, path=['z', 'b', 'c', 'g','d','e','f'], values="menge",
hover_name="menge",
maxdepth=2
)
gesamt_grund.update_traces(textinfo='label+percent entry')
gesamt_grund.update_layout(
    margin=dict(l=20, r=350, t=40, b=40)
)


bu_grund = px.sunburst(df_sunburst, path=['zz' , 'a', 'b', 'c', 'd', 'e','f'], values="menge",
hover_name="menge",
#hover_data={'all':False},
maxdepth=2
#template="ggplot",
)
bu_grund.update_traces(textinfo='label+percent entry')
bu_grund.update_layout(
    margin=dict(l=20, r=350, t=40, b=40)
)

produkte = px.sunburst(df_sunburst, path=['zzz', 'd', 'e','f'], values="menge",
hover_name="menge",
#hover_data={'all':False},
maxdepth=2
#template="ggplot",
)
produkte.update_traces(textinfo='label+percent entry')
produkte.update_layout(
    margin=dict(l=20, r=350, t=40, b=40)
)







# ---- MAINPAGE ----
st.title(":bar_chart: Lebensmittelabfall Dashboard")
st.markdown("##")

# TOP KPI's
Menge_Lebensmittelabfall = int(df_selection["Menge"].sum())
glmabfall_bu1 = df_kennzahlen["Gesamtlebensmittelabfallquote"].values[0]
glmabfall_bu2 = df_kennzahlen["Gesamtlebensmittelabfallquote"].values[1]
glmabfall_bu3 = df_kennzahlen["Gesamtlebensmittelabfallquote"].values[2]
glmabfall_bu4 = df_kennzahlen["Gesamtlebensmittelabfallquote"].values[3]

mlmabfall_bu1 = df_kennzahlen["Gesamtlebensmittelabfallquote"].values[0]
mlmabfall_bu2 = df_kennzahlen["Gesamtlebensmittelabfallquote"].values[1]
mlmabfall_bu3 = df_kennzahlen["Gesamtlebensmittelabfallquote"].values[2]
mlmabfall_bu4 = df_kennzahlen["Gesamtlebensmittelabfallquote"].values[3]


#average_rating = round(df_selection["Rating"].mean(), 1)
#star_rating = ":star:" * int(round(average_rating, 0))
#average_sale_by_transaction = round(df_selection["Menge"].mean(), 2)

uebersicht = px.pie(df_selection,
            values = "Menge",
            names = "BU",
)

uebersicht.update_traces(
    textposition = "inside",
    textinfo = "percent+label"
)

uebersicht.update_layout(
    title_font_size = 42
)
uebersicht.update_layout(
    margin=dict(l=20, r=300, t=20, b=0)
)

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Menge Lebensmittelabfall:")
with right_column:
    st.subheader("Hier stehen zukünftig die KPIs")
    

st.markdown("""---""")

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Aufteilung BUs")
    st.plotly_chart(bu_grund)
with middle_column:
    st.subheader("Symptome und Gründe")
    st.plotly_chart(gesamt_grund)
with right_column:
    st.subheader("Produktgruppen")    
    st.plotly_chart(produkte)

st.markdown("""---""")

# Lebensmittelabfall BY Symptom [BAR CHART]
Lebensmittelabfall_by_product_line = (
    df_selection.groupby(by=["Symptom"]).sum()[["Menge"]].sort_values(by="Menge")
)
fig_product_Lebensmittelabfall = px.bar(
    Lebensmittelabfall_by_product_line,
    x="Menge",
    y=Lebensmittelabfall_by_product_line.index,
    orientation="h",
    title="<b>Symptome des Lebensmittelabfalls</b>",
    color_discrete_sequence=["#0083B8"] * len(Lebensmittelabfall_by_product_line),
    template="plotly_white",
)
fig_product_Lebensmittelabfall.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

fig_product_Lebensmittelabfall.update_traces(
    
    selector=dict(type='bar')
)

# Lebensmittelabfall BY Symptom [BAR CHART]
produktgruppe_chart = (
    df_selection.groupby(by=["Produktgruppe"]).sum()[["Menge"]].sort_values(by="Menge")
)
fig_produktgruppe_chart = px.bar(
    produktgruppe_chart,
    x="Menge",
    y=produktgruppe_chart.index,
    orientation="h",
    title="<b>Produktegruppen</b>",
    color_discrete_sequence=["#0083B8"] * len(Lebensmittelabfall_by_product_line),
    template="plotly_white",
)
fig_produktgruppe_chart.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

fig_produktgruppe_chart.update_traces(
   
    selector=dict(type='bar')
)



left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_produktgruppe_chart, use_container_width=True)
right_column.plotly_chart(fig_product_Lebensmittelabfall, use_container_width=True)









    













raw_data = df_selection.replace({'nein': ""})
raw_data

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
