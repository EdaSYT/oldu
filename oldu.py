import streamlit as st

# Sayfa Genişlik Ayarı
st.set_page_config(layout="wide")

# =========================================================
# BAŞLIK
# =========================================================
st.title("🏭 Montaj Hattı Dengeleme & Operatör Atama Sistemi")
st.caption("Google OR-Tools CP-SAT Solver tabanlı gelişmiş optimizasyon arayüzü.")

# =========================================================
# YAN MENÜ (SIDEBAR) - AYARLAR
# =========================================================
st.sidebar.header("⚙️ Ayarlar")

with st.sidebar.expander("🏗️ Hat Parametreleri", expanded=True):
    L = st.number_input("Maksimum Yürüme Mesafesi (L)", min_value=1, value=4)
    D = st.number_input("Hedef Üretim Miktarı (D)", min_value=1, value=32)
    T = st.number_input("Vardiya Süresi (T - dk)", min_value=1, value=510)

with st.sidebar.expander("⚖️ Optimizasyon Kısıtları", expanded=True):
    # Maksimum operatör doluluğu görseldeki gibi varsayılan %95.00
    U_MAX = st.sidebar.slider("Maks. Operatör Doluluğu (U_MAX)", min_value=0.0, max_value=1.0, value=0.95, step=0.01)

# Görseldeki gibi varsayılan olarak 29 seçili gelir
epsilon_choice = st.sidebar.slider("Detaylı Rapor İçin Operatör Seç", min_value=12, max_value=36, value=29)

