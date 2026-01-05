---

# 🌅 Daylength App  
Interactive annual analysis of sunrise, sunset, and daylight duration

## 📌 Overview  
The Daylength App is an interactive Streamlit application that calculates sunrise, sunset, and daylength for every day of any selected year.  
It uses precise astronomical calculations (Astral library) and provides a modern, multilingual user interface optimized for desktop and mobile devices.

---

## ✨ Features

### 🔭 Astronomical Calculations  
- Sunrise time  
- Sunset time  
- Daylength (HH:MM:SS)  
- Automatic timezone detection based on coordinates  
- Display of UTC offset (e.g., UTC+1)

### 🌍 Multilingual Interface  
Supported languages:
- English  
- German  
- French  
- Spanish  
- Russian  

Language can be switched directly in the sidebar.

### 📈 Interactive Charts  
- Line chart for sunrise, sunset, and daylength  
- Distinct line styles for better readability  
- Automatic markers for extreme values  
  - earliest/latest sunrise  
  - earliest/latest sunset  
  - shortest/longest day  
- Legend placed below the chart for optimal mobile and portrait‑mode viewing

### 📅 Table Views  
- Summary of all extreme values  
- Full year table with all daily values  
- Compact layout without index column  
- Highlighted rows for min/max days

---

## 🧭 How to Use

1. **Enter latitude and longitude**  
   The app automatically detects city, country, and timezone.

2. **Select a year**  
   Calculations cover all 365/366 days.

3. **Choose a language**  
   The interface updates instantly.

4. **Explore charts and tables**  
   Extreme values are clearly highlighted.

---

## 🛠️ Technologies

- **Python 3.10+**  
- **Streamlit** – UI framework  
- **Astral** – solar position calculations  
- **TimezoneFinder** – timezone detection  
- **Geopy** – reverse geocoding  
- **Plotly** – interactive charts  
- **Pandas / NumPy** – data processing  

---

## 🚀 Run the App

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📬 Feedback  
Questions or suggestions  
📧 astro01239@gmail.com

---


