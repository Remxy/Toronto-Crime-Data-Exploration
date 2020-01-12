import streamlit as st
import pandas as pd 
import plotly_express as px 
import folium 
from folium.plugins import HeatMap
import seaborn as sns

# Get the data from url and request it as json file
@st.cache(persist=True, suppress_st_warning=True)
def load_data():
    df = pd.read_csv('Toronto_Crime_MCI_2014_to_2018.csv')
        #"https://services.arcgis.com/S9th0jAJ7bqgIRjw/arcgis/rest/services/MCI_2014_to_2018/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json"
    df["reporteddate"] = pd.to_datetime(
        df["reporteddate"], infer_datetime_format=True)
    df["Day"] = df["reporteddate"].dt.day
    df["Month"] = df["reporteddate"].dt.month
    df["Hour"] = df["reporteddate"].dt.hour
    return df

@st.cache(persist=True, suppress_st_warning=True)
def display_map(df):
    st.subheader(" Displaying Point based map")
    px.set_mapbox_access_token(
        "pk.eyJ1Ijoic2hha2Fzb20iLCJhIjoiY2plMWg1NGFpMXZ5NjJxbjhlM2ttN3AwbiJ9.RtGYHmreKiyBfHuElgYq_w")
    fig = px.scatter_mapbox(df, lat="Y", lon="X", color="MCI", zoom=10)
    return fig


#Map Visualizations with Folium

def generateBaseMap(default_location=[43.741667, -79.373333], default_zoom_start=11):
    base_map = folium.Map(location=default_location, control_scale=True, zoom_start=default_zoom_start)
    return base_map


def heat_map(df):
    df = df.loc[0:40000, :] # Reducing data size so it runs faster
    locs = zip(df.Y, df.X)
    m = folium.Map([43.741667, -79.373333], tiles='stamentoner', zoom_start=11)
    HeatMap(locs).add_to(m)
    return st.markdown(m._repr_html_(), unsafe_allow_html=True)

def main():
    df_data = load_data()
    st.header("Toronto Crimes Data Exploration")
    st.subheader("Visualization using Streamlit")
    st.image("Crime_Scene.jpg", width=1000)
    #st.image("https://www.balcanicaucaso.org/var/obc/storage/images/articoli-da-pubblicare-2/kosovo-in-aumento-rapine-e-reati-violenti-192124/1860637-9-eng-GB/Kosovo-robberies-and-violent-crimes-on-the-rise.jpg", width=800)
    if st.checkbox("Tick Box to show first rows of the data & shape of the data"):
        st.write(df_data.head())
        st.write(df_data.shape)
    
    st.plotly_chart(display_map(df_data))

    dataviz_choice = st.sidebar.selectbox("Select Data Visualization",
                                          ["None", "Heatmap", "Countplot", "DayofWeek", "Premises Type", "Police Division", "Reported Year", "Reported Month"])
    if dataviz_choice == "Countplot":
        st.subheader("Countplot")
        sns.countplot("MCI", data=df_data)
        st.pyplot()
        
    elif dataviz_choice == "DayofWeek":
        st.subheader("DayofWeek")
        sns.countplot(y="reporteddayofweek", data=df_data)
        st.pyplot()    

    elif dataviz_choice == "Hood_ID":
        st.subheader("Hood_ID")
        sns.countplot(y="Hood_ID", data=df_data)
        st.pyplot() 
        
    elif dataviz_choice == "Offence":
        st.subheader("Offence")
        sns.countplot(y="offence", data=df_data, palette="Set3", hue = "offence" )
          
        #st.set_xticklabels(st.get_xticklabels(), rotation=90)
        st.pyplot() 
        
    elif dataviz_choice == "Premises Type":
        st.subheader("Premises Type")
        sns.countplot(y="premisetype", data=df_data)
        st.pyplot()
    
    elif dataviz_choice == "Police Division":
        st.subheader("Police Division")
        sns.countplot("Division", data=df_data)
        st.pyplot()
        
    elif dataviz_choice == "Reported Year":
        st.subheader("Reported Year")
        sns.countplot(y= "reportedyear", data=df_data)
        st.pyplot()
        
    elif dataviz_choice == "Reported Month":
        st.subheader("Reported Month")
        sns.countplot(y= "reportedmonth", data=df_data)
        st.pyplot()
        
    elif dataviz_choice == "Heatmap":
        st.subheader("Heatmap")
        heat_map(df_data)
        

if __name__ == "__main__":
    main()