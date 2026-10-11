import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==============================================================================
# 1. KONFIGURASI HALAMAN
# ==============================================================================
st.set_page_config(
    page_title="Proyek Transaksi e-Statement Bank FSB",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. SISTEM DESAIN: ELEGAN KORPORASI TERANG (LIGHT THEME COHESION)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    
    :root {
        --font-sans: 'Geist', -apple-system, BlinkMacSystemFont, sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
        --bg-page: #f8fafc;
        --surface-white: #ffffff;
        --surface-tray: #f1f5f9;
        --border-main: #e2e8f0;
        --border-accent: #cbd5e1;
        --text-headline: #0f172a;
        --text-body: #334155;
        --text-muted: #64748b;
        --corp-blue: #0284c7;
        --corp-emerald: #059669;
        --corp-crimson: #e11d48;
        --corp-indigo: #4f46e5;
    }
    
    html, body, [class*="css"], [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: var(--font-sans);
        color: var(--text-headline);
        background-color: var(--bg-page) !important;
        letter-spacing: -0.015em;
    }
    
    /* Format Angka Tabular Monospace agar rapi sejajar */
    .tabular, [data-testid="stMetricValue"], table, td, th {
        font-variant-numeric: tabular-nums;
        letter-spacing: -0.02em;
    }
    
    /* SIDEBAR KORPORAT: Kontras Tinggi & Bersih */
    [data-testid="stSidebar"] {
        background-color: var(--surface-white) !important;
        border-right: 1px solid var(--border-main) !important;
    }
    
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: var(--text-headline) !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }
    
    /* Memperbaiki chip/tag multiselect agar rapi, berlatar abu-abu terang, teks hitam */
    [data-baseweb="tag"] {
        background-color: #f1f5f9 !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 6px !important;
        padding: 2px 6px !important;
    }
    [data-baseweb="tag"] span {
        color: #0f172a !important;
        font-weight: 500 !important;
        font-size: 12px !important;
    }
    [data-baseweb="tag"] svg {
        fill: #475569 !important;
    }
    
    /* Input dan Selectbox Kontras */
    [data-baseweb="select"], [data-baseweb="input"] {
        background-color: #ffffff !important;
        border: 1px solid var(--border-accent) !important;
        border-radius: 8px !important;
        color: #0f172a !important;
    }
    
    /* TAB BAR KORPORAT */
    button[data-baseweb="tab"] {
        font-family: var(--font-sans);
        font-size: 13.5px;
        font-weight: 600;
        color: var(--text-muted) !important;
        padding: 10px 20px;
        border-radius: 8px 8px 0 0;
        transition: all 0.2s ease;
    }
    button[aria-selected="true"] {
        color: var(--text-headline) !important;
        background: #ffffff !important;
        font-weight: 700 !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.08) !important;
        border-bottom: 3px solid var(--corp-blue) !important;
    }
    
    /* HERO HEADER CARD (Putih Elegan, Border Halus) */
    .hero-card {
        background: #ffffff;
        border: 1px solid var(--border-main);
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.04);
    }
    
    .hero-eyebrow {
        font-family: var(--font-mono);
        font-size: 11.5px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--corp-blue);
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .hero-eyebrow::before {
        content: "";
        display: inline-block;
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: var(--corp-blue);
    }
    
    .hero-title {
        font-size: 26px;
        font-weight: 800;
        color: var(--text-headline);
        margin: 0;
        letter-spacing: -0.03em;
    }
    
    .hero-desc {
        font-size: 13.5px;
        color: var(--text-body);
        margin-top: 6px;
        max-width: 76ch;
        line-height: 1.55;
    }
    
    .spec-pill {
        font-family: var(--font-mono);
        font-size: 11px;
        font-weight: 600;
        color: var(--text-body);
        background: #f8fafc;
        border: 1px solid var(--border-main);
        padding: 4px 10px;
        border-radius: 999px;
    }
    
    /* DOUBLE-BEZEL METRIC CARDS (Bento Grid) */
    .bento-shell {
        background: var(--surface-tray);
        border: 1px solid var(--border-main);
        padding: 5px;
        border-radius: 14px;
        height: 100%;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .bento-shell:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 18px -4px rgba(15, 23, 42, 0.06);
    }
    
    .bento-core {
        background: #ffffff;
        border-radius: 10px;
        padding: 16px 18px;
        border: 1px solid rgba(226, 232, 240, 0.7);
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .bento-label {
        font-family: var(--font-mono);
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--text-muted);
        margin-bottom: 4px;
    }
    
    .bento-val {
        font-size: 26px;
        font-weight: 800;
        color: var(--text-headline);
        letter-spacing: -0.03em;
        line-height: 1.15;
    }
    
    .section-title {
        font-size: 15.5px;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: var(--text-headline);
        margin-top: 20px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* CUSTOMER PROFILE CARD */
    .cust-card {
        background: #ffffff;
        border: 1px solid var(--border-main);
        border-radius: 14px;
        padding: 20px 24px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
        margin-bottom: 18px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. PEMUATAN DATA
# ==============================================================================
@st.cache_data
def load_dataset():
    df = pd.read_csv('fsb_estatement_transaction.csv')
    df['transaction_datetime'] = pd.to_datetime(df['transaction_datetime'])
    df['date'] = df['transaction_datetime'].dt.date
    df['acquirer_bank_name'] = df['acquirer_bank_name'].fillna('INTERNAL / FSB BANK').astype(str)
    df['acquirer_account_name'] = df['acquirer_account_name'].fillna('-').astype(str)
    df['acquirer_account_number'] = df['acquirer_account_number'].fillna('-').astype(str)
    df['acquirer_bank_code'] = df['acquirer_bank_code'].fillna('-').astype(str)
    return df

try:
    df_raw = load_dataset()
except Exception as e:
    st.error(f"Gagal memuat dataset: {e}. Pastikan 'fsb_estatement_transaction.csv' tersedia.")
    st.stop()

# Fungsi format Rupiah
def fmt_idr_compact(v):
    sign = "-" if v < 0 else ""
    abs_v = abs(v)
    if abs_v >= 1e9:
        return f"{sign}Rp {abs_v/1e9:.2f} M"
    elif abs_v >= 1e6:
        return f"{sign}Rp {abs_v/1e6:.1f} Jt"
    else:
        return f"{sign}Rp {abs_v:,.0f}".replace(",", ".")

def fmt_idr_full(v):
    sign = "-" if v < 0 else ""
    return f"{sign}Rp {abs(v):,.0f}".replace(",", ".")

# ==============================================================================
# 4. SIDEBAR FILTER (BERSIH & BAHASA INDONESIA)
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div style="padding: 6px 0 14px 0;">
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #0284c7; font-weight: 700; letter-spacing: 0.1em;">BANK FSB INDONESIA</div>
        <div style="font-size: 17px; font-weight: 800; color: #0f172a; letter-spacing: -0.02em;">Data Mart e-Statement</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border: none; border-top: 1px solid #e2e8f0; margin: 0 0 16px 0;'>", unsafe_allow_html=True)
    
    # Rentang Tanggal
    min_date = df_raw['date'].min()
    max_date = df_raw['date'].max()
    date_range = st.date_input(
        "Periode Transaksi",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Produk Tabungan
    all_products = sorted(df_raw['product_name'].dropna().unique())
    selected_products = st.multiselect("Produk Tabungan", options=all_products, default=all_products)
    
    # Jenis Mutasi
    all_transmodes = sorted(df_raw['trasmode_code'].dropna().unique())
    selected_transmodes = st.multiselect("Jenis Mutasi Transaksi", options=all_transmodes, default=all_transmodes)
    
    # Kanal Layanan
    all_channels = sorted(df_raw['channel'].dropna().unique())
    selected_channels = st.multiselect("Kanal Layanan", options=all_channels, default=all_channels)
    
    # Kantor Cabang
    all_branches = sorted(df_raw['branch_name'].dropna().unique())
    selected_branches = st.multiselect("Kantor Cabang", options=all_branches, default=[])
    
    st.markdown("<hr style='border: none; border-top: 1px solid #e2e8f0; margin: 20px 0 12px 0;'>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="font-size: 11.5px; color: #64748b; line-height: 1.6;">
        <strong>Lampiran Portfolio PDF:</strong><br>
        Tampilan dirancang harmonis dengan tema terang korporasi untuk dokumen presentasi profesional.
    </div>
    """, unsafe_allow_html=True)

# Eksekusi Filter Data
df_filtered = df_raw.copy()

if isinstance(date_range, tuple) and len(date_range) == 2:
    s_date, e_date = date_range
    df_filtered = df_filtered[(df_filtered['date'] >= s_date) & (df_filtered['date'] <= e_date)]

if selected_products:
    df_filtered = df_filtered[df_filtered['product_name'].isin(selected_products)]

if selected_transmodes:
    df_filtered = df_filtered[df_filtered['trasmode_code'].isin(selected_transmodes)]

if selected_channels:
    df_filtered = df_filtered[df_filtered['channel'].isin(selected_channels)]

if selected_branches:
    df_filtered = df_filtered[df_filtered['branch_name'].isin(selected_branches)]

# ==============================================================================
# 5. HEADER UTAMA (JUDUL RESMI PROYEK - BAHASA INDONESIA)
# ==============================================================================
st.markdown("""
<div class="hero-card">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 14px;">
        <div>
            <div class="hero-eyebrow">PORTFOLIO DATA MART & ANALISIS TRANSAKSI PERBANKAN</div>
            <h1 class="hero-title">Proyek Transaksi e-Statement Bank FSB</h1>
            <div class="hero-desc">
                Pengembangan data mart transaksi perbankan terintegrasi: pembersihan data, rekonsiliasi biaya admin, penelusuran bank acquirer, serta kalkulasi saldo berjalan secara kronologis untuk penyediaan rekening koran digital (e-Statement).
            </div>
            <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 14px;">
                <span class="spec-pill">1.339 Transaksi Valid</span>
                <span class="spec-pill">123 Nasabah Terverifikasi</span>
                <span class="spec-pill">74 Kantor Cabang</span>
                <span class="spec-pill">Model Star Schema</span>
                <span class="spec-pill">Running Balance Engine</span>
            </div>
        </div>
        <div style="text-align: right;">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #047857; background: #ecfdf5; border: 1px solid #a7f3d0; padding: 6px 14px; border-radius: 999px; font-weight: 700; display: inline-flex; align-items: center; gap: 6px;">
                <span style="width: 6px; height: 6px; border-radius: 50%; background: #059669;"></span>
                PORTFOLIO READY
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 6. TAB NAVIGASI
# ==============================================================================
tab_exec, tab_account, tab_channel, tab_arch = st.tabs([
    "Ringkasan Eksekutif",
    "Rekening & e-Statement Nasabah",
    "Kanal & Jaringan Interbank",
    "Arsitektur Pipeline ETL"
])

# Template Standar Plotly Tema Terang Kontras Tinggi
PLOTLY_LIGHT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Geist, sans-serif', color='#1e293b', size=11.5),
    margin=dict(l=15, r=15, t=30, b=15)
)

# ==============================================================================
# TAB 1: RINGKASAN EKSEKUTIF (BENTO GRID METRICS)
# ==============================================================================
with tab_exec:
    tot_tx = len(df_filtered)
    tot_inflow = df_filtered['credit_amount'].sum()
    tot_outflow = df_filtered['debit_amount'].sum()
    net_liquidity = tot_inflow - tot_outflow
    tot_fees = df_filtered['additional_fee'].sum()
    
    # Bento Row Metrik
    c1, c2, c3 = st.columns([5, 4, 3])
    
    with c1:
        net_color = "#059669" if net_liquidity >= 0 else "#e11d48"
        st.markdown(f"""
        <div class="bento-shell">
            <div class="bento-core" style="background: linear-gradient(135deg, #ffffff 60%, #f0fdf4 100%);">
                <div>
                    <div class="bento-label">Surplus Arus Kas Bersih (Net Inflow)</div>
                    <div class="bento-val" style="color: {net_color}; font-size: 30px;">{fmt_idr_compact(net_liquidity)}</div>
                </div>
                <div style="margin-top: 14px;">
                    <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px; color: #475569;">
                        <span>Rasio Penyerapan Arus Kas</span>
                        <span style="font-family: 'JetBrains Mono'; font-weight: 700; color: #0f172a;">{(tot_outflow / tot_inflow * 100 if tot_inflow else 0):.1f}% diserap</span>
                    </div>
                    <div style="height: 6px; background: #e2e8f0; border-radius: 999px; overflow: hidden;">
                        <div style="height: 100%; width: {min(100, (tot_outflow / tot_inflow * 100 if tot_inflow else 0)):.1f}%; background: linear-gradient(90deg, #059669, #0284c7); border-radius: 999px;"></div>
                    </div>
                    <div style="font-size: 12px; color: #64748b; margin-top: 8px;">Total kredit masuk berhasil menutupi debet operasional.</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
        <div class="bento-shell">
            <div class="bento-core">
                <div>
                    <div class="bento-label">Arus Kas Masuk vs Keluar</div>
                    <div style="display: flex; gap: 18px; margin-top: 4px;">
                        <div>
                            <div style="font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: 600;">Uang Masuk (Kredit)</div>
                            <div style="font-size: 20px; font-weight: 800; color: #059669;" class="tabular">{fmt_idr_compact(tot_inflow)}</div>
                        </div>
                        <div style="border-left: 1px solid #e2e8f0; padding-left: 18px;">
                            <div style="font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: 600;">Uang Keluar (Debit)</div>
                            <div style="font-size: 20px; font-weight: 800; color: #e11d48;" class="tabular">{fmt_idr_compact(tot_outflow)}</div>
                        </div>
                    </div>
                </div>
                <div style="font-size: 12px; color: #475569; margin-top: 8px;">
                    Total Aktivitas: <strong style="color: #0f172a;">{tot_tx:,}</strong> transaksi tercatat
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"""
        <div class="bento-shell">
            <div class="bento-core">
                <div>
                    <div class="bento-label">Pendapatan Biaya Admin (Fee)</div>
                    <div class="bento-val" style="color: #0284c7;">{fmt_idr_compact(tot_fees)}</div>
                </div>
                <div style="font-size: 12px; color: #64748b; margin-top: 8px;">
                    <span style="font-family: 'JetBrains Mono';">Restrukturisasi kode TRX092</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    
    # Chart Row 1: Tren & Donut
    col_gr1, col_gr2 = st.columns([7, 5])
    
    with col_gr1:
        st.markdown("<div class='section-title'>Tren Harian Arus Kas Masuk vs Keluar</div>", unsafe_allow_html=True)
        daily = df_filtered.groupby('date').agg({
            'credit_amount': 'sum',
            'debit_amount': 'sum'
        }).reset_index()
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Bar(
            x=daily['date'],
            y=daily['credit_amount'],
            name='Uang Masuk (Kredit)',
            marker_color='#059669',
            marker_line_width=0
        ))
        fig_trend.add_trace(go.Bar(
            x=daily['date'],
            y=daily['debit_amount'],
            name='Uang Keluar (Debit)',
            marker_color='#e11d48',
            marker_line_width=0
        ))
        fig_trend.update_layout(
            **PLOTLY_LIGHT,
            height=320,
            barmode='group',
            bargroupgap=0.1,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11, color='#0f172a')),
            xaxis=dict(showgrid=False, linecolor='#cbd5e1', tickfont=dict(color='#0f172a', size=10)),
            yaxis=dict(showgrid=True, gridcolor='#f1f5f9', linecolor='#cbd5e1', tickfont=dict(color='#0f172a', size=10))
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_gr2:
        st.markdown("<div class='section-title'>Proporsi Jenis Mutasi (Trasmode Code)</div>", unsafe_allow_html=True)
        mode_counts = df_filtered['trasmode_code'].value_counts().reset_index()
        mode_counts.columns = ['mode', 'count']
        
        fig_donut = px.pie(
            mode_counts,
            values='count',
            names='mode',
            hole=0.6,
            color_discrete_sequence=['#0284c7', '#059669', '#6366f1', '#d97706', '#ec4899', '#64748b']
        )
        fig_donut.update_layout(
            **PLOTLY_LIGHT,
            height=320,
            legend=dict(orientation="v", yanchor="middle", y=0.5, font=dict(size=11, color='#0f172a'))
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent')
        st.plotly_chart(fig_donut, use_container_width=True)
        
    # Chart Row 2: Perputaran Produk & Kanal
    col_gr3, col_gr4 = st.columns([6, 6])
    
    with col_gr3:
        st.markdown("<div class='section-title'>Perputaran Dana per Produk Tabungan</div>", unsafe_allow_html=True)
        prod_agg = df_filtered.groupby('product_name').agg({
            'credit_amount': 'sum',
            'debit_amount': 'sum',
            'transaction_id': 'count'
        }).reset_index()
        prod_agg['turnover'] = prod_agg['credit_amount'] + prod_agg['debit_amount']
        
        fig_prod = px.bar(
            prod_agg,
            x='product_name',
            y='turnover',
            text=prod_agg['turnover'].apply(fmt_idr_compact),
            color='product_name',
            color_discrete_sequence=['#0284c7', '#059669', '#d97706', '#7c3aed']
        )
        fig_prod.update_layout(
            **PLOTLY_LIGHT,
            showlegend=False,
            height=290,
            xaxis=dict(showgrid=False, title=None, tickfont=dict(color='#0f172a', size=11, family='Geist, sans-serif')),
            yaxis=dict(showgrid=True, gridcolor='#f1f5f9', title=None, tickfont=dict(color='#475569', size=10))
        )
        fig_prod.update_traces(textposition='outside', textfont=dict(color='#0f172a', size=11, family='Geist, sans-serif'))
        st.plotly_chart(fig_prod, use_container_width=True)
        
    with col_gr4:
        st.markdown("<div class='section-title'>Dominasi Penggunaan Kanal Layanan</div>", unsafe_allow_html=True)
        ch_counts = df_filtered['channel'].value_counts().reset_index()
        ch_counts.columns = ['channel', 'count']
        
        fig_ch = px.bar(
            ch_counts,
            x='count',
            y='channel',
            orientation='h',
            color='count',
            color_continuous_scale='Blues',
            text='count'
        )
        fig_ch.update_layout(
            **PLOTLY_LIGHT,
            height=290,
            coloraxis_showscale=False,
            xaxis=dict(showgrid=True, gridcolor='#f1f5f9', title=None, tickfont=dict(color='#475569', size=10)),
            yaxis=dict(categoryorder='total ascending', title=None, tickfont=dict(color='#0f172a', size=11, family='Geist, sans-serif'))
        )
        fig_ch.update_traces(textposition='outside', textfont=dict(color='#0f172a', size=11, family='Geist, sans-serif'))
        st.plotly_chart(fig_ch, use_container_width=True)

# ==============================================================================
# TAB 2: REKENING & E-STATEMENT NASABAH
# ==============================================================================
with tab_account:
    st.markdown("<div class='section-title'>Buku Rekening Koran & Audit Saldo Nasabah</div>", unsafe_allow_html=True)
    
    accounts_avail = sorted(df_filtered['account_number'].unique())
    if not accounts_avail:
        st.info("Tidak ada rekening yang sesuai dengan filter saat ini.")
    else:
        acc_dict = {}
        for acc in accounts_avail:
            first_row = df_raw[df_raw['account_number'] == acc].iloc[0]
            acc_dict[acc] = f"{acc} — {first_row['customer_name']} [{first_row['product_name']}]"
            
        selected_acc = st.selectbox(
            "Pilih Nomor Rekening Nasabah:",
            options=accounts_avail,
            format_func=lambda x: acc_dict.get(x, str(x))
        )
        
        acc_history = df_raw[df_raw['account_number'] == selected_acc].sort_values('transaction_datetime').copy()
        cust_profile = acc_history.iloc[0]
        latest_record = acc_history.iloc[-1]
        
        # Kartu Profil Nasabah
        st.markdown(f"""
        <div class="cust-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px;">
                <div>
                    <div style="font-family: 'JetBrains Mono'; font-size: 11px; color: #0284c7; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700;">CIF: {cust_profile['cif_number']}</div>
                    <h2 style="font-size: 22px; font-weight: 800; color: #0f172a; margin: 2px 0 6px 0; letter-spacing: -0.02em;">{cust_profile['customer_name']}</h2>
                    <div style="font-size: 13px; color: #475569;">
                        {cust_profile['product_name']} • Cabang: {cust_profile['branch_name']}
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 11px; text-transform: uppercase; color: #64748b; font-weight: 600;">Saldo Terakhir</div>
                    <div style="font-size: 26px; font-weight: 800; color: #059669;" class="tabular">{fmt_idr_full(latest_record['balance'])}</div>
                    <div style="font-size: 11px; color: #64748b; margin-top: 2px;">
                        Buka Rekening: {cust_profile['account_open_date']} • Usia: {latest_record['account_aging']} hari
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Grafik Saldo Berjalan
        st.markdown("<div class='section-title'>Grafik Perkembangan Saldo Berjalan (Running Balance)</div>", unsafe_allow_html=True)
        fig_bal = px.line(
            acc_history,
            x='transaction_datetime',
            y='balance',
            markers=True
        )
        fig_bal.update_traces(
            line_color='#0284c7',
            line_width=2.5,
            marker=dict(size=6, color='#0369a1', line=dict(width=1, color='#ffffff'))
        )
        fig_bal.update_layout(
            **PLOTLY_LIGHT,
            height=260,
            xaxis=dict(showgrid=True, gridcolor='#f1f5f9', title=None, tickfont=dict(color='#0f172a', size=10)),
            yaxis=dict(showgrid=True, gridcolor='#f1f5f9', title=None, tickfont=dict(color='#0f172a', size=10))
        )
        st.plotly_chart(fig_bal, use_container_width=True)
        
        # Tabel Mutasi Formal
        st.markdown("<div class='section-title'>Buku Mutasi Transaksi e-Statement</div>", unsafe_allow_html=True)
        cols_ledger = [
            'transaction_datetime', 'transaction_desc', 'trasmode_code',
            'channel', 'credit_amount', 'debit_amount', 'additional_fee',
            'balance', 'acquirer_bank_name', 'transaction_remark'
        ]
        
        tbl_show = acc_history[cols_ledger].copy()
        tbl_show.columns = [
            'Waktu Transaksi', 'Keterangan', 'Jenis Mutasi', 'Kanal',
            'Kredit (Rp)', 'Debit (Rp)', 'Biaya Admin (Rp)',
            'Saldo Akhir (Rp)', 'Bank Lawan', 'Remark Transaksi'
        ]
        
        st.dataframe(
            tbl_show.style.format({
                'Kredit (Rp)': '{:,.0f}',
                'Debit (Rp)': '{:,.0f}',
                'Biaya Admin (Rp)': '{:,.0f}',
                'Saldo Akhir (Rp)': '{:,.0f}'
            }),
            use_container_width=True,
            height=280
        )
        
        csv_download = tbl_show.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"Unduh e-Statement Rekening {selected_acc} (.CSV)",
            data=csv_download,
            file_name=f"estatement_FSB_{selected_acc}.csv",
            mime="text/csv"
        )

# ==============================================================================
# TAB 3: KANAL & JARINGAN INTERBANK
# ==============================================================================
with tab_channel:
    st.markdown("<div class='section-title'>Jaringan Kliring Antarbank & Analisis Cabang</div>", unsafe_allow_html=True)
    
    col_net_a, col_net_b = st.columns(2)
    
    with col_net_a:
        st.markdown("<div class='section-title'>Top 10 Bank Tujuan / Acquirer</div>", unsafe_allow_html=True)
        outgoing = df_filtered[df_filtered['acquirer_bank_name'] != 'INTERNAL / FSB BANK']
        top_banks = outgoing['acquirer_bank_name'].value_counts().head(10).reset_index()
        top_banks.columns = ['bank', 'tx_count']
        
        fig_tb = px.bar(
            top_banks,
            x='tx_count',
            y='bank',
            orientation='h',
            text='tx_count',
            color='tx_count',
            color_continuous_scale='Blues'
        )
        fig_tb.update_layout(
            **PLOTLY_LIGHT,
            height=340,
            coloraxis_showscale=False,
            xaxis=dict(showgrid=True, gridcolor='#f1f5f9', title=None, tickfont=dict(color='#475569', size=10)),
            yaxis=dict(categoryorder='total ascending', title=None, tickfont=dict(color='#0f172a', size=11, family='Geist, sans-serif'))
        )
        fig_tb.update_traces(textposition='outside', textfont=dict(color='#0f172a', size=11, family='Geist, sans-serif'))
        st.plotly_chart(fig_tb, use_container_width=True)
        
    with col_net_b:
        st.markdown("<div class='section-title'>Top 10 Kantor Cabang Berdasarkan Volume</div>", unsafe_allow_html=True)
        top_br = df_filtered['branch_name'].value_counts().head(10).reset_index()
        top_br.columns = ['branch', 'tx_count']
        
        fig_br = px.bar(
            top_br,
            x='tx_count',
            y='branch',
            orientation='h',
            text='tx_count',
            color='tx_count',
            color_continuous_scale='Purples'
        )
        fig_br.update_layout(
            **PLOTLY_LIGHT,
            height=340,
            coloraxis_showscale=False,
            xaxis=dict(showgrid=True, gridcolor='#f1f5f9', title=None, tickfont=dict(color='#475569', size=10)),
            yaxis=dict(categoryorder='total ascending', title=None, tickfont=dict(color='#0f172a', size=11, family='Geist, sans-serif'))
        )
        fig_br.update_traces(textposition='outside', textfont=dict(color='#0f172a', size=11, family='Geist, sans-serif'))
        st.plotly_chart(fig_br, use_container_width=True)
        
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    col_dem1, col_dem2 = st.columns(2)
    with col_dem1:
        st.markdown("<div class='section-title'>Distribusi Gender Nasabah</div>", unsafe_allow_html=True)
        g_df = df_filtered.groupby('gender')['cif_number'].nunique().reset_index()
        g_df.columns = ['gender', 'nasabah']
        g_df['gender'] = g_df['gender'].map({'M': 'Pria', 'F': 'Wanita'}).fillna(g_df['gender'])
        
        fig_g = px.pie(
            g_df,
            names='gender',
            values='nasabah',
            color='gender',
            color_discrete_map={'Pria': '#0284c7', 'Wanita': '#e11d48'}
        )
        fig_g.update_layout(**PLOTLY_LIGHT, height=220, legend=dict(font=dict(color='#0f172a', size=11)))
        st.plotly_chart(fig_g, use_container_width=True)
        
    with col_dem2:
        st.markdown("<div class='section-title'>Sebaran Usia Hubungan Rekening (Account Aging)</div>", unsafe_allow_html=True)
        aging = df_filtered.groupby('account_number')['account_aging'].first()
        fig_ag = px.histogram(
            aging,
            nbins=18,
            color_discrete_sequence=['#4f46e5']
        )
        fig_ag.update_layout(
            **PLOTLY_LIGHT,
            height=220,
            xaxis=dict(title="Hari Beroperasi", tickfont=dict(color='#0f172a', size=10)),
            yaxis=dict(title="Jumlah Akun", tickfont=dict(color='#0f172a', size=10))
        )
        st.plotly_chart(fig_ag, use_container_width=True)

# ==============================================================================
# TAB 4: ARSITEKTUR PIPELINE ETL
# ==============================================================================
with tab_arch:
    st.markdown("<div class='section-title'>Metodologi Rekayasa Data & Pemodelan Data Mart</div>", unsafe_allow_html=True)
    
    p1, p2 = st.columns(2)
    with p1:
        st.markdown("""
        <div class="bento-shell">
            <div class="bento-core">
                <div class="bento-label">1. Standarisasi & Pembersihan</div>
                <ul style="font-size: 13px; color: #334155; line-height: 1.7; padding-left: 18px; margin: 8px 0;">
                    <li><strong>Konversi Julian Date:</strong> Format <code>YYYYDDD</code> (contoh: <code>2025213</code>) dikonversi ke kalender ISO-8601 standar dan digabungkan dengan waktu integer 6-digit menjadi <code>datetime</code> presisi.</li>
                    <li><strong>Restrukturisasi Biaya (TRX092):</strong> Mutasi fee dipisahkan dari transaksi mandiri dan dipetakan ke transaksi induk via kolom <code>additional_fee</code> agar tidak terjadi penggandaan volume debit.</li>
                    <li><strong>Deteksi Overbooking:</strong> Membedakan transaksi internal antar-rekening FSB dengan transfer bank eksternal berbasis pengulangan <code>transaction_reference</code>.</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with p2:
        st.markdown("""
        <div class="bento-shell">
            <div class="bento-core">
                <div class="bento-label">2. Desain Skema Bintang (Star Schema)</div>
                <ul style="font-size: 13px; color: #334155; line-height: 1.7; padding-left: 18px; margin: 8px 0;">
                    <li><strong>Tabel Fakta:</strong> <code>f_estatement_transaction</code> (1.339 baris terverifikasi, 31 kolom metrik keuangan).</li>
                    <li><strong>Tabel Dimensi:</strong> Terintegrasi dengan <code>dim_account</code>, <code>dim_customer</code>, <code>dim_branch</code>, <code>dim_transaction_code</code>, dan <code>dim_bank_code</code>.</li>
                    <li><strong>Jaminan Kualitas Data:</strong> Eliminasi duplikasi primary key 100% dan standardisasi tipe data string pada kode bank.</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Pratinjau Tabel Fakta Akhir (`fsb_estatement_transaction.csv`)</div>", unsafe_allow_html=True)
    st.dataframe(df_filtered.head(8), use_container_width=True)

# ==============================================================================
# 7. FOOTER
# ==============================================================================
st.markdown("<hr style='border: none; border-top: 1px solid #e2e8f0; margin: 32px 0 16px 0;'>", unsafe_allow_html=True)
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; font-size: 12px; color: #64748b;">
    <div>
        <strong>Studi Kasus Analisis Perbankan FSB</strong> — End-to-End Data Engineering & Business Intelligence
    </div>
    <div style="font-family: 'JetBrains Mono', monospace;">
        Stack: Python • Pandas • NumPy • Plotly • Streamlit • Star Schema
    </div>
</div>
""", unsafe_allow_html=True)
