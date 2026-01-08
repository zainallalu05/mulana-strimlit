import streamlit as st

st.set_page_config( page_title="Kalkulator PLTS", layout="wide")

st.title("🔆 Kalkulator Sistem PLTS (On-Grid & Off-Grid)")

st.sidebar.header("⚙️ Parameter Sistem")

system_type = st.sidebar.selectbox("Jenis Sistem", ["Off-Grid", "On-Grid"])
system_voltage = st.sidebar.selectbox("Tegangan Sistem (V)", [12, 24, 48])
sun_hours = st.sidebar.number_input("Jam Matahari Efektif (jam/hari)", 3.0, 6.0, 4.0)
efficiency = st.sidebar.slider("Efisiensi Sistem (%)", 60, 95, 80) / 100

st.header("📊 Input Beban Listrik")

num_loads = st.number_input("Jumlah Peralatan", 1, 20, 3)

total_energy = 0
for i in range(num_loads):
    col1, col2, col3 = st.columns(3)
    with col1:
        power = st.number_input(f"Daya Alat {i+1} (W)", 1, 5000, 100)
    with col2:
        hours = st.number_input(f"Jam Pakai/hari {i+1}", 0.1, 24.0, 5.0)
    with col3:
        energy = power * hours
        st.write(f"Energi: **{energy:.1f} Wh**")
    total_energy += energy

st.subheader(f"🔋 Total Kebutuhan Energi: **{total_energy:.1f} Wh/hari**")

st.divider()

# ================== PERHITUNGAN ==================
st.header("⚡ Hasil Perhitungan")

# PANEL SURYA
panel_power = 550  # Wp
required_panel_power = total_energy / (sun_hours * efficiency)
num_panels = int(required_panel_power / panel_power) + 1

st.subheader("☀️ Panel Surya")
st.write(f"Kebutuhan Daya Panel: **{required_panel_power:.1f} Wp**")
st.write(f"Rekomendasi Panel: **{num_panels} unit x {panel_power} Wp**")

# BATERAI (OFF GRID)
if system_type == "Off-Grid":
    dod = 0.5
    battery_voltage = system_voltage
    battery_ah = (total_energy / (battery_voltage * dod))

    st.subheader("🔋 Baterai")
    st.write(f"Kapasitas Minimum Baterai: **{battery_ah:.1f} Ah @ {battery_voltage}V**")
    st.write("Contoh: 2–4 baterai 12V 100Ah (tergantung konfigurasi)")

# SCC
scc_current = (num_panels * panel_power) / system_voltage

st.subheader("🔌 Solar Charge Controller (SCC)")
st.write(f"Arus Minimum SCC: **{scc_current:.1f} A**")
st.write("Rekomendasi: **MPPT** (lebih efisien)")

# BIAYA ESTIMASI
st.header("💰 Estimasi Biaya")

panel_price = 3500000
battery_price = 2500000
scc_price = 2000000
inverter_price = 3000000

total_cost = (num_panels * panel_price) + scc_price + inverter_price

if system_type == "Off-Grid":
    total_cost += battery_price * 2

st.write(f"Estimasi Total Biaya: **Rp {total_cost:,.0f}**")

st.divider()

st.info("""
📌 Catatan:
- Ini estimasi kasar
- Tidak termasuk kabel, mounting, dan instalasi
- Untuk desain final, konsultasi teknisi PLTS
""")
