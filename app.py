#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  4 08:54:20 2026

@author: up
"""

import streamlit as st
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from timezonefinder import TimezoneFinder


# ---------------------------------------------------------
# 🌍 Mehrsprachigkeit
# ---------------------------------------------------------
LANG = {
    "de": {
        "title": "🌅 Jahresanalyse der Sonnenzeiten",
        "subtitle": "Berechne Sonnenaufgang, Sonnenuntergang und Tageslänge für jeden Tag eines Jahres.",
        "location_settings": "📍 Standort & Einstellungen",
        "latitude": "Breitengrad",
        "longitude": "Längengrad",
        "year": "Jahr",
        "place": "Ort",
        "timezone": "Zeitzone",
        "utc_offset": "UTC-Verschiebung",
        "chart": "📈 Diagramm",
        "extremes": "⭐ Extremwerte",
        "table": "📅 Jahrestabelle",
        "sunrise": "Sonnenaufgang",
        "sunset": "Sonnenuntergang",
        "daylength": "Tageslänge",
        "min_sunrise": "Frühester Sonnenaufgang",
        "max_sunrise": "Spätester Sonnenaufgang",
        "min_sunset": "Frühester Sonnenuntergang",
        "max_sunset": "Spätester Sonnenuntergang",
        "min_day": "Kürzeste Tageslänge",
        "max_day": "Längste Tageslänge",
        "day_col": "Tageslänge (h)",
        "date_col": "Datum",
        "event_col": "Ereignis",
        "value_col": "Zeit / Länge",
        "day_index_col": "Tag#",
        "minmax_col": "Min/Max",
        "lang": "Sprache",
        "ordinate": "Stunde des Tages [h]",
    },
    "en": {
        "title": "🌅 Annual Sunlight Analysis",
        "subtitle": "Calculate sunrise, sunset and day length for every day of the year.",
        "location_settings": "📍 Location & Settings",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "year": "Year",
        "place": "Place",
        "timezone": "Timezone",
        "utc_offset": "UTC offset",
        "chart": "📈 Chart",
        "extremes": "⭐ Extremes",
        "table": "📅 Year table",
        "sunrise": "Sunrise",
        "sunset": "Sunset",
        "daylength": "Day length",
        "min_sunrise": "Earliest sunrise",
        "max_sunrise": "Latest sunrise",
        "min_sunset": "Earliest sunset",
        "max_sunset": "Latest sunset",
        "min_day": "Shortest day",
        "max_day": "Longest day",
        "day_col": "Day length (h)",
        "date_col": "Date",
        "event_col": "Event",
        "value_col": "Time / length",
        "day_index_col": "Day#",
        "minmax_col": "Min/Max",
        "lang": "Language",
        "ordinate": "Hour of the day [h]",
    },
    "fr": {
        "title": "🌅 Analyse annuelle du soleil",
        "subtitle": "Calcule le lever, le coucher du soleil et la durée du jour pour chaque jour de l'année.",
        "location_settings": "📍 Localisation et paramètres",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "year": "Année",
        "place": "Lieu",
        "timezone": "Fuseau horaire",
        "utc_offset": "Décalage UTC",
        "chart": "📈 Diagramme",
        "extremes": "⭐ Valeurs extrêmes",
        "table": "📅 Tableau annuel",
        "sunrise": "Lever du soleil",
        "sunset": "Coucher du soleil",
        "daylength": "Durée du jour",
        "min_sunrise": "Lever le plus tôt",
        "max_sunrise": "Lever le plus tard",
        "min_sunset": "Coucher le plus tôt",
        "max_sunset": "Coucher le plus tard",
        "min_day": "Jour le plus court",
        "max_day": "Jour le plus long",
        "day_col": "Durée du jour (h)",
        "date_col": "Date",
        "event_col": "Événement",
        "value_col": "Heure / durée",
        "day_index_col": "Jour#",
        "minmax_col": "Min/Max",
        "lang": "Langue",
        "ordinate": "Heure du jour [h]",
    },
    "es": {
        "title": "🌅 Análisis anual de luz solar",
        "subtitle": "Calcula el amanecer, atardecer y duración del día para cada día del año.",
        "location_settings": "📍 Ubicación y ajustes",
        "latitude": "Latitud",
        "longitude": "Longitud",
        "year": "Año",
        "place": "Lugar",
        "timezone": "Zona horaria",
        "utc_offset": "Desfase UTC",
        "chart": "📈 Gráfico",
        "extremes": "⭐ Valores extremos",
        "table": "📅 Tabla anual",
        "sunrise": "Amanecer",
        "sunset": "Atardecer",
        "daylength": "Duración del día",
        "min_sunrise": "Amanecer más temprano",
        "max_sunrise": "Amanecer más tardío",
        "min_sunset": "Atardecer más temprano",
        "max_sunset": "Atardecer más tardío",
        "min_day": "Día más corto",
        "max_day": "Día más largo",
        "day_col": "Duración del día (h)",
        "date_col": "Fecha",
        "event_col": "Evento",
        "value_col": "Hora / duración",
        "day_index_col": "Día#",
        "minmax_col": "Min/Max",
        "lang" : "Idioma",
        "ordinate": "Hora del día [h]",
    },
    "ru": {
        "title": "🌅 Годовой анализ солнечного света",
        "subtitle": "Рассчитайте время восхода, заката и длину дня для каждого дня года.",
        "location_settings": "📍 Местоположение и настройки",
        "latitude": "Широта",
        "longitude": "Долгота",
        "year": "Год",
        "place": "Место",
        "timezone": "Часовой пояс",
        "utc_offset": "Смещение UTC",
        "chart": "📈 Диаграмма",
        "extremes": "⭐ Экстремальные значения",
        "table": "📅 Таблица года",
        "sunrise": "Восход",
        "sunset": "Закат",
        "daylength": "Длина дня",
        "min_sunrise": "Самый ранний восход",
        "max_sunrise": "Самый поздний восход",
        "min_sunset": "Самый ранний закат",
        "max_sunset": "Самый поздний закат",
        "min_day": "Самый короткий день",
        "max_day": "Самый длинный день",
        "day_col": "Длина дня (ч)",
        "date_col": "Дата",
        "event_col": "Событие",
        "value_col": "Время / длина",
        "day_index_col": "День#",
        "minmax_col": "Мин/Макс",
        "lang": "Язык",
        "ordinate": "Час дня [h]",
    }
}


# ---------------------------------------------------------
# 📍 Standort & Zeitzone
# ---------------------------------------------------------
def get_location_info(lat, lon):
    geolocator = Nominatim(user_agent="geoapi")
    tf = TimezoneFinder()

    city = "?"
    country = "?"
    timezone = "?"

    try:
        location = geolocator.reverse((lat, lon), language="de", timeout=5)
        if location:
            address = location.raw.get("address", {})
            city = next(
                (address.get(k) for k in ["city", "town", "village", "hamlet", "municipality"] if address.get(k)),
                "?"
            )
            country = address.get("country", "?")
    except (GeocoderTimedOut, GeocoderUnavailable, Exception):
        pass

    try:
        tz = tf.timezone_at(lat=lat, lng=lon)
        if tz:
            timezone = tz
    except Exception:
        pass

    return {"city": city, "country": country, "timezone": timezone}


def timezone_to_utc_offset(tz_name: str) -> str:
    if not tz_name or tz_name == "?":
        tz_name = "Europe/Berlin"
    try:
        now = datetime.now(ZoneInfo(tz_name))
        offset = now.utcoffset()
        hours = int(offset.total_seconds() // 3600)
        return f"UTC{hours:+d}"
    except Exception:
        return "UTC+1"


# ---------------------------------------------------------
# 🌞 Sonnenzeiten berechnen (mit Cache)
# ---------------------------------------------------------
@st.cache_data
def compute_sun_times(lat, lon, year, tz):
    tzinfo = ZoneInfo(tz)
    city = LocationInfo("Custom", "Earth", tz, lat, lon)

    start = datetime(year, 1, 1, tzinfo=tzinfo)
    end = datetime(year, 12, 31, tzinfo=tzinfo)

    dates = []
    sunrise = []
    sunset = []
    daylen = []

    current = start
    while current <= end:
        s = sun(city.observer, date=current.date(), tzinfo=tzinfo)
        dates.append(current)
        sunrise.append(s["sunrise"])
        sunset.append(s["sunset"])
        daylen.append((s["sunset"] - s["sunrise"]).total_seconds() / 3600)
        current += timedelta(days=1)

    return dates, sunrise, sunset, daylen


# ---------------------------------------------------------
# 🖥 Streamlit UI
# ---------------------------------------------------------
st.set_page_config(page_title="Sonnenzeiten", page_icon="🌅", layout="wide")

# Sprache oben initialisieren
if "language" not in st.session_state:
    st.session_state.language = "de"

T = LANG[st.session_state.language]

# Titel
st.markdown(f"# {T['title']}")
st.markdown(T["subtitle"])

# Sidebar: Standort & Jahr
st.sidebar.header(T["location_settings"])
lat = st.sidebar.number_input(T["latitude"], value=51.0504, format="%.6f")
lon = st.sidebar.number_input(T["longitude"], value=13.7373, format="%.6f")
year = st.sidebar.number_input(T["year"], value=2026, step=1)

# Standortinfo & Zeitzone
info = get_location_info(lat, lon)
tz = info["timezone"] if info["timezone"] != "?" else "Europe/Berlin"
utc_offset_str = timezone_to_utc_offset(tz)

st.sidebar.subheader(T["place"])
st.sidebar.text(f"{info['city']}, {info['country']}")

st.sidebar.subheader(T["timezone"])
st.sidebar.text(tz)

st.sidebar.subheader(T["utc_offset"])
st.sidebar.text(utc_offset_str)

# Daten: Ein Dictionary, das IDs auf Anzeigenamen mappt
options_dict = {
    "de": "\U0001F1E9\U0001F1EA Deutsch",
    "en": "\U0001F1FA\U0001F1F8 English",
    "fr": "\U0001F1EB\U0001F1F7 Français",
    "es": "\U0001F1EA\U0001F1F8 Español",
    "ru": "\U0001F1F7\U0001F1FA Русский",
}

# Die Selectbox nutzt die Keys ("de", "fr", ...) als Auswahlbasis
new_lang = st.sidebar.selectbox(
    T["lang"],
    options=list(options_dict.keys()),
    format_func=lambda x: options_dict[x],
    index=["de", "en", "fr", "es", "ru"].index(st.session_state.language)
)

if new_lang != st.session_state.language:
    st.session_state.language = new_lang
    st.rerun()

st.sidebar.markdown('<a href="mailto:astro01239@gmail.com">Feedback</a>', unsafe_allow_html=True)

# Berechnung
dates, sr, ss, dl = compute_sun_times(lat, lon, year, tz)

# Hilfswerte
sr_hours = [t.hour + t.minute/60 + t.second/3600 for t in sr]
ss_hours = [t.hour + t.minute/60 + t.second/3600 for t in ss]
sr_str = [t.strftime("%H:%M") for t in sr]
ss_str = [t.strftime("%H:%M") for t in ss]
dl_str = [f"{int(x)}:{int((x % 1) * 60):02d}" for x in dl]

# Extremwerte
idx_min_sr = int(np.argmin(sr_hours))
idx_max_sr = int(np.argmax(sr_hours))
idx_min_ss = int(np.argmin(ss_hours))
idx_max_ss = int(np.argmax(ss_hours))
idx_min_dl = int(np.argmin(dl))
idx_max_dl = int(np.argmax(dl))

extreme_indices = {
    idx_min_sr, idx_max_sr,
    idx_min_ss, idx_max_ss,
    idx_min_dl, idx_max_dl
}

# Tabs
tab1, tab2, tab3 = st.tabs([T["chart"], T["extremes"], T["table"]])

# ---------------------------------------------------------
# 📈 Diagramm (mit Linienstilen & Markern)
# ---------------------------------------------------------
with tab1:
    fig = go.Figure()

    # Sonnenaufgang – gestrichelte Linie
    fig.add_trace(go.Scatter(
        x=dates, y=sr_hours,
        mode="lines",
        name=T["sunrise"],
        line=dict(color="#1f77b4", dash="dashdot"),
        customdata=sr_str,
        hovertemplate="<b>%{customdata}</b><extra></extra>"
    ))

    # Sonnenuntergang – andere Strichart
    fig.add_trace(go.Scatter(
        x=dates, y=ss_hours,
        mode="lines",
        name=T["sunset"],
        line=dict(color="#ff7f0e", dash="dash"),
        customdata=ss_str,
        hovertemplate="<b>%{customdata}</b><extra></extra>"
    ))

    # Tageslänge – durchgezogen
    fig.add_trace(go.Scatter(
        x=dates, y=dl,
        mode="lines",
        name=T["daylength"],
        line=dict(color="#2ca02c", dash="solid"),
        customdata=dl_str,
        hovertemplate="<b>%{customdata}</b><extra></extra>"
    ))

    # Marker-Funktion
    def add_marker(idx, label, color, value_str, y_value, symbol, textposition):
        fig.add_trace(go.Scatter(
            x=[dates[idx]], y=[y_value],
            mode="markers+text",
            name=label,
            text=[label],
            textposition=textposition,
            marker=dict(color=color, size=15, symbol=symbol),
            customdata=[value_str],
            hovertemplate=f"{label}: %{{customdata}}<extra></extra>"
        ))

    # Marker hinzufügen – Texte aus LANG
    add_marker(idx_min_sr, T["min_sunrise"], "blue", sr_str[idx_min_sr], sr_hours[idx_min_sr], "triangle-down", "bottom center")
    add_marker(idx_max_sr, T["max_sunrise"], "cyan", sr_str[idx_max_sr], sr_hours[idx_max_sr], "triangle-up", "bottom center")
    add_marker(idx_min_ss, T["min_sunset"], "red", ss_str[idx_min_ss], ss_hours[idx_min_ss], "triangle-down", "top center")
    add_marker(idx_max_ss, T["max_sunset"], "darkred", ss_str[idx_max_ss], ss_hours[idx_max_ss], "triangle-up", "top center")
    add_marker(idx_min_dl, T["min_day"], "green", dl_str[idx_min_dl], dl[idx_min_dl], "triangle-down", "top center")
    add_marker(idx_max_dl, T["max_day"], "lime", dl_str[idx_max_dl], dl[idx_max_dl], "triangle-up", "top center")

    fig.update_layout(
        title=f"{T['sunrise']}, {T['sunset']} & {T['daylength']} – {year}",
        xaxis_title=T["date_col"],
        yaxis_title=T["ordinate"],
        hovermode="x unified",
        template="plotly_white",
        height=600,
        xaxis=dict(showgrid=True, gridcolor="gray", gridwidth=0.1, griddash="dot", nticks=30),
        yaxis=dict(showgrid=True, gridcolor="gray", gridwidth=0.1, griddash="dot", nticks=30)
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# ⭐ Extremwerte
# ---------------------------------------------------------
with tab2:
    df_ext = pd.DataFrame({
        T["event_col"]: [
            T["min_sunrise"], T["max_sunrise"],
            T["min_sunset"], T["max_sunset"],
            T["min_day"], T["max_day"]
        ],
        T["date_col"]: [
            dates[idx_min_sr].strftime("%d.%m.%Y"),
            dates[idx_max_sr].strftime("%d.%m.%Y"),
            dates[idx_min_ss].strftime("%d.%m.%Y"),
            dates[idx_max_ss].strftime("%d.%m.%Y"),
            dates[idx_min_dl].strftime("%d.%m.%Y"),
            dates[idx_max_dl].strftime("%d.%m.%Y"),
        ],
        T["value_col"]: [
            sr_str[idx_min_sr],
            sr_str[idx_max_sr],
            ss_str[idx_min_ss],
            ss_str[idx_max_ss],
            dl_str[idx_min_dl],
            dl_str[idx_max_dl],
        ]
    })

    st.dataframe(df_ext, use_container_width=True)

# ---------------------------------------------------------
# 📅 Jahrestabelle
# ---------------------------------------------------------
with tab3: 
    rows = [] 
    for i, (d, srt, sst, dlen) in enumerate(zip(dates, sr_str, ss_str, dl_str), start=1): 
        rows.append({ 
            T["day_index_col"]: i, 
            T["date_col"]: d.strftime("%d.%m.%Y"), 
            T["sunrise"]: srt, 
            T["sunset"]: sst, 
            T["day_col"]: dlen, 
            T["minmax_col"]: "*" if (i - 1) in extreme_indices else "" 
            }) 
        df = pd.DataFrame(rows) 
        st.dataframe(df, use_container_width=True)

