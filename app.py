import streamlit as st
from astral import LocationInfo
from astral.sun import sun
import pytz
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo 
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from timezonefinder import TimezoneFinder 

def get_location_info(lat, lon):
    geolocator = Nominatim(user_agent="geoapi")
    tf = TimezoneFinder() 

    try:
        location = geolocator.reverse((lat, lon), language="de", timeout=5)
    except (GeocoderTimedOut, GeocoderUnavailable):
        return {"city": "?", "country": "?", "timezone": "?"}

    if not location:
        return {"city": "?", "country": "?", "timezone": "?"}

    address = location.raw.get("address", {})

    # Stadt (verschiedene mögliche Felder)
    city = next(
        (address[key] for key in ["city", "town", "village", "hamlet", "municipality"]
         if key in address and address[key]),
        "?"
    )

    # Land
    country = address.get("country", "?")
    # --- Zeitzone mit timezonefinder --- 
    try: 
        tz = tf.timezone_at(lat=lat, lng=lon) 
        if tz: 
            timezone = tz 
    except Exception: 
        pass # bleibt "?"
    # Zeitzone (falls verfügbar)
    #timezone = location.raw.get("timezone", "?")

    return {"city": city, "country": country, "timezone": timezone}



def normalize_timezone(tz):
    """
    Gibt die übergebene Zeitzone zurück.
    Falls tz '?' ist oder None, wird 'Europe/Berlin' verwendet.
    """
    if not tz or tz == "?":
        return "Europe/Berlin"
    return tz


def timezone_to_utc_offset(tz_name):
    """
    Wandelt eine Zeitzone wie 'Europe/Berlin' in 'UTC+1' oder 'UTC+2' um.
    Falls tz_name '?' ist, wird 'UTC+1' (Europe/Berlin) verwendet.
    """
    if not tz_name or tz_name == "?":
        tz_name = "Europe/Berlin"

    try:
        now = datetime.now(ZoneInfo(tz_name))
        offset = now.utcoffset()
        hours = int(offset.total_seconds() // 3600)
        return f"UTC{hours:+d}"
    except Exception:
        return "UTC+1"   # Fallback


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

#result = search_location_by_coordinates(lat,lon)
#st.sidebar.header(result)

#geolocator = Nominatim(user_agent="geoapi")
#location = geolocator.reverse((lat, lon), language="de") 
wo = get_location_info(lat,lon)
tz = normalize_timezone(wo['timezone'])
tz2 = timezone_to_utc_offset(wo['timezone'])

st.sidebar.subheader('Ort:')
st.sidebar.text(f"{wo['city']}, {wo['country']}")
st.sidebar.subheader('Zeitzone:')
st.sidebar.text(f"{wo['timezone']}")
st.sidebar.text(f"{tz2}")
#st.sidebar.header(location.address) 
#st.sidebar.header(location.raw["address"].get("city")) 

year = st.sidebar.number_input("Jahr", value=2026, step=1)

st.sidebar.markdown('<a href="mailto:astro01239@gmail.com">Feedback</a>', unsafe_allow_html=True)

timezone = pytz.timezone(tz)
city = LocationInfo("Custom", "Earth", tz, lat, lon)

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
        "Zeit": [
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
            "MinMax": "*" if (i-1) in extreme_indices else ""
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)
