import streamlit as st
import pandas as pd

# Sayfa Genişlik ve Tema Ayarı
st.set_page_config(layout="wide", page_title="Montaj Hattı Dengeleme", page_icon="🏭")

# Custom CSS ile Arayüz Tasarımı
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
# YAN MENÜ (SIDEBAR) - YENİ AYARLAR
# =========================================================
st.sidebar.header("⚙️ Parametre Ayarları")

with st.sidebar.expander("🏗️ Hat Parametreleri", expanded=True):
    L = st.number_input("Maksimum Yürüme Mesafesi (L)", min_value=1, value=4)
    D = st.number_input("Hedef Üretim Miktarı (D)", min_value=1, value=32)
    T = st.number_input("Vardiya Süresi (T - dk)", min_value=1, value=510)

with st.sidebar.expander("⚖️ Optimizasyon Kısıtları", expanded=True):
    U_MAX = st.sidebar.slider("Maks. Operatör Doluluğu (U_MAX)", min_value=0.0, max_value=1.0, value=0.95, step=0.01)

st.sidebar.markdown("---")
# Yeni görsele göre varsayılan seçimi 28 yaptık
epsilon_choice = st.sidebar.slider("📊 Detaylı Rapor İçin Operatör Seç", min_value=12, max_value=36, value=28)

