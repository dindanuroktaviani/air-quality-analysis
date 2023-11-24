import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

#1.Menyiapkan dataframe

def create_air_polution_yearly_df(df):
    air_polution_yearly_df = df.groupby("year").agg({
    "PM2.5" : "mean",
    "PM10" : "mean",
    "SO2" : "mean",
    "NO2" : "mean",
    "CO" : "mean",
    "O3" : "mean"
}) 
    return air_polution_yearly_df

def create_df_melted1(df):
    df_melted1 = df.melt(id_vars=['year'], value_vars=['PM2.5', 'PM10'], var_name='Parameter', value_name='Value')
    return df_melted1

def create_df_melted2(df):
    df_melted2 = df.melt(id_vars=['year'], value_vars=['SO2', 'NO2', 'CO','O3'], var_name='Parameter', value_name='Value')
    return df_melted2

def create_air_polution_station_df(df):
    air_polution_station_df = df.groupby("station").agg({
    "PM2.5" : "mean",
    "PM10" : "mean",
    "SO2" : "mean",
    "NO2" : "mean",
    "CO" : "mean",
    "O3" : "mean"
}) 
    return air_polution_station_df

#2.Load Berkas air_quality_df.csv
air_quality_df = pd.read_csv("air_quality_df.csv")

datetime_columns = ["date"]
air_quality_df.sort_values(by="date",inplace=True)
air_quality_df.reset_index(inplace=True)

for column in datetime_columns:
    air_quality_df[column] = pd.to_datetime(air_quality_df[column])

#3.Membuat Komponen Filter
min_date = air_quality_df["date"].min()
max_date = air_quality_df["date"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("C:\\Users\\dinda\\Downloads\\Ecommerce-air-quality-index")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = air_quality_df[(air_quality_df["date"] >= str(start_date)) & 
                (air_quality_df["date"] <= str(end_date))]

air_polution_yearly_df = create_air_polution_yearly_df(main_df)
df_melted1 = create_df_melted1(main_df)
df_melted2 = create_df_melted2(main_df)
air_polution_station_df = create_air_polution_station_df(main_df)

#4.Melengkapi Dashboard dgn Visualisasi Data
st.header('Dashboard Air Quality :sparkles:')

#4a.Tren Konsentrasi PM2.5 dan PM10 
st.subheader("Trend Konsentrasi PM2.5 dan PM10")

fig, ax = plt.subplots(figsize=(20, 10))
# plt.figure(figsize=(10, 6))
sns.lineplot(x='year', y='Value', hue='Parameter', marker='o', data=df_melted1)
plt.title('PM2.5 and PM10 Trends Over Years')
plt.xlabel(None)
plt.ylabel(None)
plt.show()

st.pyplot(fig)

#4b.Tren Konsentrasi Other Polutan
st.subheader("Tren Konsentrasi Other Polutan")

fig, ax = plt.subplots(figsize=(20, 10))
# plt.figure(figsize=(10, 6))
sns.lineplot(x='year', y='Value', hue='Parameter', marker='o', data=df_melted2)
plt.title('Other Polutants Trends Over Years')
plt.xlabel(None)
plt.ylabel(None)
plt.show()

st.pyplot(fig)

#4c.PM per station
st.subheader("Particulate Matter per Station")

air_polution_station_df["sumPM"] = air_polution_station_df["PM2.5"]+air_polution_station_df["PM10"]
air_polution_station_df.sort_values(by="sumPM",ascending=False)
fig, ax = plt.subplots(figsize=(20, 10))
# plt.figure(figsize=(10, 6))
sns.barplot(x="sumPM", y="station", data=air_polution_station_df.sort_values(by="sumPM",ascending=False))
plt.title('Particulate Matter per Station')
plt.xlabel(None)
plt.ylabel(None)
plt.show()

st.pyplot(fig)

#4d.CO per station
st.subheader("CO per station")

fig, ax = plt.subplots(figsize=(20, 10))
# plt.figure(figsize=(10, 6))
sns.barplot(x="CO", y="station", data=air_polution_station_df.sort_values(by="CO",ascending=False))
plt.title('Concentration CO per Station')
plt.xlabel(None)
plt.ylabel(None)
plt.show()

st.pyplot(fig)

