import streamlit as st
import math

# =====================================================
# KONFIGURASI HALAMAN
# =====================================================
st.set_page_config(
    page_title="Kalkulator PLTS Profesional",
    layout="wide",
    page_icon="☀️"
)

st.title("☀️ Kalkulator Sistem PLTS Profesional")
st.caption("Alat bantu perhitungan awal untuk teknisi & konsultan PLTS")

# =====================================================
# SIDEBAR – PARAMETER SISTEM
# =====================================================
st.sidebar.header("⚙️ Parameter Sistem")

system_type = st.sidebar.selectbox(
    "Jenis Sistem PLTS",
    ["Off-Grid", "On-Grid"]
)

system_voltage = st.sidebar.selectbox(
    "Tegangan Sistem DC (V)",
    [12, 24, 48]
)

sun_hours = st.sidebar.number_input(
    "Jam Matahari Efektif (PSH) [jam/hari]",
    min_value=3.0,
    max_value=6.5,
    value=4.0,
    step=0.1
)

efficiency = st.sidebar.slider(
    "Efisiensi Sistem Total (%)",
    60,
    95,
    80
) / 100

days_backup = 1
if system_type == "Off-Grid":
    days_backup = st.sidebar.number_input(
        "Hari Cadangan Baterai (days of autonomy)",
        min_value=1,
        max_value=3,
        value=1
    )

st.sidebar.divider()

tarif_pln = st.sidebar.number_input(
    "Tarif Listrik PLN (Rp/kWh)",
    min_value=1000,
    max_value=3000,
    value=1444
)

# =====================================================
# INPUT BEBAN LISTRIK
# =====================================================
st.header("📊 Input Beban Listrik")

num_loads = st.number_input(
    "Jumlah Peralatan",
    min_value=1,
    max_value=30,
    value=3
)

total_energy_wh = 0.0
total_power_w = 0.0

for i in range(int(num_loads)):
    with st.expander(f"🔹 Peralatan {i+1}", expanded=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            power = st.number_input(
                "Daya (W)",
                min_value=1,
                max_value=5000,
                value=100,
                key=f"power_{i}"
            )

        with col2:
            hours = st.number_input(
                "Jam Pakai per Hari",
                min_value=0.1,
                max_value=24.0,
                value=5.0,
                key=f"hours_{i}"
            )

        energy = power * hours

        with col3:
            st.metric("Energi Harian", "{:.1f} Wh".format(energy))

        total_power_w += power
        total_energy_wh += energy

# =====================================================
# RINGKASAN KONSUMSI
# =====================================================
st.divider()
st.header("🔋 Ringkasan Konsumsi Energi")

energy_kwh_day = total_energy_wh / 1000
energy_kwh_month = energy_kwh_day * 30

col1, col2, col3 = st.columns(3)
col1.metric("Total Daya Terpasang", "{:.0f} W".format(total_power_w))
col2.metric("Energi Harian", "{:.2f} kWh".format(energy_kwh_day))
col3.metric("Energi Bulanan", "{:.1f} kWh".format(energy_kwh_month))

biaya_pln = energy_kwh_month * tarif_pln
st.metric("Estimasi Tagihan PLN / Bulan", "Rp {:,.0f}".format(biaya_pln))

# =====================================================
# PERHITUNGAN PANEL SURYA
# =====================================================
st.divider()
st.header("☀️ Perhitungan Panel Surya")

panel_wp = 550
required_wp = total_energy_wh / (sun_hours * efficiency)
num_panels = math.ceil(required_wp / panel_wp)

st.write("Kebutuhan Daya Panel: {:.1f} Wp".format(required_wp))
st.success("Rekomendasi Panel: {} unit x {} Wp".format(num_panels, panel_wp))

# =====================================================
# PERHITUNGAN INVERTER
# =====================================================
st.header("🔄 Inverter")

inverter_power = total_power_w * 1.25
st.write("Daya Inverter Minimum: {:.0f} W".format(inverter_power))
st.write("Rekomendasi: pilih inverter di atas nilai ini")

# =====================================================
# PERHITUNGAN BATERAI (OFF-GRID)
# =====================================================
if system_type == "Off-Grid":
    st.header("🔋 Perhitungan Baterai")

    dod = 0.5
    battery_voltage = system_voltage

    battery_ah = (total_energy_wh * days_backup) / (battery_voltage * dod)

    st.write(
        "Kapasitas Baterai Minimum: {:.1f} Ah @ {} V".format(
            battery_ah, battery_voltage
        )
    )
    st.write("Contoh konfigurasi: baterai 12V 100Ah diseri/paralel")
    st.warning("⚠️ Untuk baterai lithium, DoD bisa 80–90%")

# =====================================================
# SOLAR CHARGE CONTROLLER
# =====================================================
st.header("🔌 Solar Charge Controller (SCC)")

scc_current = (num_panels * panel_wp) / system_voltage
st.write("Arus Minimum SCC: {:.1f} A".format(scc_current))
st.success("Rekomendasi: MPPT")

# =====================================================
# ESTIMASI BIAYA SISTEM
# =====================================================
st.divider()
st.header("💰 Estimasi Biaya Sistem")

panel_price = 3500000
battery_price = 2500000
scc_price = 2000000
inverter_price = 3000000

total_cost = (
    num_panels * panel_price
    + scc_price
    + inverter_price
)

if system_type == "Off-Grid":
    total_cost += battery_price * 2

st.metric("Estimasi Total Investasi", "Rp {:,.0f}".format(total_cost))

if system_type == "On-Grid":
    payback_year = total_cost / (biaya_pln * 12)
    st.success("Estimasi Balik Modal: {:.1f} tahun".format(payback_year))

# =====================================================
# CATATAN TEKNISI
# =====================================================
st.divider()
st.info("""
📌 Catatan Teknis:
- Ini adalah perhitungan awal (preliminary design)
- Belum memasukkan faktor rugi kabel, suhu, shading
- Untuk desain final gunakan survey lapangan & software simulasi
- Cocok untuk konsultasi awal dengan klien PLTS
""")