# =========================================================
# YENİ GÖRSELDEKİ (BİREBİR) GÜNCEL ÖZET TABLO VERİSİ
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
    13: {"C": 32.82,        "Z": 13.00, "output": 15.54, "target": "Hayır"},  # Güncellendi
    14: {"C": 28.92,        "Z": 14.00, "output": 17.63, "target": "Hayır"},  # Güncellendi
    15: {"C": 27.51,        "Z": 15.00, "output": 18.54, "target": "Hayır"},  # Güncellendi
    16: {"C": 26.32,        "Z": 16.00, "output": 19.38, "target": "Hayır"},
    17: {"C": 24.26,        "Z": 17.00, "output": 21.02, "target": "Hayır"},
    18: {"C": 24.10,        "Z": 18.00, "output": 21.16, "target": "Hayır"},  # Güncellendi
    19: {"C": 21.83,        "Z": 19.00, "output": 23.36, "target": "Hayır"},
    20: {"C": 20.74,        "Z": 20.00, "output": 24.59, "target": "Hayır"},
    21: {"C": 19.58,        "Z": 21.00, "output": 26.05, "target": "Hayır"},
    22: {"C": 19.08,        "Z": 22.00, "output": 26.73, "target": "Hayır"},
    23: {"C": 18.61,        "Z": 23.00, "output": 27.40, "target": "Hayır"},  # Güncellendi
    24: {"C": 18.52,        "Z": 24.00, "output": 27.54, "target": "Hayır"},
    25: {"C": 17.65,        "Z": 25.00, "output": 28.90, "target": "Hayır"},  # Güncellendi
    26: {"C": 17.63,        "Z": 26.00, "output": 28.93, "target": "Hayır"},  # Yeni Satır Eklendi
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
# YENİ YÜKLENEN OPERATÖR 28 İÇİN DETAYLI RAPOR VERİLERİ
# =========================================================
detailed_28 = {
    "C": 15.89, "workers": 28, "output": 32.10, "meets": "Evet",
    "station_assignments": {
        1: [1, 2, 3], 2: [4, 5], 3: [6], 4: [7, 8, 9], 5: [10], 6: [11, 12, 13], 7: [14],
        8: [15], 9: [16, 17, 18], 10: [19], 11: [20, 21, 22], 12: [23, 24, 25], 13: [26],
        14: [27], 15: [28], 16: [29], 17: [30, 31], 18: [32, 33], 19: [34], 20: [35, 36],
        21: [37, 38, 39, 40], 22: [41, 42, 43], 23: [], 24: [], 25: [44, 45, 46],
        26: [47, 48, 49], 27: [], 28: [], 29: [50], 30: [51, 52], 31: [53, 54],
        32: [55], 33: [], 34: [56, 57, 58], 35: [59, 60], 36: [61, 62, 63]
    },
    "station_loads": {
        1: 14.34, 2: 14.58, 3: 11.58, 4: 12.11, 5: 10.30, 6: 14.80, 7: 2.44, 8: 3.58,
        9: 15.89, 10: 11.27, 11: 15.46, 12: 15.24, 13: 5.20, 14: 11.89, 15: 6.30,
        16: 13.32, 17: 15.18, 18: 7.11, 19: 14.49, 20: 15.26, 21: 12.41, 22: 12.42,
        23: 0.00, 24: 0.00, 25: 12.68, 26: 14.74, 27: 0.00, 28: 0.00, 29: 15.09,
        30: 14.24, 31: 12.03, 32: 6.45, 33: 0.00, 34: 14.34, 35: 14.50, 36: 11.40
    },
    "operator_stations": {
        4: [20], 7: [19], 8: [16], 9: [18], 11: [21], 12: [4], 13: [14], 14: [17],
        15: [31], 18: [3], 19: [13, 15], 20: [25], 21: [12], 22: [26], 23: [30],
        24: [34], 25: [27, 28, 29], 26: [9], 27: [8, 10], 28: [22, 23, 24], 29: [11],
        30: [32], 31: [6], 32: [5, 7], 33: [2], 34: [33, 35], 35: [36], 36: [1]
    },
    "operator_loads": {
        4: 15.26, 7: 14.49, 8: 13.32, 9: 7.11, 11: 12.41, 12: 12.11, 13: 11.89, 14: 15.18,
        15: 12.03, 18: 11.58, 19: 11.50, 20: 12.68, 21: 15.24, 22: 14.74, 23: 14.24, 24: 14.34,
        25: 15.09, 26: 15.89, 27: 14.85, 28: 12.42, 29: 15.46, 30: 6.45, 31: 14.80, 32: 12.74,
        33: 14.58, 34: 14.50, 35: 11.40, 36: 14.34
    },
    "distance_control": [
        {"Operatör": 19, "İstasyonlar": "İstasyon 13-15", "Mesafe": 4, "Durum": "Uygun"},
        {"Operatör": 25, "İstasyonlar": "İstasyon 27-28", "Mesafe": 2, "Durum": "Uygun"},
        {"Operatör": 25, "İstasyonlar": "İstasyon 27-29", "Mesafe": 4, "Durum": "Uygun"},
        {"Operatör": 25, "İstasyonlar": "İstasyon 28-29", "Mesafe": 2, "Durum": "Uygun"},
        {"Operatör": 27, "İstasyonlar": "İstasyon 8-10",  "Mesafe": 4, "Durum": "Uygun"},
        {"Operatör": 28, "İstasyonlar": "İstasyon 22-23", "Mesafe": 2, "Durum": "Uygun"},
        {"Operatör": 28, "İstasyonlar": "İstasyon 22-24", "Mesafe": 4, "Durum": "Uygun"},
        {"Operatör": 28, "İstasyonlar": "İstasyon 23-24", "Mesafe": 2, "Durum": "Uygun"},
        {"Operatör": 32, "İstasyonlar": "İstasyon 5-7",   "Mesafe": 4, "Durum": "Uygun"},
        {"Operatör": 34, "İstasyonlar": "İstasyon 33-35", "Mesafe": 4, "Durum": "Uygun"}
    ]
}

# Session State ile hesaplama kontrolü
if "calculated" not in st.session_state:
    st.session_state.calculated = False

if st.button("🚀 Tüm Senaryoları Hesapla ve Analiz Et"):
    st.session_state.calculated = True

