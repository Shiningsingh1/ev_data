#import packages
import streamlit as st
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from PIL import Image
import seaborn as sns
import numpy as np
from statsmodels.formula.api import ols
import streamlit.components.v1 as components
import geopandas as gdp
import folium
import geopandas.tools
from shapely.geometry import Point
import shapely.speedups
from operator import index

#title
st.markdown("<h1 style='text-align: center; color: grey;'>🔌Dashboard EV🔌</h1>", unsafe_allow_html=True)

#create header
components.html(
    """
        <div style="text-align: center">
            <a href="https://opendata.rdw.nl/Voertuigen/Elektrische-voertuigen/w4rt-e856" target="_blank" class="button">Link naar de gebruikte data set van de RDW🔗</a>
            </div>
    """, height= 30
)

#image
image = Image.open('HVA-logo.jpg')
st.image(image)
st.markdown("<h4 style='text-align: center; color: grey;'>Opdracht 2 gemaakt door: Jaskirat, Thijs, Maureen en Dinand</h4>", unsafe_allow_html=True)

#import dataset
ev_data = pd.read_csv('ev_app_data.csv')
url_data = pd.read_csv('url_data.csv',index_col=[0])
lp_data = pd.read_csv('laadpaaldata_app.csv', index_col=[0])
geo = gdp.read_file('Provinciess.json') #json-file


#visualisations
def display_ev_data():
    #defining values
    ev_user = ev_data
    _id = 0
    tesla= ev_data[ev_data["Merk"] == "TESLA"]
    tesla = tesla[tesla['Catalogusprijs'] <=215000]
    prijs_datum = ols("Catalogusprijs ~ Jaartallen", data=tesla).fit()
    explanatory=pd.DataFrame({'Jaartallen': np.arange(2012, 2025)})
    prediction=explanatory.assign(Catalogusprijs=prijs_datum.predict(explanatory))


    see_data = st.expander('Orginele data 👇')
    with see_data:
        st.dataframe(data=ev_data)
    if st.sidebar.checkbox("Sliders menu🎚️"):
     _id = st.sidebar.slider('Aantal elektrische voertuigen', 1 , 307949, 150000)
     ev_user = ev_data[ev_data['slider_number'] <= _id]
     see_user_data = st.expander('Data na selectie👇')
     with see_user_data:
        st.dataframe(data=ev_user)
   
    #KPI's
    kpi1, kpi2 = st.columns(2)
    _max_weight = round(ev_data['Massa rijklaar'].sum()/ev_data['slider_number'].max(),1)
    if _id > 0 :
        _weight_user = round(ev_user['Massa rijklaar'].sum()/ev_user['slider_number'].max(),1)
    else  :
        _weight_user = round(ev_data['Massa rijklaar'].sum()/ev_data['slider_number'].max(),1)        
    kpi1.metric(label = "Gemiddelde massa",
           value = _weight_user,
             delta = round(_weight_user-_max_weight)) 

    _max_price = round(ev_data['Catalogusprijs'].sum()/ev_data['slider_number'].max(),1)
    if _id > 0:
        _price_user = round(ev_user['Catalogusprijs'].sum()/ev_user['slider_number'].max(),1)
    else  :
        _price_user = round(ev_data['Catalogusprijs'].sum()/ev_data['slider_number'].max(),1)
    kpi2.metric(label = "Gemiddelde catalogusprijs",
           value = _price_user,
           delta = round(_price_user-_max_price))
    
    #vis1
    inrichting_color_map = {'stationwagen': 'aliceblue', 'MPV' : 'brown', 'sedan' : 'cyan', 'Niet geregistreerd' : 'darkblue', 'cabriolet' : 'yellowgreen',
                        'coupe' : 'pink', 'hatchback' : 'yellow', 'kampeerwagen' : 'lime',
                        'voor rolstoelen toegankelijk voertuig' : 'Black', 'niet nader aangeduid' : 'red',
                        'speciale groep' : 'green', 'gesloten opbouw' : 'purple', 'lijkwagen' : 'turquoise'}

    fig = px.histogram(data_frame= ev_user, x="Inrichting",                                                                                                             
                  title= "Aantal auto's per inrichting",                       
                  color="Inrichting",                                               
                  color_discrete_map = inrichting_color_map,
                  width=1800,
                  height=1000)                        
    fig.update_layout()                                                             
    st.plotly_chart(fig,use_container_width=True)
    
    #Vis 2
    fig = px.scatter(tesla, x="Jaartallen", y="Catalogusprijs", trendline="ols")
    st.plotly_chart(fig,use_container_width=True)

    #vis_dataframe
    col1, col2, col3 = st.columns(3)
    with col1:
         st.header("")
    with col2:
     st.dataframe(prediction)
    with col3:
     st.header("")

    #vis3
    fig=plt.figure()
    sns.regplot(x='Jaartallen', y='Catalogusprijs', ci=None, data=tesla)
    sns.scatterplot(x='Jaartallen', y='Catalogusprijs', data=prediction, color='red', marker='s')
    st.write(fig)