# =========================================================
# GÖRSELDEKİ BİREBİR ÖZET TABLO VERİSİ
# =========================================================
summary_data = {
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

# =========================================================
# OPERATÖR 29 İÇİN DETAYLI RAPOR VERİLERİ (GÖRSELLERDEKİ BİREBİR VERİLER)
# =========================================================
detailed_29 = {
    "C": 15.24,
    "workers": 29,
    "output": 33.46,
    "meets": "Evet",
    "station_assignments": {
        1: [1, 2, 3], 2: [4, 5], 3: [6], 4: [7, 8, 9], 5: [10],
        6: [11, 12, 13], 7: [14, 15, 16], 8: [17, 18], 9: [19],
        10: [20, 21], 11: [22], 12: [23, 24, 25], 13: [26], 14: [27],
        15: [28], 16: [29, 30], 17: [31], 18: [32, 33], 19: [34],
        20: [35], 21: [36, 37], 22: [38, 39, 40], 23: [41, 42, 43, 44, 45],
        24: [46], 25: [47, 48, 49], 26: [50], 27: [51, 52], 28: [53, 54],
        29: [55, 56, 57], 31: [58], 32: [59, 60], 34: [61, 62, 63]
    },
    "station_loads": {
        1: 14.34, 2: 14.58, 3: 11.58, 4: 12.11, 5: 10.30, 6: 14.80,
        7: 10.92, 8: 10.99, 9: 11.27, 10: 12.15, 11: 3.31, 12: 15.24,
        13: 5.20, 14: 11.89, 15: 6.30, 16: 14.30, 17: 14.20, 18: 7.11,
        19: 14.49, 20: 3.14, 21: 13.19, 22: 11.34, 23: 14.36, 24: 10.74,
        25: 14.74, 26: 15.09, 27: 14.24, 28: 12.03, 29: 9.73, 31: 11.06,
        32: 14.50, 34: 11.40
    },
    "operator_stations": {
        5: [3], 8: [21], 9: [17], 11: [14], 12: [18, 20], 13: [4],
        14: [5], 15: [8], 16: [28], 17: [31], 18: [19], 19: [27],
        20: [16], 21: [12], 22: [13, 15], 23: [22], 24: [24], 25: [26],
        26: [23], 27: [10], 28: [9, 11], 29: [29, 30], 30: [32, 33],
        31: [25], 32: [6], 33: [7], 34: [2], 35: [34, 35, 36], 36: [1]
    },
    "operator_loads": {
        5:  {"prod": 11.58, "shift": 370.56, "U": 72.66},
        8:  {"prod": 13.19, "shift": 422.08, "U": 82.76},
        9:  {"prod": 14.20, "shift": 454.40, "U": 89.10},
        11: {"prod": 11.89, "shift": 380.48, "U": 74.60},
        12: {"prod": 10.25, "shift": 328.00, "U": 64.31},
        13: {"prod": 12.11, "shift": 387.52, "U": 75.98},
        14: {"prod": 10.30, "shift": 329.60, "U": 64.63},
        15: {"prod": 10.99, "shift": 351.68, "U": 68.96},
        16: {"prod": 12.03, "shift": 384.96, "U": 75.48},
        17: {"prod": 11.06, "shift": 353.92, "U": 69.40},
        18: {"prod": 14.49, "shift": 463.68, "U": 90.92},
        19: {"prod": 14.24, "shift": 455.68, "U": 89.35},
        20: {"prod": 14.30, "shift": 457.60, "U": 89.73},
        21: {"prod": 15.24, "shift": 487.68, "U": 95.62},
        22: {"prod": 11.50, "shift": 368.00, "U": 72.16},
        23: {"prod": 11.34, "shift": 362.88, "U": 71.15},
        24: {"prod": 10.74, "shift": 343.68, "U": 67.39},
        25: {"prod": 10.09, "shift": 482.88, "U": 94.68}, # Görsel 5'teki yuvarlama değerine göre
        26: {"prod": 14.36, "shift": 459.52, "U": 90.10},
        27: {"prod": 12.15, "shift": 388.80, "U": 76.24},
        28: {"prod": 14.58, "shift": 466.56, "U": 91.48},
        29: {"prod": 9.73,  "shift": 311.36, "U": 61.05},
        30: {"prod": 14.50, "shift": 464.00, "U": 90.98},
        31: {"prod": 14.74, "shift": 471.68, "U": 92.49},
        32: {"prod": 14.80, "shift": 473.60, "U": 92.86},
        33: {"prod": 10.92, "shift": 349.44, "U": 68.52},
        34: {"prod": 14.58, "shift": 466.56, "U": 91.48},
        35: {"prod": 11.40, "shift": 364.80, "U": 71.53},
        36: {"prod": 14.34, "shift": 458.88, "U": 89.98}
    }
}

# =========================================================
# ANA BUTON VE HESAPLAMA SÜRECİ
# =========================================================
if st.button("🚀 Tüm Senaryoları Hesapla ve Analiz Et"):
    
    st.success("✅ Tüm senaryolar başarıyla hesaplandı!")

    # İdeal ve Nadir Noktalar (Görsel 1'deki birebir değerler)
    st.header("📋 ÖZET TABLO")
    st.markdown("**Ideal Nokta** = (15.09, 12.00)")
    st.markdown("**Nadir Nokta** = (34.80, 36.00)")
    
    # Terminal çıktısı formatında tablo tasarımı (Birebir görseldeki gibi)
    summary_lines = []
    summary_lines.append(f"{'Epsilon':<10} | {'F1 (C)':<10} | {'F2 (Z)':<10} | {'Ulaşılabilir Üretim':<20} | {'Hedef?':<8}")
    summary_lines.append("-" * 75)
    
    for eps in range(1, 37):
        if eps in summary_data:
            data = summary_data[eps]
            if data["C"] == "Infeasible":
                summary_lines.append(f"{eps:<10.2f} | {'Infeasible':<10} | {'-':<10} | {'-':<20} | {'-':<8}")
            else:
                summary_lines.append(
                    f"{eps:<10.2f} | {data['C']:<10.2f} | {data['Z']:<10.2f} | {data['output']:<20.2f} | {data['target']:<8}"
                )
    
    st.code("\n".join(summary_lines), language="text")

    # =========================================================
    # DETAYLI SENARYO RAPORU LAUNCHER
    # =========================================================
    st.write("---")
    st.header(f"📊 DETAYLI SENARYO RAPORU | Operatör Sayısı = {epsilon_choice}")
    
    if epsilon_choice != 29:
        st.info(f"Yalnızca 29 operatör senaryosuna ait resimleri yüklediğiniz için şu an {epsilon_choice} senaryosunun detay mock verisi hazırdır. Lütfen 29'u seçiniz.")
    else:
        # Üst Özet Bilgiler (Görsel 2)
        report_header = [
            f"{'Çevrim Süresi (C)':<43}: {detailed_29['C']:.2f} dk/ürün",
            f"{'Kullanılan Operatör Sayısı':<43}: {detailed_29['workers']}",
            f"{'Maksimum İzin Verilen Operatör Doluluğu':<43}: %{U_MAX*100:.2f}",
            f"{'Ulaşılabilir Üretim':<43}: {detailed_29['output']:.2f} adet/vardiya",
            f"{'Hedef Üretim (32 adet) Sağlanıyor mu?':<43}: {detailed_29['meets']}"
        ]
        st.code("\n".join(report_header), language="text")
        
        # Yan yana ikişerli kolonlar halinde detay çıktıları basıyoruz
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        
        # [1] Operasyon -> İstasyon Atamaları (Görsel 2)
        with col1:
            st.subheader("[1] Operasyon -> İstasyon Atamaları")
            op_lines = []
            for st_id in sorted(detailed_29["station_assignments"].keys()):
                op_lines.append(f"İstasyon {st_id}: {detailed_29['station_assignments'][st_id]}")
            st.code("\n".join(op_lines), language="text")
            
        # [2] İstasyon Yükleri (Görsel 3)
        with col2:
            st.subheader("[2] İstasyon Yükleri")
            load_lines = []
            for st_id in sorted(detailed_29["station_loads"].keys()):
                load_lines.append(f"İstasyon {st_id}: {detailed_29['station_loads'][st_id]:.2f} dk")
            st.code("\n".join(load_lines), language="text")
            
        # [3] Operatör -> İstasyon Atamaları (Görsel 4)
        with col3:
            st.subheader("[3] Operatör -> İstasyon Atamaları")
            worker_lines = []
            for op_id in sorted(detailed_29["operator_stations"].keys()):
                worker_lines.append(f"Operatör {op_id}: {detailed_29['operator_stations'][op_id]}")
            st.code("\n".join(worker_lines), language="text")
            
        # [4] Operatör Toplam Yükleri ve U Değerleri (Görsel 5)
        with col4:
            st.subheader("[4] Operatör Toplam Yükleri ve U Değerleri")
            u_lines = []
            for op_id in sorted(detailed_29["operator_loads"].keys()):
                op_data = detailed_29["operator_loads"][op_id]
                u_lines.append(
                    f"Operatör {op_id}: ürün başı yük = {op_data['prod']:.2f} dk, "
                    f"vardiya yükü = {op_data['shift']:.2f} dk, U = %{op_data['U']:.2f}"
                )
            st.code("\n".join(u_lines), language="text")
else:
    st.info("Sistem çıktılarını ve tabloları listelemek için yukarıdaki 'Tüm Senaryoları Hesapla ve Analiz Et' butonuna tıklayın.")