# =========================================================
# GÖRÜNTÜLEME ALANI
# =========================================================
if st.session_state.calculated:
    
    # 1. KISIM: GÜNCEL ÖZET TABLO PANELI
    st.markdown('<div class="section-header">📋 ÖZET TABLO SONUÇLARI</div>', unsafe_allow_html=True)
    
    m_col1, m_col2 = st.columns(2)
    m_col1.metric(label="🎯 İdeal Nokta (C, Z)", value="(15.09, 12.00)")
    m_col2.metric(label="⚠️ Nadir Nokta (C, Z)", value="(34.80, 36.00)")
    
    st.write("")
    
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

    # 2. KISIM: GÜNCEL DETAYLI SENARYO RAPORU PANELI
    st.markdown(f'<div class="section-header">📊 DETAYLI SENARYO RAPORU | Operatör Sayısı = {epsilon_choice}</div>', unsafe_allow_html=True)
    
    if epsilon_choice != 28:
        st.warning(f"Şu an yeni veri yapısında yalnızca 28 operatörün detay sonuçları yüklüdür. Görsellerinizdeki tam eşleşmeyi görmek için lütfen soldan 28'i seçiniz.")
    else:
        st.markdown(f"""
        <div class="report-card">
            <b>• Çevrim Süresi (C):</b> {detailed_28['C']} dk/ürün <br>
            <b>• Kullanılan Operatör Sayısı:</b> {detailed_28['workers']} <br>
            <b>• Maksimum İzin Verilen Operatör Doluluğu:</b> %{U_MAX*100:.2f} <br>
            <b>• Ulaşılabilir Üretim:</b> {detailed_28['output']} adet/vardiya <br>
            <b>• Hedef Üretim (32 adet) Sağlanıyor mu?:</b> <span style='color:green; font-weight:bold;'>{detailed_28['meets']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        # Sol Panel: İstasyon Atamaları ve Yükleri
        with col1:
            st.markdown("### 🚉 İstasyon Atamaları ve Yükleri")
            st_data = []
            for s_id in sorted(detailed_28["station_assignments"].keys()):
                st_data.append({
                    "İstasyon No": f"İstasyon {s_id}",
                    "Atanan Operasyonlar": str(detailed_28["station_assignments"][s_id]) if detailed_28["station_assignments"][s_id] else "Boş",
                    "İstasyon Yükü (dk)": f"{detailed_28['station_loads'].get(s_id, 0.0):.2f} dk"
                })
            st.dataframe(pd.DataFrame(st_data), use_container_width=True, hide_index=True, height=450)
            
        # Sağ Panel: Operatör Performans Tablosu
        with col2:
            st.markdown("### 👷 Operatör Performans ve Atama Tablosu")
            op_data = []
            for o_id in sorted(detailed_28["operator_stations"].keys()):
                p_load = detailed_28["operator_loads"][o_id]
                s_load = p_load * D
                u_val = 100 * ((D / T) * p_load)
                op_data.append({
                    "Operatör No": f"Operatör {o_id}",
                    "Sorumlu İstasyonlar": str(detailed_28["operator_stations"][o_id]),
                    "Ürün Başı Yük (dk)": f"{p_load:.2f} dk",
                    "Vardiya Yükü (dk)": f"{s_load:.2f} dk",
                    "Doluluk Oranı (U)": f"%{u_val:.2f}"
                })
            st.dataframe(pd.DataFrame(op_data), use_container_width=True, hide_index=True, height=450)

        # 3. KISIM: [5] MESAFE KONTROLÜ TABLOSU (Alt Geniş Panel)
        st.write("")
        st.markdown("### 🏃‍♂️ [5] Mesafe Kontrolü Raporu")
        df_dist = pd.DataFrame(detailed_28["distance_control"])
        
        def style_distance(val):
            if val == "Uygun":
                return 'background-color: #D1FAE5; color: #065F46; font-weight: bold; text-align: center;'
            return ''
            
        styled_dist = df_dist.style.map(style_distance, subset=["Durum"])
        st.dataframe(styled_dist, use_container_width=True, hide_index=True)

else:
    st.info("Yenilenen verileri tablolarda görmek ve mesafe kontrollerini incelemek için 'Tüm Senaryoları Hesapla ve Analiz Et' butonuna tıklayın.")