def display_opencharge_map():
    see_data = st.expander('Data 👇')
    with see_data:
        st.dataframe(data=url_data)
   
    #creating provinces
    nh = pd.DataFrame(data=url_data, columns=["Latitude", "Longitude", "Provincie", "Point", "Town/City"])
    nh = nh.loc[nh["Provincie"] == "Noord-Holland"]

    zh = pd.DataFrame(data=url_data, columns=["Latitude", "Longitude", "Provincie", "Point",  "Town/City"])
    zh = zh.loc[zh["Provincie"] == "Zuid-Holland"]

    drenthe = pd.DataFrame(data=url_data, columns=["Latitude", "Longitude", "Provincie", "Point",  "Town/City"])
    drenthe = drenthe.loc[drenthe["Provincie"] == "Drenthe"]

    flevoland = pd.DataFrame(data=url_data, columns=["Latitude", "Longitude", "Provincie", "Point",  "Town/City"])
    flevoland = flevoland.loc[flevoland["Provincie"] == "Flevoland"]

    friesland = pd.DataFrame(data=url_data, columns=["Latitude", "Longitude", "Provincie", "Point",  "Town/City"])
    friesland = friesland.loc[friesland["Provincie"] == "Fryslân"]

    gelderland = pd.DataFrame(data=url_data, columns=["Latitude", "Longitude", "Provincie", "Point",  "Town/City"])
    gelderland = gelderland.loc[gelderland["Provincie"] == "Gelderland"]

    groningen = pd.DataFrame(data=url_data, columns=["Latitude", "Longitude", "Provincie", "Point",  "Town/City"])
    groningen = groningen.loc[groningen["Provincie"] == "Groningen"]

    limburg = pd.DataFrame(data=url_data, columns=["Latitude", "Longitude", "Provincie", "Point",  "Town/City"])
    limburg = limburg.loc[limburg["Provincie"] == "Limburg"]

    noordb = pd.DataFrame(data=url_data, columns=["Latitude", "Longitude", "Provincie", "Point",  "Town/City"])
    noordb = noordb.loc[noordb["Provincie"] == "Noord-Brabant"]

    overijssel = pd.DataFrame(data=url_data, columns=["Latitude", "Longitude", "Provincie", "Point",  "Town/City"])
    overijssel = overijssel.loc[overijssel["Provincie"] == "Overijssel"]

    utrecht = pd.DataFrame(data=url_data, columns=["Latitude", "Longitude", "Provincie", "Point",  "Town/City"])
    utrecht = utrecht.loc[utrecht["Provincie"] == "Utrecht"]

    zeeland = pd.DataFrame(data=url_data, columns=["Latitude", "Longitude", "Provincie", "Point",  "Town/City"])
    zeeland = zeeland.loc[zeeland["Provincie"] == "Zeeland"]

    # creating figure
    m= folium.Map(location=[52.110298852802124, 5.180856142933691], zoom_start=9)
    folium.TileLayer('cartodbpositron').add_to(m) #Expliciete achtergrond

    a = folium.FeatureGroup(name="Noord-Holland", show=False).add_to(m)
    b = folium.FeatureGroup(name="Zuid-Holland", show=False).add_to(m)
    c = folium.FeatureGroup(name="Groningen", show=False).add_to(m)
    d = folium.FeatureGroup(name="Flevoland", show=False).add_to(m)
    e = folium.FeatureGroup(name="Friesland", show=False).add_to(m)
    f = folium.FeatureGroup(name="Overijssel", show=False).add_to(m)
    g = folium.FeatureGroup(name="Zeeland", show=False).add_to(m)
    h = folium.FeatureGroup(name="Drenthe", show=False).add_to(m)
    i = folium.FeatureGroup(name="Limburg", show=False).add_to(m)
    j = folium.FeatureGroup(name="Noord-Brabant", show=False).add_to(m)
    k = folium.FeatureGroup(name="Gelderland", show=False).add_to(m)
    l = folium.FeatureGroup(name="Utrecht").add_to(m)

    folium.Choropleth(
        geo_data=geo,
        data=url_data,
        columns=["Provincie", "slider_number"],
        key_on="feature.type",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=1.5,
        nan_fill_color = "greenyellow",
        Highlight= True,
        smooth_factor=0,
        overlay=True).add_to(m)



    for index, nh in nh.iterrows(): 
        location=[nh['Latitude'], nh['Longitude']]
        a.add_child(folium.Marker(location,
                        popup=nh["Town/City"],
                        tooltip='Klik hier om de locatie van laadpaal te zien').add_to(m))  

    
    for index, zh in zh.iterrows(): 
        location=[zh['Latitude'], zh['Longitude']]
        b.add_child(folium.Marker(location,
                        popup=zh["Town/City"],
                        tooltip='Klik hier om de locatie van laadpaal te zien').add_to(m))  
    
    
    for index, groningen in groningen.iterrows(): 
        location=[groningen['Latitude'], groningen['Longitude']]
        c.add_child(folium.Marker(location,
                        popup=groningen["Town/City"],
                        tooltip='Klik hier om de locatie van laadpaal te zien').add_to(m))  
    
    for index, flevoland in flevoland.iterrows(): 
        location=[flevoland['Latitude'], flevoland['Longitude']]
        d.add_child(folium.Marker(location,
                        popup=flevoland["Town/City"],
                        tooltip='Klik hier om de locatie van laadpaal te zien').add_to(m))  
    
    for index, friesland in friesland.iterrows(): 
        location=[friesland['Latitude'], friesland['Longitude']]
        e.add_child(folium.Marker(location,
                        popup=friesland["Town/City"],
                        tooltip='Klik hier om de locatie van laadpaal te zien').add_to(m)) 
    
    
    for index, overijssel in overijssel.iterrows(): 
        location=[overijssel['Latitude'], overijssel['Longitude']]
        f.add_child(folium.Marker(location,
                       popup=overijssel["Town/City"],
                       tooltip='Klik hier om de locatie van laadpaal te zien').add_to(m))  
    
    for index, zeeland in zeeland.iterrows(): 
        location=[zeeland['Latitude'], zeeland['Longitude']]
        g.add_child(folium.Marker(location,
                        popup=zeeland["Town/City"],
                        tooltip='Klik hier om de locatie van laadpaal te zien').add_to(m))  
    
    for index, drenthe in drenthe.iterrows(): 
        location=[drenthe['Latitude'], drenthe['Longitude']]
        h.add_child(folium.Marker(location,
                        popup=drenthe["Town/City"],
                        tooltip='Klik hier om de locatie van laadpaal te zien').add_to(m)) 
    
    for index, limburg in limburg.iterrows(): 
        location=[limburg['Latitude'], limburg['Longitude']]
        i.add_child(folium.Marker(location,
                        popup=limburg["Town/City"],
                        tooltip='Klik hier om de locatie van laadpaal te zien').add_to(m)) 

    for index, noordb in noordb.iterrows(): 
        location=[noordb['Latitude'], noordb['Longitude']]
        j.add_child(folium.Marker(location,
                        popup=noordb["Town/City"],
                        tooltip='Klik hier om de locatie van laadpaal te zien').add_to(m)) 


    for index, gelderland in gelderland.iterrows(): 
        location=[gelderland['Latitude'], gelderland['Longitude']]
        k.add_child(folium.Marker(location,
                        popup=gelderland["Town/City"],
                        tooltip='Klik hier om de locatie van laadpaal te zien').add_to(m)) 
    

    for index, utrecht in utrecht.iterrows(): 
        location=[utrecht['Latitude'], utrecht['Longitude']]
        l.add_child(folium.Marker(location,
                        popup=utrecht["Town/City"],
                        tooltip='Klik hier om de locatie van laadpaal te zien').add_to(m)) 
                
    folium.LayerControl(position='bottomleft', collapsed=False).add_to(m)

    st_data = st_folium(m, width =725)
    

