import os
import tempfile
import sqlite3
from datetime import datetime
import streamlit as st
import matplotlib.pyplot as plt
st.set_page_config(page_title='Voxie', layout='wide', initial_sidebar_state='expanded')
from detector import DeepfakeDetector
from watermark import detect_watermark, embed_watermark
from decision import generate_verdict
from forensics import analyze_biological_markers
from database import init_db, save_analysis, fetch_all_history, clear_history
init_db()

@st.cache_resource(show_spinner="Downloading AI Model (~1.2GB) for the first time... This might take a few minutes depending on internet speed.")
def load_model() -> DeepfakeDetector:
    return DeepfakeDetector()
try:
    detector_model = load_model()
except Exception as e:
    st.error(f'Initialization failed: {e}')
    st.stop()

def inject_css():
    st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Syne:wght@600;700;800&display=swap');
    
    :root {
        --bg: #ffffff;
        --sidebar-bg: #e6e1ff;
        --card-pink: #fbc3e0;
        --card-yellow: #e6e89a;
        --card-blue: #dee2ff;
        --card-green: #d9db81;
        --accent-purple: #85586f;
        --btn-gold: #f3e391;
        --text: #000000;
        --border: #000000;
        --border-width: 3px;
        --radius: 24px;
        --font-main: 'Plus Jakarta Sans', sans-serif;
        --font-title: 'Syne', sans-serif;
    }
    
    .stApp {
        background-color: var(--bg);
        color: var(--text);
        font-family: var(--font-main);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg);
        border-right: var(--border-width) solid var(--border);
    }
    
    [data-testid="stSidebarNav"] {
        background-color: transparent !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* Custom Sidebar Nav Buttons */
    .st-emotion-cache-16ids0d {
        background-color: transparent !important;
        border: none !important;
    }

    /* Override Streamlit Sidebar Radio buttons to look like the image */
    div[data-testid="stSidebarUserContent"] .stRadio > div {
        gap: 12px;
    }
    
    /* Main Layout Headers */
    h1, h2, h3 {
        font-family: var(--font-title);
        font-weight: 800;
        color: var(--text);
        text-transform: none;
    }
    
    /* The "Analyze" Style Button */
    button[kind="primary"] {
        background-color: var(--btn-gold) !important;
        color: var(--text) !important;
        border: var(--border-width) solid var(--border) !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 700 !important;
        box-shadow: 4px 4px 0px 0px var(--border) !important;
        transition: all 0.1s !important;
    }
    button[kind="primary"]:active {
        transform: translate(2px, 2px) !important;
        box-shadow: 2px 2px 0px 0px var(--border) !important;
    }
    
    button[kind="secondary"] {
        background-color: #fff !important;
        color: var(--text) !important;
        border: var(--border-width) solid var(--border) !important;
        border-radius: 12px !important;
        box-shadow: 4px 4px 0px 0px var(--border) !important;
    }

    /* Cards from Mockup */
    .hero-container {
        background-color: var(--card-pink);
        border: var(--border-width) solid var(--border);
        border-radius: var(--radius);
        padding: 40px;
        margin-bottom: 24px;
        box-shadow: 6px 6px 0px 0px var(--border);
        position: relative;
        overflow: hidden;
    }
    .hero-container::after {
        content: '';
        position: absolute;
        top: -20px;
        right: -20px;
        width: 100px;
        height: 100px;
        background: rgba(0,0,0,0.05);
        border-radius: 50%;
        border: var(--border-width) solid var(--border);
    }
    
    .hero-title {
        font-size: 2.5rem;
        margin-bottom: 8px;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        font-weight: 500;
        opacity: 0.8;
    }
    
    .card-yellow {
        background-color: var(--card-yellow);
        border: var(--border-width) solid var(--border);
        border-radius: var(--radius);
        padding: 32px;
        box-shadow: 6px 6px 0px 0px var(--border);
        text-align: center;
    }
    
    .card-blue {
        background-color: var(--card-blue);
        border: var(--border-width) solid var(--border);
        border-radius: var(--radius);
        padding: 24px;
        box-shadow: 6px 6px 0px 0px var(--border);
    }
    
    .card-green {
        background-color: var(--card-green);
        border: var(--border-width) solid var(--border);
        border-radius: var(--radius);
        padding: 24px;
        box-shadow: 6px 6px 0px 0px var(--border);
        display: flex;
        align-items: center;
        gap: 20px;
    }

    /* File Uploader override */
    div[data-testid="stFileUploader"] {
        background-color: #fff;
        border: 2px dashed var(--border);
        border-radius: 16px !important;
        padding: 20px;
    }
    
    /* Metric styling */
    .metric-value {
        font-size: 3.5rem;
        font-weight: 800;
        font-family: var(--font-title);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background-color: var(--accent-purple) !important;
    }
    .stProgress > div > div > div {
        background-color: #fff !important;
        border: var(--border-width) solid var(--border) !important;
        height: 24px !important;
        border-radius: 12px !important;
    }

    /* Streamlit Widget Overrides */
    [data-testid="stWidgetLabel"] p, .stRadio label, .stFileUploader label, .stSelectbox label {
        color: #000000 !important;
        font-family: var(--font-main) !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
    }
    
    [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] span {
        color: #000000 !important;
    }

    /* Radio button text fix */
    div[data-testid="stRadio"] div[role="radiogroup"] label {
        color: #000000 !important;
    }

    .upgrade-btn {
        background-color: var(--accent-purple) !important;
        color: white !important;
        border: var(--border-width) solid var(--border) !important;
        border-radius: 12px !important;
        padding: 16px !important;
        text-align: center;
        font-weight: 700;
        box-shadow: 4px 4px 0px 0px var(--border);
        margin-top: 40px;
    }
    </style>
    ''', unsafe_allow_html=True)

def render_dashboard():
    st.markdown('''
    <div class="hero-container">
        <div class="hero-title">Voxie AI Dashboard</div>
        <div class="hero-subtitle">Dual-layer AI deepfake detection and spectral watermark verification.</div>
    </div>
    ''', unsafe_allow_html=True)
    
    history = fetch_all_history()
    total_analyses = len(history)
    high_risk_count = sum((1 for r in history if r['risk_level'] == 'High'))
    avg_score = sum((r['risk_score'] for r in history)) / total_analyses if total_analyses > 0 else 0
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown(f'''
        <div class="card-blue">
            <h3 style="margin-top:0;">System Health</h3>
            <p>Total analyses performed: <b>{total_analyses}</b></p>
            <p>Average risk detected: <b>{avg_score:.1f}%</b></p>
        </div>
        ''', unsafe_allow_html=True)
        
    with col2:
        risk_color = "var(--card-green)" if high_risk_count == 0 else "var(--card-yellow)"
        st.markdown(f'''
        <div class="card-yellow" style="background-color: {risk_color};">
            <div style="font-weight:800; text-transform:uppercase; letter-spacing:1px; margin-bottom:10px;">Security Status</div>
            <div class="metric-value">{high_risk_count}</div>
            <div style="font-weight:700;">High Risk Threats</div>
        </div>
        ''', unsafe_allow_html=True)

def render_verify():
    st.markdown('<div class="hero-container"><div class="hero-title">Scan New Audio</div><div class="hero-subtitle">Drop your recording here to detect AI synthesis with 99.8% precision.</div></div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns([1.5, 1])
    
    with c1:
        st.markdown('<div class="card-blue" style="margin-bottom:24px;">', unsafe_allow_html=True)
        source_type = st.radio("Choose audio source:", ["Upload File", "Use Sample Audio"], horizontal=True)
        audio_bytes = None
        original_filename = None
        suffix = None
        tmp_filepath = None
        
        if source_type == "Upload File":
            uploaded_file = st.file_uploader('Upload Audio File (WAV/MP3)', type=['wav', 'mp3'], label_visibility='collapsed')
            if uploaded_file is not None:
                audio_bytes = uploaded_file.getvalue()
                original_filename = uploaded_file.name
                suffix = os.path.splitext(original_filename)[1]
        else:
            sample_files = ["None", "Raman_Audio.wav", "Ai_audio.wav"]
            selected_sample = st.selectbox("Select a sample audio file", sample_files, label_visibility='collapsed')
            if selected_sample != "None":
                sample_path = os.path.join("sample_audio", selected_sample)
                if os.path.exists(sample_path):
                    with open(sample_path, "rb") as f:
                        audio_bytes = f.read()
                    original_filename = selected_sample
                    suffix = os.path.splitext(original_filename)[1]
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="card-yellow" style="height:100%;">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-top:0;">AI Probability</h3>', unsafe_allow_html=True)
        st.markdown('<div class="metric-value" style="font-size:4rem; margin:20px 0;">--%</div>', unsafe_allow_html=True)
        st.markdown('<div style="background:#fff; border:3px solid #000; border-radius:100px; padding:10px; font-weight:800;">AWAITING SCAN</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    if audio_bytes is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_filepath = tmp_file.name
            
        st.markdown('<div class="card-blue" style="margin-top: -20px; border-top: none; border-radius: 0 0 24px 24px;">', unsafe_allow_html=True)
        st.audio(audio_bytes, format=f"audio/{suffix.strip('.')}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card-blue" style="margin-top: 24px;">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-top:0;">Analysis Controls</h3>', unsafe_allow_html=True)
        embed_wm = st.checkbox('Embed watermark before analysis', key='embed_chk')
        analyze_clicked = st.button('analyze audio', type='primary', use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if analyze_clicked:
            analysis_filepath = tmp_filepath
            watermarked_tmp = None
            if embed_wm:
                with st.spinner('Embedding spectral watermark...'):
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as wt_file:
                        watermarked_tmp = wt_file.name
                    try:
                        embed_watermark(tmp_filepath, watermarked_tmp)
                        analysis_filepath = watermarked_tmp
                    except Exception as e:
                        st.error(f'Watermark embedding failed: {e}')
            
            with st.spinner('Processing deepfake classification and watermark...'):
                try:
                    with open(analysis_filepath, 'rb') as af:
                        analysis_bytes = af.read()
                        analysis_suffix = os.path.splitext(analysis_filepath)[1]
                    deepfake_label, deepfake_confidence = detector_model.detect(analysis_bytes, suffix=analysis_suffix)
                    watermark_confidence = detect_watermark(analysis_filepath)
                    forensic_results = analyze_biological_markers(analysis_filepath)
                    verdict_results = generate_verdict(deepfake_label, deepfake_confidence, watermark_confidence, forensic_results=forensic_results)
                    save_analysis(filename=original_filename, deepfake_label=deepfake_label, deepfake_confidence=deepfake_confidence, watermark_confidence=watermark_confidence, risk_score=verdict_results.get('risk_score', 0), final_verdict=verdict_results.get('final_verdict', 'Unknown'), risk_level=verdict_results.get('risk_level', 'Unknown'))
                except Exception as e:
                    st.error(f'Analysis failed: {e}')
                    st.stop()

            # Result Section
            st.markdown('<div style="margin-top: 32px;"></div>', unsafe_allow_html=True)
            risk_score = verdict_results.get('risk_score', 0.0)
            risk_level = verdict_results.get('risk_level', 'Unknown')
            final_verdict = verdict_results.get('final_verdict', 'Unknown')
            explanation = verdict_results.get('explanation', '')
            
            # Update the AI Probability Card visually if possible (Streamlit limitation, we use a new one)
            st.markdown(f'''
            <div class="card-yellow" style="margin-bottom: 24px;">
                <h3 style="margin-top:0;">Final Analysis</h3>
                <div class="metric-value" style="font-size:4rem; margin:20px 0;">{risk_score}%</div>
                <div style="background:#fff; border:3px solid #000; border-radius:100px; padding:10px; font-weight:800; text-transform:uppercase;">{risk_level} RISK</div>
            </div>
            ''', unsafe_allow_html=True)

            st.markdown(f'''
            <div class="card-green">
                <div style="background: white; border: 3px solid black; border-radius: 50%; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; font-size: 24px;">🛡️</div>
                <div>
                    <h4 style="margin:0;">Verdict: {final_verdict}</h4>
                    <p style="margin:0; font-weight: 500;">{explanation}</p>
                </div>
            </div>
            ''', unsafe_allow_html=True)

            # Forensic Details
            if forensic_results:
                st.markdown('<div style="margin-top: 24px;"></div>', unsafe_allow_html=True)
                st.markdown('<h3 style="margin-bottom:12px;">Forensic Breakdown</h3>', unsafe_allow_html=True)
                f1, f2, f3 = st.columns(3)
                with f1:
                    j_val = forensic_results.get('jitter', 0)
                    st.markdown(f'<div class="card-blue"><div style="font-size:0.8rem; font-weight:800; text-transform:uppercase;">Pitch Jitter</div><div style="font-size:1.5rem; font-weight:800;">{j_val:.4f}</div><div style="font-size:0.7rem;">(Biological randomness)</div></div>', unsafe_allow_html=True)
                with f2:
                    s_val = forensic_results.get('spectral_variance', 0)
                    st.markdown(f'<div class="card-blue"><div style="font-size:0.8rem; font-weight:800; text-transform:uppercase;">Spectral Flux</div><div style="font-size:1.5rem; font-weight:800;">{s_val:.4f}</div><div style="font-size:0.7rem;">(Timbre variation)</div></div>', unsafe_allow_html=True)
                with f3:
                    h_val = forensic_results.get('hnr_proxy', 0)
                    st.markdown(f'<div class="card-blue"><div style="font-size:0.8rem; font-weight:800; text-transform:uppercase;">HNR Proxy</div><div style="font-size:1.5rem; font-weight:800;">{h_val:.1f}</div><div style="font-size:0.7rem;">(Harmonic purity)</div></div>', unsafe_allow_html=True)

            if os.path.exists(tmp_filepath):
                try: os.remove(tmp_filepath)
                except: pass

def render_embed():
    st.markdown('<div class="section-header"><span>watermark studio</span> <span>↗</span></div>', unsafe_allow_html=True)
    st.markdown('<p style="font-weight: 600; margin-bottom: 24px; font-size: 1.1rem;">Upload an audio file to embed a secure spectral watermark. This process does not perform deepfake analysis.</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown('<div style="font-family: var(--syne); font-size: 1.5rem; font-weight: 800; margin-bottom: 12px; text-transform: lowercase;">original audio</div>', unsafe_allow_html=True)
        
        source_type = st.radio("Choose audio source:", ["Upload File", "Use Sample Audio"], horizontal=True, key="embed_src")
        audio_bytes = None
        original_filename = None
        
        if source_type == "Upload File":
            uploaded_file = st.file_uploader('Upload Audio', type=['wav', 'mp3'], key='wm_uploader', label_visibility='collapsed')
            if uploaded_file:
                audio_bytes = uploaded_file.getvalue()
                original_filename = uploaded_file.name
        else:
            sample_files = ["None", "Raman_Audio.wav", "Ai_audio.wav"]
            selected_sample = st.selectbox("Select a sample audio file", sample_files, label_visibility='collapsed', key='wm_sample')
            if selected_sample != "None":
                sample_path = os.path.join("sample_audio", selected_sample)
                if os.path.exists(sample_path):
                    with open(sample_path, "rb") as f:
                        audio_bytes = f.read()
                    original_filename = selected_sample
                else:
                    st.warning(f"Sample file {selected_sample} not found.")
                    
        gen_clicked = None
        if audio_bytes is not None:
            st.markdown('<br>', unsafe_allow_html=True)
            gen_clicked = st.button('generate watermarked audio', type='primary', use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown('<div style="font-family: var(--syne); font-size: 1.5rem; font-weight: 800; margin-bottom: 12px; text-transform: lowercase;">watermarked audio</div>', unsafe_allow_html=True)
        if audio_bytes is not None and gen_clicked:
            suffix = os.path.splitext(original_filename)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as t_in:
                t_in.write(audio_bytes)
                t_in_path = t_in.name
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as t_out:
                t_out_path = t_out.name
            with st.spinner('Embedding spectral watermark...'):
                try:
                    embed_watermark(t_in_path, t_out_path)
                    st.success('Watermark successfully embedded.')
                    st.audio(t_out_path, format='audio/wav')
                    with open(t_out_path, 'rb') as f:
                        aud_bytes = f.read()
                    st.download_button(label='download watermarked audio', data=aud_bytes, file_name=f'watermarked_{original_filename}', mime='audio/wav', type='primary', use_container_width=True)
                except Exception as e:
                    st.error(f'Watermark failed to embed: {e}')
        else:
            st.markdown('<div style="background: #fff; font-weight: 600; border: 2px dashed var(--border); padding: 40px; text-align: center;">no file processed yet.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def render_history():
    st.markdown('<div class="section-header"><span>history</span> <span>↗</span></div>', unsafe_allow_html=True)
    history_records = fetch_all_history()
    if not history_records:
        st.info('No historical data available. Run an analysis to generate history.')
        return
    df_data = []
    for rec in history_records:
        df_data.append({'ID': rec['id'], 'Time': rec['timestamp'], 'Filename': rec['filename'], 'Verdict': rec['final_verdict'], 'Risk Score': rec['risk_score'], 'AI Label': rec['deepfake_label'], 'WM Confidence': round(rec['watermark_confidence'], 3)})
    st.dataframe(df_data, use_container_width=True, hide_index=True)
    st.markdown('<div class="section-header" style="margin-top: 32px;"><span>recent risk score trends</span> <span>↗</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    recent = history_records[:20]
    recent.reverse()
    if len(recent) > 1:
        plt.style.use('default')
        fig, ax = plt.subplots(figsize=(10, 4))
        times = [r['timestamp'].split(' ')[1] for r in recent]
        scores = [r['risk_score'] for r in recent]
        ax.plot(times, scores, color='#000', marker='s', linewidth=2, markersize=8, markeredgecolor='black', markerfacecolor='#ff9a9e')
        fig.patch.set_facecolor('#ebebeb')
        ax.set_facecolor('#fff')
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(2)
        ax.tick_params(colors='#000', width=2)
        ax.set_ylabel('Risk Score', color='#000', fontname='Space Grotesk', fontweight='bold')
        plt.xticks(rotation=45, ha='right', fontsize=8, fontname='Space Grotesk')
        ax.grid(True, linestyle='-', alpha=1, color='#000', linewidth=0.5)
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.markdown('<div style="text-align: center; font-weight: 600; padding: 20px;">Need at least 2 historical records to plot trends.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header" style="margin-top: 32px; color: var(--high); border-bottom-color: var(--high);"><span>clear history</span> <span>↗</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="card" style="background: var(--high);">', unsafe_allow_html=True)
    st.markdown('<div style="font-family: var(--syne); font-size: 1.5rem; font-weight: 800; margin-bottom: 8px;">delete data</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-weight: 600; margin-bottom: 16px;">This action will permanently delete all analysis history from the database.</div>', unsafe_allow_html=True)
    confirm = st.checkbox('I understand, proceed to clear')
    if confirm:
        if st.button('clear history', type='secondary'):
            clear_history()
            st.success('History successfully cleared.')
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def render_analytics():
    st.markdown('<div class="section-header"><span>analytics</span> <span>↗</span></div>', unsafe_allow_html=True)
    history = fetch_all_history()
    if not history:
        st.info('No logs available to visualize data.')
        return
    low_count = sum((1 for r in history if r['risk_level'] == 'Low'))
    med_count = sum((1 for r in history if r['risk_level'] == 'Medium'))
    high_count = sum((1 for r in history if r['risk_level'] == 'High'))
    total = len(history)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><div style="font-family: var(--syne); font-size: 1.5rem; font-weight: 800; text-transform: lowercase; border-bottom: 2px solid #000; padding-bottom: 8px; margin-bottom: 16px;">risk distribution</div>', unsafe_allow_html=True)
        plt.style.use('default')
        fig, ax = plt.subplots(figsize=(6, 4))
        labels = ['Low Risk', 'Medium Risk', 'High Risk']
        sizes = [low_count, med_count, high_count]
        colors = ['#a8e6cf', '#ffd3b6', '#ff8b94']
        valid_sizes, valid_lbls, valid_cols = ([], [], [])
        for i in range(len(sizes)):
            if sizes[i] > 0:
                valid_sizes.append(sizes[i])
                valid_lbls.append(labels[i])
                valid_cols.append(colors[i])
        if valid_sizes:
            ax.pie(valid_sizes, labels=valid_lbls, colors=valid_cols, autopct='%1.1f%%', startangle=90, textprops={'color': '#000', 'fontweight': 'bold', 'family': 'Space Grotesk'}, wedgeprops={'edgecolor': 'black', 'linewidth': 2})
            centre_circle = plt.Circle((0, 0), 0.7, fc='#ebebeb', ec='black', lw=2)
            fig.gca().add_artist(centre_circle)
        fig.patch.set_facecolor('#ebebeb')
        ax.set_facecolor('#ebebeb')
        plt.tight_layout()
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div style="font-family: var(--syne); font-size: 1.5rem; font-weight: 800; text-transform: lowercase; border-bottom: 2px solid #000; padding-bottom: 8px; margin-bottom: 16px;">average scores</div>', unsafe_allow_html=True)
        avg_wm = sum((r['watermark_confidence'] for r in history)) / total
        avg_ai = sum((r['deepfake_confidence'] for r in history)) / total
        st.markdown(f'\n        <div style="margin-bottom: 24px;">\n            <div style="font-weight: 700; font-size: 0.875rem; text-transform: lowercase; border-bottom: 2px solid #000; display: inline-block;">average watermark confidence</div>\n            <div style="font-family: var(--syne); font-size: 2.5rem; font-weight: 800;">{avg_wm * 100:.1f}%</div>\n        </div>\n        <div style="margin-bottom: 24px;">\n            <div style="font-weight: 700; font-size: 0.875rem; text-transform: lowercase; border-bottom: 2px solid #000; display: inline-block;">average ai detection confidence</div>\n            <div style="font-family: var(--syne); font-size: 2.5rem; font-weight: 800;">{avg_ai * 100:.1f}%</div>\n        </div>\n        <div style="margin-bottom: 12px;">\n            <div style="font-weight: 700; font-size: 0.875rem; text-transform: lowercase; border-bottom: 2px solid #000; display: inline-block;">total analyses run</div>\n            <div style="font-family: var(--syne); font-size: 2.5rem; font-weight: 800;">{total} operations</div>\n        </div>\n        ', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def render_architecture():
    st.markdown('<div class="section-header"><span>system architecture</span> <span>↗</span></div>', unsafe_allow_html=True)
    st.markdown('\n    <div class="card">\n        <h3 style="margin-top: 0; margin-bottom: 16px; font-family: var(--syne); font-size: 2rem;">processing pipeline</h3>\n        <p style="font-weight: 500; line-height: 1.8; margin-bottom: 0;">\n            <b>1. Audio Upload</b><br>\n            Receives WAV/MP3 files and saves them to temporary storage.\n            <br><br>\n            <b>2. Resampling & Preprocessing</b><br>\n            Normalizes the audio sample rates using `librosa` to prepare the audio for AI analysis.\n            <br><br>\n            <b>3. AI Detection (Wav2Vec2)</b><br>\n            Processes the audio through a transformer network trained for deepfake detection. Outputs an authenticity probability.\n            <br><br>\n            <b>4. Watermark Verification (FFT)</b><br>\n            Analyzes the audio frequency spectrum using Fast Fourier Transform to detect hidden spectral watermarks.\n            <br><br>\n            <b>5. Risk Engine</b><br>\n            Combines AI and watermark results into a final 0-100% Risk Score to determine if the audio is a deepfake or authentic.\n            <br><br>\n            <b>6. Database Logging</b><br>\n            Saves the results into a local SQLite database for historical analytics.\n        </p>\n    </div>\n    ', unsafe_allow_html=True)
inject_css()
with st.sidebar:
    st.markdown(f'''
    <div style="text-align: center; margin-bottom: 20px;">
        <div style="background: white; border: 3px solid black; border-radius: 12px; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px auto;">
            <span style="font-size: 30px;">🎤</span>
        </div>
        <h2 style="margin:0;">Voxie AI</h2>
        <p style="margin:0; opacity:0.6; font-size:0.8rem;">Voice Authenticator</p>
    </div>
    ''', unsafe_allow_html=True)
    
    nav_choice = st.radio('Navigation', options=['Dashboard', 'Verify Audio', 'Embed Watermark', 'History', 'Analytics', 'Architecture'], label_visibility='collapsed')
    
    st.markdown('<div class="upgrade-btn">Upgrade to Pro</div>', unsafe_allow_html=True)

if nav_choice == 'Dashboard':
    render_dashboard()
elif nav_choice == 'Verify Audio':
    render_verify()
elif nav_choice == 'Embed Watermark':
    render_embed()
elif nav_choice == 'History':
    render_history()
elif nav_choice == 'Analytics':
    render_analytics()
elif nav_choice == 'Architecture':
    render_architecture()
