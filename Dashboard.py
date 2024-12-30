import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Bike Rentals Dashboard", layout="wide")

@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Load data
day = load_data("day.csv")
hour = load_data("hour.csv")

# Convert date columns to datetime
day['dteday'] = pd.to_datetime(day['dteday'])
hour['dteday'] = pd.to_datetime(hour['dteday'])


# Dashboard Title
st.title("Bike Rentals Dashboard")
st.markdown("### Analisis Pengaruh Cuaca dan Pola Penyewaan Sepeda Berdasarkan Jam")

# Sidebar Filters
st.sidebar.header("Filter Data")
filter_year = st.sidebar.selectbox("Pilih Tahun", options=[0, 1], format_func=lambda x: "2011" if x == 0 else "2012")
filter_workingday = st.sidebar.radio("Pilih Jenis Hari", options=[0, 1, 2], 
                                     format_func=lambda x: "Libur" if x == 0 else "Hari Kerja" if x == 1 else "Semua")

# Filter data based on selections
filtered_day = day[(day['yr'] == filter_year)]
if filter_workingday in [0, 1]:
    filtered_day = filtered_day[filtered_day['workingday'] == filter_workingday]

# **Pengaruh Cuaca terhadap Penyewaan Sepeda**
st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Pengaruh Suhu")
    fig_temp = px.scatter(filtered_day, x="temp", y="cnt", color="weathersit",
                          title="Suhu vs Jumlah Penyewaan",
                          labels={"temp": "Suhu (Normalized)", "cnt": "Jumlah Penyewaan", "weathersit": "Kondisi Cuaca"})
    st.plotly_chart(fig_temp, use_container_width=True)

with col2:
    st.markdown("### Pengaruh Kelembapan")
    fig_hum = px.scatter(filtered_day, x="hum", y="cnt", color="weathersit",
                         title="Kelembapan vs Jumlah Penyewaan",
                         labels={"hum": "Kelembapan", "cnt": "Jumlah Penyewaan", "weathersit": "Kondisi Cuaca"})
    st.plotly_chart(fig_hum, use_container_width=True)

with col3:
    st.markdown("### Pengaruh Kecepatan Angin")
    fig_wind = px.scatter(filtered_day, x="windspeed", y="cnt", color="weathersit",
                          title="Kecepatan Angin vs Jumlah Penyewaan",
                          labels={"windspeed": "Kecepatan Angin", "cnt": "Jumlah Penyewaan", "weathersit": "Kondisi Cuaca"})
    st.plotly_chart(fig_wind, use_container_width=True)

# **Pola Penyewaan Berdasarkan Jam**
st.subheader("Pola Penyewaan Sepeda Berdasarkan Jam")
hour_grouped = hour.groupby('hr')['cnt'].sum().reset_index()

# Create a line chart
fig_hour_trend = px.line(hour_grouped, 
                         x='hr', 
                         y='cnt', 
                         title="Pola Penyewaan Sepeda Berdasarkan Jam",
                         labels={'hr': 'Jam', 'cnt': 'Jumlah Penyewaan'})
fig_hour_trend.update_xaxes(tickmode='linear')

# Display chart
st.plotly_chart(fig_hour_trend, use_container_width=True)

# Find and display peak hour
peak_hour = hour_grouped[hour_grouped['cnt'] == hour_grouped['cnt'].max()]
st.write(f"**Jam puncak penyewaan sepeda:** {peak_hour['hr'].values[0]}:00 dengan {peak_hour['cnt'].values[0]} penyewaan.")

# **Tren Penyewaan Harian**
st.subheader("Tren Penyewaan Harian")
day_grouped = day.groupby('dteday')['cnt'].sum().reset_index()

fig_day_trend = px.line(day_grouped, x='dteday', y='cnt', 
                        title="Tren Penyewaan Sepeda Harian",
                        labels={"dteday": "Tanggal", "cnt": "Jumlah Penyewaan"})
fig_day_trend.update_xaxes(rangeslider_visible=True)
st.plotly_chart(fig_day_trend, use_container_width=True)