def display_charge_data():
    lp_user=lp_data
    st.write("""#####  Hier de plot\'s""")
    see_data = st.expander('Orginele data 👇')
    with see_data:
        st.dataframe(data=lp_data)
    if st.sidebar.checkbox("Sliders menu🎚️"):
      _id = st.sidebar.slider('Aantal elektrische voertuigen', 1 , 10188, 5000)
      lp_user = lp_data[lp_data['slider_number'] <= _id]
      see_user_data = st.expander('Data na selectie👇')
      with see_user_data:
        st.dataframe(data=lp_user)
    #vis 1    
    fig = plt.subplots(figsize=(12, 4))
    plt.xlabel("Time while Connected (min)") 
    plt.ylabel("Usage per month in kWh")
    lp_user.groupby(lp_user['Month'])["TotalEnergy_kWh"].sum().plot(kind='bar', rot=0)
    st.pyplot(fig=plt)

    #vis2 
    median = round((lp_user['ChargeTime_min'].median()),1)
    mean= round((lp_user['ChargeTime_min'].mean()),1)
    mean_text= 'Mean:'
    median_text ='Median:'

    Month_color_map = {'1': 'aliceblue', '2' : 'brown', '3' : 'cyan', '4' : 'darkblue', '5' : 'yellowgreen',
                   '6' : 'pink', '7' : 'yellow', '8' : 'lime', '9' : 'Black', '10' : 'red', '11' : 'green', '12' : 'purple'}

    fig = px.histogram(data_frame= lp_user, x="ChargeTime_min",                                                                                                             
                  title= "Charge time per minuten per maand",                       
                  color="Month",                                               
                  color_discrete_map = Month_color_map,
                  labels={"ChargeTime_min": "Chargetime (min)"}) 
    fig.update_xaxes(range=[0,1000])
    fig.add_annotation(x=800, y=800, text=median, showarrow=False)
    fig.add_annotation(x=800, y=750, text=mean, showarrow=False)
    fig.add_annotation(x=725, y=750, text=median_text, showarrow=False)
    fig.add_annotation(x=725, y=800, text=mean_text, showarrow=False)

    fig.update_annotations()
    fig.update_layout()                                                            
    st.plotly_chart(fig)

#side-bar + data selection
st.sidebar.write("""# Selectie menu⚙️""")
options = st.sidebar.radio('Bladzijdes📂', options=['RDW voertuigen', 'Locaties van laadpalen', 'Laadsessie\'s'])

if options == 'RDW voertuigen':
    display_ev_data()     

elif options == 'Locaties van laadpalen' :
    display_opencharge_map()
    
elif options == 'Laadsessie\'s':
    display_charge_data()
    