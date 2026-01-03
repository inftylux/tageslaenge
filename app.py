import streamlit as st
from astral import LocationInfo
from astral.sun import sun
import pytz
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="Sonnenzeiten Jahresanalyse",
    page_icon="🌅",
    layout="wide"
)

# --- Titel ---
st.markdown("""
# 🌅 Jahresanalyse der Sonnenzeiten  
Berechne Sonnenaufgang, Sonnenuntergang und Tageslänge für jeden Tag eines Jahres.
""")

# --- Sidebar ---
st.sidebar.header("📍 Standort & Einstellungen")

lat = st.sidebar.number_input("Breitengrad", value=51.0504, format="%.6f")
lon = st.sidebar.number_input("Längengrad", value=13.7373, format="%.6f")
year = st.sidebar.number_input("Jahr", value=2026, step=1)

timezone = pytz.timezone("Europe/Berlin")
city = LocationInfo("Custom", "Earth", "Europe/Berlin", lat, lon)

# --- Berechnung ---
start = datetime(year, 1, 1, tzinfo=timezone)
end = datetime(year, 12, 31, tzinfo=timezone)

dates = []
sunrise_times = []
sunset_times = []
day_lengths = []

current = start
while current <= end:
    s = sun(city.observer, date=current.date(), tzinfo=timezone)

    sunrise = s["sunrise"]
    sunset = s["sunset"]

    dates.append(current)
    sunrise_times.append(sunrise)
    sunset_times.append(sunset)
    day_lengths.append((sunset - sunrise).total_seconds() / 3600)

    current += timedelta(days=1)

# --- Hilfsarrays ---
sr_hours = [t.hour + t.minute/60 + t.second/3600 for t in sunrise_times]
ss_hours = [t.hour + t.minute/60 + t.second/3600 for t in sunset_times]

# Zeitstrings für Hover
sr_str = [t.strftime("%H:%M") for t in sunrise_times]
ss_str = [t.strftime("%H:%M") for t in sunset_times]
dl_str = [f"{int(dl)}:{int((dl % 1) * 60):02d}" for dl in day_lengths]

# --- Extremwerte ---
idx_min_sr = int(np.argmin(sr_hours))
idx_max_sr = int(np.argmax(sr_hours))
idx_min_ss = int(np.argmin(ss_hours))
idx_max_ss = int(np.argmax(ss_hours))
idx_min_dl = int(np.argmin(day_lengths))
idx_max_dl = int(np.argmax(day_lengths))

extreme_indices = {
    idx_min_sr, idx_max_sr,
    idx_min_ss, idx_max_ss,
    idx_min_dl, idx_max_dl
}

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["📈 Diagramm", "⭐ Extremwerte", "📅 Jahrestabelle"])

# --- Tab 1: Interaktives Diagramm ---
with tab1:
    st.subheader("📈 Interaktives Jahresdiagramm")

    fig = go.Figure()

    # Sonnenaufgang
    fig.add_trace(go.Scatter(
        x=dates, y=sr_hours,
        mode="lines",
        name="Sonnenaufgang",
        line=dict(color="#1f77b4"),
        customdata=sr_str,
        hovertemplate="<br>%{customdata}"
    ))

    # Sonnenuntergang
    fig.add_trace(go.Scatter(
        x=dates, y=ss_hours,
        mode="lines",
        name="Sonnenuntergang",
        line=dict(color="#ff7f0e"),
        customdata=ss_str,
        hovertemplate="<br>%{customdata}"
    ))

    # Tageslänge
    fig.add_trace(go.Scatter(
        x=dates, y=day_lengths,
        mode="lines",
        name="Tageslänge",
        line=dict(color="#2ca02c"),
        customdata=dl_str,
        hovertemplate="<br>%{customdata}"
    ))

    # Marker-Funktion
    def add_marker(idx, label, color, value_str, y_value):
        fig.add_trace(go.Scatter(
            x=[dates[idx]], y=[y_value],
            mode="markers",
            name=label,
            marker=dict(color=color, size=10),
            customdata=[value_str],
            hovertemplate=f"{label}: %{{customdata}}"
        ))

    add_marker(idx_min_sr, "Min Aufgang", "blue", sr_str[idx_min_sr], sr_hours[idx_min_sr])
    add_marker(idx_max_sr, "Max Aufgang", "cyan", sr_str[idx_max_sr], sr_hours[idx_max_sr])
    add_marker(idx_min_ss, "Min Untergang", "red", ss_str[idx_min_ss], ss_hours[idx_min_ss])
    add_marker(idx_max_ss, "Max Untergang", "darkred", ss_str[idx_max_ss], ss_hours[idx_max_ss])
    add_marker(idx_min_dl, "Min Tageslänge", "green", dl_str[idx_min_dl], day_lengths[idx_min_dl])
    add_marker(idx_max_dl, "Max Tageslänge", "lime", dl_str[idx_max_dl], day_lengths[idx_max_dl])

    fig.update_layout(
        title=f"Sonnenaufgang, Sonnenuntergang und Tageslänge – {year}",
        xaxis_title="Datum",
        yaxis_title="Stunden",
        hovermode="x unified",
        template="plotly_white",
        height=600,
        xaxis=dict(showgrid=True, gridcolor="gray", gridwidth=0.1, griddash="dot", nticks=30), 
        yaxis=dict(showgrid=True, gridcolor="gray", gridwidth=0.1, griddash="dot", nticks=30) 
    )

    st.plotly_chart(fig, use_container_width=True)

# --- Tab 2: Extremwerte ---
with tab2:
    st.subheader("⭐ Extremwerte des Jahres")

    extreme_data = {
        "Ereignis": [
            "Frühester Sonnenaufgang",
            "Spätester Sonnenaufgang",
            "Frühester Sonnenuntergang",
            "Spätester Sonnenuntergang",
            "Kürzeste Tageslänge",
            "Längste Tageslänge"
        ],
        "Datum": [
            dates[idx_min_sr].strftime("%d.%m.%Y"),
            dates[idx_max_sr].strftime("%d.%m.%Y"),
            dates[idx_min_ss].strftime("%d.%m.%Y"),
            dates[idx_max_ss].strftime("%d.%m.%Y"),
            dates[idx_min_dl].strftime("%d.%m.%Y"),
            dates[idx_max_dl].strftime("%d.%m.%Y"),
        ],
        "Wert": [
            sr_str[idx_min_sr],
            sr_str[idx_max_sr],
            ss_str[idx_min_ss],
            ss_str[idx_max_ss],
            dl_str[idx_min_dl],
            dl_str[idx_max_dl],
        ]
    }

    st.dataframe(pd.DataFrame(extreme_data), use_container_width=True)

# --- Tab 3: Jahrestabelle ---
with tab3:
    st.subheader("📅 Tabelle aller Tage")

    rows = []
    for i, (d, sr, ss, dl) in enumerate(zip(dates, sunrise_times, sunset_times, day_lengths), start=1):
        rows.append({
            "Tag#": i,
            "Datum": d.strftime("%d.%m.%Y"),
            "Sonnenaufgang": sr.strftime("%H:%M"),
            "Sonnenuntergang": ss.strftime("%H:%M"),
            "Tageslänge (h)": f"{int(dl)}:{int((dl % 1) * 60):02d}",
            "*": "*" if (i-1) in extreme_indices else ""
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)
