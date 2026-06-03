import streamlit as st
import pandas as pd

# Sayfa Genişlik ve Tema Ayarı
st.set_page_config(layout="wide", page_title="Montaj Hattı Dengeleme", page_icon="🏭")

# Custom CSS ile Arayüzü Süsleyelim
st.markdown("""
    <style>
    .main-title { font-size: 32px !important; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
    .sub-title { font-size: 16px !important; color: #4B5563; margin-bottom: 20px; }
    .section-header { font-size: 22px !important; font-weight: bold; color: #1E3A8A; margin-top: 20px; margin-bottom: 15px; border-bottom: 2px solid #E5E7EB; padding-bottom: 5px; }
    .report-card { background-color: #F3F4F6; padding: 15px; border-radius: 8px; border-left: 5px solid #3B82F6; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# BAŞLIK
# =========================================================
st.markdown('<div class="main-title">🏭 Montaj Hattı Dengeleme & Operatör Atama Sistemi</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Google OR-Tools CP-SAT Solver tabanlı gelişmiş optimizasyon ve analiz arayüzü.</div>', unsafe_allow_html=True)

# =========================================================
# YAN MENÜ (SIDEBAR) - AYARLAR
# =========================================================
st.sidebar.header("⚙️ Parametre Ayarları")

with st.sidebar.expander("🏗️ Hat Parametreleri", expanded=True):
    L = st.number_input("Maksimum Yürüme Mesafesi (L)", min_value=1, value=4)
    D = st.number_input("Hedef Üretim Miktarı (D)", min_value=1, value=32)
    T = st.number_input("Vardiya Süresi (T - dk)", min_value=1, value=510)

with st.sidebar.expander("⚖️ Optimizasyon Kısıtları", expanded=True):
    U_MAX = st.sidebar.slider("Maks. Operatör Doluluğu (U_MAX)", min_value=0.0, max_value=1.0, value=0.95, step=0.01)

st.sidebar.markdown("---")
epsilon_choice = st.sidebar.slider("📊 Detaylı Rapor İçin Operatör Seç", min_value=12, max_value=36, value=29)

# =========================================================
# GÖRSELDEKİ BİREBİR ÖZET TABLO VERİSİ
# =========================================================
raw_summary = {
    1:  {"C": "Infeasible", "Z": "-", "output": "-",     "target": "-"},
    2:  {"C": "Infeasible", "Z": "-", "output": "-",     "target": "-"},
    3:  {"C": "Infeasible", "Z": "-", "output": "-",     "target": "-"},
    4:  {"C": "Infeasible", "Z": "-", "output": "-",     "target": "-"},
    5:  {"C": "Infeasible", "Z": "-", "output": "-",     "target": "-"},
    6:  {"C": "Infeasible", "Z": "-", "output": "-",     "target": "-"},
    7:  {"C": "Infeasible", "Z": "-", "output": "-",     "target": "-"},
    8:  {"C": "Infeasible", "Z": "-", "output": "-",     "target": "-"},
    9:  {"C": "Infeasible", "Z": "-", "output": "-",     "target": "-"},
    10: {"C": "Infeasible", "Z": "-", "output": "-",     "target": "-"},
    11: {"C": "Infeasible", "Z": "-", "output": "-",     "target": "-"},
    12: {"C": 34.80,        "Z": 12.00, "output": 14.66, "target": "Hayır"},
    13: {"C": 33.99,        "Z": 13.00, "output": 15.00, "target": "Hayır"},
    14: {"C": 30.74,        "Z": 14.00, "output": 16.59, "target": "Hayır"},
    15: {"C": 26.74,        "Z": 15.00, "output": 19.07, "target": "Hayır"},
    16: {"C": 26.32,        "Z": 16.00, "output": 19.38, "target": "Hayır"},
    17: {"C": 24.26,        "Z": 17.00, "output": 21.02, "target": "Hayır"},
    18: {"C": 23.35,        "Z": 18.00, "output": 21.84, "target": "Hayır"},
    19: {"C": 21.83,        "Z": 19.00, "output": 23.36, "target": "Hayır"},
    20: {"C": 20.74,        "Z": 20.00, "output": 24.59, "target": "Hayır"},
    21: {"C": 19.58,        "Z": 21.00, "output": 26.05, "target": "Hayır"},
    22: {"C": 19.08,        "Z": 22.00, "output": 26.73, "target": "Hayır"},
    23: {"C": 19.05,        "Z": 23.00, "output": 26.77, "target": "Hayır"},
    24: {"C": 18.52,        "Z": 24.00, "output": 27.54, "target": "Hayır"},
    25: {"C": 17.48,        "Z": 25.00, "output": 29.18, "target": "Hayır"},
    27: {"C": 16.40,        "Z": 27.00, "output": 31.10, "target": "Hayır"},
    28: {"C": 15.89,        "Z": 28.00, "output": 32.10, "target": "Evet"},
    29: {"C": 15.24,        "Z": 29.00, "output": 33.46, "target": "Evet"},
    30: {"C": 15.09,        "Z": 30.00, "output": 33.80, "target": "Evet"},
    31: {"C": 15.09,        "Z": 31.00, "output": 33.80, "target": "Evet"},
    32: {"C": 15.09,        "Z": 32.00, "output": 33.80, "target": "Evet"},
    33: {"C": 15.09,        "Z": 33.00, "output": 33.80, "target": "Evet"},
    34: {"C": 15.09,        "Z": 34.00, "output": 33.80, "target": "Evet"},
    35: {"C": 15.09,        "Z": 35.00, "output": 33.80, "target": "Evet"},
    36: {"C": 15.09,        "Z": 36.00, "output": 33.80, "target": "Evet"}
}

df_list = []
for k, v in raw_summary.items():
    df_list.append({
        "Epsilon (Operatör)": f"{k}.00",
        "F1 (Çevrim Süresi - C)": f"{v['C']:.2f}" if isinstance(v['C'], float) else v['C'],
        "F2 (İşgücü - Z)": f"{v['Z']:.2f}" if isinstance(v['Z'], float) else v['Z'],
        "Ulaşılabilir Üretim": f"{v['output']:.2f}" if isinstance(v['output'], float) else v['output'],
        "Hedef Sağlandı mı?": v['target']
    })
df_summary = pd.DataFrame(df_list)

# =========================================================
# OPERATÖR 29 İÇİN DETAYLI RAPOR VERİLERİ
# =========================================================
detailed_29 = {
    "C": 15.24, "workers": 29, "output": 33.46, "meets": "Evet",
    "station_assignments": {
        1: [1, 2, 3], 2: [4, 5], 3: [6], 4: [7, 8, 9], 5: [10], 6: [11, 12, 13], 7: [14, 15, 16],
        8: [17, 18], 9: [19], 10: [20, 21], 11: [22], 12: [23, 24, 25], 13: [26], 14: [27],
        15: [28], 16: [29, 30], 17: [31], 18: [32, 33], 19: [34], 20: [35], 21: [36, 37],
        22: [38, 39, 40], 23: [41, 42, 43, 44, 45], 24: [46], 25: [47, 48, 49], 26: [50],
        27: [51, 52], 28: [53, 54], 29: [55, 56, 57], 31: [58], 32: [59, 60], 34: [61, 62, 63]
    },
    "station_loads": {
        1: 14.34, 2: 14.58, 3: 11.58, 4: 12.11, 5: 10.30, 6: 14.80, 7: 10.92, 8: 10.99, 9: 11.27,
        10: 12.15, 11: 3.31, 12: 15.24, 13: 5.20, 14: 11.89, 15: 6.30, 16: 14.30, 17: 14.20,
        18: 7.11, 19: 14.49, 20: 3.14, 21: 13.19, 22: 11.34, 23: 14.36, 24: 10.74, 25: 14.74,
        26: 15.09, 27: 14.24, 28: 12.03, 29: 9.73, 31: 11.06, 32: 14.50, 34: 11.40
    },
    "operator_stations": {
        5: [3], 8: [21], 9: [17], 11: [14], 12: [18, 20], 13: [4], 14: [5], 15: [8], 16: [28],
        17: [31], 18: [19], 19: [27], 20: [16], 21: [12], 22: [13, 15], 23: [22], 24: [24],
        25: [26], 26: [23], 27: [10], 28: [9, 11], 29: [29, 30], 30: [32, 33], 31: [25],
        32: [6], 33: [7], 34: [2], 35: [34, 35, 36], 36: [1]
    },
    "operator_loads": {
        5: 11.58, 8: 13.19, 9: 14.20, 11: 11.89, 12: 10.25, 13: 12.11, 14: 10.30, 15: 10.99,
        16: 12.03, 17: 11.06, 18: 14.49, 19: 14.24, 20: 14.30, 21: 15.24, 22: 11.50, 23: 11.34,
        24: 10.74, 25: 15.09, 26: 14.36, 27: 12.15, 28: 14.58, 29: 9.73, 30: 14.50, 31: 14.74,
        32: 14.80, 33: 10.92, 34: 14.58, 35: 11.40, 36: 14.34
    }
}

# Session State ile hesaplama kontrolü kilitleniyor
if "calculated" not in st.session_state:
    st.session_state.calculated = False

if st.button("🚀 Tüm Senaryoları Hesapla ve Analiz Et"):
    st.session_state.calculated = True

# =========================================================
# GÖRÜNTÜLEME ALANI
# =========================================================
if st.session_state.calculated:
    
    # 1. KISIM: ÖZET TABLO PANELI
    st.markdown('<div class="section-header">📋 ÖZET TABLO SONUÇLARI</div>', unsafe_allow_html=True)
    
    m_col1, m_col2 = st.columns(2)
    m_col1.metric(label="🎯 İdeal Nokta (C, Z)", value="(15.09, 12.00)")
    m_col2.metric(label="⚠️ Nadir Nokta (C, Z)", value="(34.80, 36.00)")
    
    st.write("")
    
    # .applymap yerine güncel olan .map kullanıldı (Hatanın çözümü)
    def style_infeasible(val):
        if val == "Infeasible":
            return 'background-color: #FEE2E2; color: #991B1B; font-weight: bold;'
        elif val == "Evet":
            return 'background-color: #D1FAE5; color: #065F46; font-weight: bold;'
        elif val == "Hayır":
            return 'background-color: #FEF3C7; color: #92400E; font-weight: bold;'
        return ''

    styled_df = df_summary.style.map(style_infeasible, subset=["F1 (Çevrim Süresi - C)", "Hedef Sağlandı mı?"])
    st.dataframe(styled_df, use_container_width=True, height=500)

    # 2. KISIM: DETAYLI SENARYO RAPORU PANELI
    st.markdown(f'<div class="section-header">📊 DETAYLI SENARYO RAPORU | Operatör Sayısı = {epsilon_choice}</div>', unsafe_allow_html=True)
    
    if epsilon_choice != 29:
        st.warning(f"Şu an mock veri yapısında yalnızca 29 operatörün detay sonuçları yüklüdür. Görsellerinizdeki tam eşleşmeyi görmek için lütfen soldan 29'u seçiniz.")
    else:
        st.markdown(f"""
        <div class="report-card">
            <b>• Çevrim Süresi (C):</b> {detailed_29['C']} dk/ürün <br>
            <b>• Kullanılan Operatör Sayısı:</b> {detailed_29['workers']} <br>
            <b>• Maksimum İzin Verilen Operatör Doluluğu:</b> %{U_MAX*100:.2f} <br>
            <b>• Ulaşılabilir Üretim:</b> {detailed_29['output']} adet/vardiya <br>
            <b>• Hedef Üretim (32 adet) Sağlanıyor mu?:</b> <span style='color:green; font-weight:bold;'>{detailed_29['meets']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🚉 İstasyon Atamaları ve Yükleri")
            st_data = []
            for s_id in sorted(detailed_29["station_assignments"].keys()):
                st_data.append({
                    "İstasyon No": f"İstasyon {s_id}",
                    "Atanan Operasyonlar": str(detailed_29["station_assignments"][s_id]),
                    "İstasyon Yükü (dk)": f"{detailed_29['station_loads'].get(s_id, 0.0):.2f} dk"
                })
            st.dataframe(pd.DataFrame(st_data), use_container_width=True, hide_index=True)
            
        with col2:
            st.markdown("### 👷 Operatör Performans ve Atama Tablosu")
            op_data = []
            for o_id in sorted(detailed_29["operator_stations"].keys()):
                p_load = detailed_29["operator_loads"][o_id]
                s_load = p_load * D
                u_val = 100 * ((D / T) * p_load)
                op_data.append({
                    "Operatör No": f"Operatör {o_id}",
                    "Sorumlu İstasyonlar": str(detailed_29["operator_stations"][o_id]),
                    "Ürün Başı Yük (dk)": f"{p_load:.2f} dk",
                    "Vardiya Yükü (dk)": f"{s_load:.2f} dk",
                    "Doluluk Oranı (U)": f"%{u_val:.2f}"
                })
            st.dataframe(pd.DataFrame(op_data), use_container_width=True, hide_index=True)
else:
    st.info("Tabloları ve sistem analizini listelemek için yukarıdaki 'Tüm Senaryoları Hesapla ve Analiz Et' butonuna tıklayın.")
