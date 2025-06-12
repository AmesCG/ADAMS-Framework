import streamlit as st
import time
import random

# Configure page
st.set_page_config(
    page_title="ADAMS - Neural RAG Evaluation",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for futuristic styling
st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom title styling */
    .main-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(45deg, #ff006e, #8338ec, #3a86ff, #06ffa5);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 3s ease infinite;
        margin-bottom: 1rem;
    }
    
    @keyframes gradient {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Cyber cards */
    .cyber-card {
        background: rgba(15, 15, 25, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 245, 255, 0.3);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 245, 255, 0.1);
    }
    
    /* Neon text */
    .neon-text {
        color: #00f5ff;
        text-shadow: 0 0 10px #00f5ff;
        font-weight: 600;
    }
    
    /* Metric cards */
    .metric-display {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 245, 255, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin: 0.5rem;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 900;
        font-family: 'JetBrains Mono', monospace;
        color: #00f5ff;
        text-shadow: 0 0 20px rgba(0, 245, 255, 0.5);
    }
    
    .metric-name {
        font-size: 0.9rem;
        color: #b8bcc8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }
    
    /* Score display */
    .score-display {
        text-align: center;
        padding: 2rem;
        background: rgba(0, 245, 255, 0.1);
        border-radius: 15px;
        margin-bottom: 2rem;
        border: 1px solid rgba(0, 245, 255, 0.3);
    }
    
    .score-value {
        font-size: 4rem;
        font-weight: 900;
        font-family: 'JetBrains Mono', monospace;
        color: #00f5ff;
        text-shadow: 0 0 30px rgba(0, 245, 255, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'upload'
if 'metrics_data' not in st.session_state:
    st.session_state.metrics_data = None
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False

# Sample metrics data
default_metrics = {
    'Factual Accuracy': {'score': 8.7, 'weight': 0.9},
    'Coherence': {'score': 9.2, 'weight': 0.8},
    'Relevance': {'score': 8.9, 'weight': 0.85},
    'Completeness': {'score': 7.8, 'weight': 0.7},
    'Citation Quality': {'score': 8.1, 'weight': 0.75},
    'Domain Specificity': {'score': 8.5, 'weight': 0.8},
    'Clarity': {'score': 9.0, 'weight': 0.7},
    'Consistency': {'score': 8.3, 'weight': 0.6},
    'Novelty': {'score': 7.5, 'weight': 0.5},
    'Readability': {'score': 8.8, 'weight': 0.6},
    'Technical Depth': {'score': 8.0, 'weight': 0.7},
    'Evidence Support': {'score': 8.4, 'weight': 0.8},
    'Contextual Fit': {'score': 8.6, 'weight': 0.7},
    'Timeliness': {'score': 7.9, 'weight': 0.6},
    'Bias Detection': {'score': 8.2, 'weight': 0.7}
}

if st.session_state.metrics_data is None:
    st.session_state.metrics_data = default_metrics.copy()

# Header
st.markdown('<h1 class="main-title">ADAMS</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #b8bcc8; margin-bottom: 2rem;">Neural Adaptive Domain-Aware Metric Selection</p>', unsafe_allow_html=True)

# Navigation
col1, col2 = st.columns(2)
with col1:
    if st.button("📊 Dataset Upload", use_container_width=True, type="primary"):
        st.session_state.page = 'upload'
with col2:
    if st.button("🎛️ Neural Configuration", use_container_width=True, type="primary"):
        st.session_state.page = 'config'

# Page 1: Upload
if st.session_state.page == 'upload':
    st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
    st.markdown("## 🧠 Neural Dataset Processing")
    st.markdown("Upload your RAG outputs for multi-agent evaluation analysis")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Drop your data into the neural network",
        type=['csv', 'json', 'xlsx'],
        help="Supports CSV, JSON, XLSX formats • Max 200MB"
    )
    
    if uploaded_file is not None:
        st.success("✅ File uploaded successfully!")
        
        # Simulate processing
        if st.button("🚀 Launch Neural Analysis", use_container_width=True, type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            stages = [
                "Initializing neural evaluation matrix...",
                "Deploying multi-agent analysis swarm...",
                "Processing domain-specific parameters...",
                "Calibrating metric weighting algorithms...",
                "Synthesizing evaluation confidence scores...",
                "Neural processing complete ⚡"
            ]
            
            for i, stage in enumerate(stages):
                progress = (i + 1) / len(stages)
                progress_bar.progress(progress)
                status_text.markdown(f'<p class="neon-text">{stage}</p>', unsafe_allow_html=True)
                time.sleep(0.8)
            
            st.session_state.processing_complete = True
            st.rerun()
    
    # Show results if processing is complete
    if st.session_state.processing_complete:
        st.markdown("### ⚡ Multi-Agent Evaluation Results")
        
        # Create metrics grid using columns
        metrics_list = list(st.session_state.metrics_data.items())
        
        # Display metrics in rows of 3
        for i in range(0, len(metrics_list), 3):
            cols = st.columns(3)
            for j, col in enumerate(cols):
                if i + j < len(metrics_list):
                    metric_name, data = metrics_list[i + j]
                    with col:
                        st.markdown(f"""
                        <div class="metric-display">
                            <div class="metric-value">{data['score']}</div>
                            <div class="metric-name">{metric_name}</div>
                        </div>
                        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("⚡ Launch Neural Configuration", use_container_width=True, type="primary"):
            st.session_state.page = 'config'
            st.rerun()
    
    if not st.session_state.processing_complete:
        st.markdown("</div>", unsafe_allow_html=True)

# Page 2: Configuration
elif st.session_state.page == 'config':
    st.markdown("## 🎛️ Neural Weight Matrix")
    st.markdown("Real-time metric calibration with AI-powered impact analysis")
    
    # Create two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.markdown("### 🧬 Metric Control Matrix")
        
        # Create sliders for each metric
        updated_weights = {}
        for metric_name, data in st.session_state.metrics_data.items():
            updated_weights[metric_name] = st.slider(
                f"**{metric_name}**",
                min_value=0.0,
                max_value=1.0,
                value=data['weight'],
                step=0.05,
                key=f"slider_{metric_name}"
            )
        
        # Update the session state
        for metric_name in st.session_state.metrics_data:
            st.session_state.metrics_data[metric_name]['weight'] = updated_weights[metric_name]
        
        if st.button("↺ Neural Reset", use_container_width=True):
            st.session_state.metrics_data = default_metrics.copy()
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        
        # Calculate final score
        weighted_sum = sum(data['score'] * data['weight'] for data in st.session_state.metrics_data.values())
        total_weight = sum(data['weight'] for data in st.session_state.metrics_data.values())
        final_score = weighted_sum / total_weight if total_weight > 0 else 0
        
        # Display final score
        st.markdown(f"""
        <div class="score-display">
            <h3 style="color: #b8bcc8; margin-bottom: 1rem;">AI Confidence Score</h3>
            <div class="score-value">{final_score:.1f}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Sample analysis
        st.markdown("#### 📋 Sample Analysis")
        
        with st.expander("View Sample Q&A", expanded=True):
            st.markdown("""
            **Query:** What are the key benefits of using RAG systems in healthcare applications?
            
            **AI Response:** RAG systems in healthcare offer several key benefits: 1) Access to up-to-date medical research and guidelines, 2) Reduced hallucination through grounded responses, 3) Compliance with regulatory requirements through traceable sources, and 4) Personalized patient care through dynamic information retrieval.
            """)
        
        # Impact analysis
        top_metrics = sorted(st.session_state.metrics_data.items(), key=lambda x: x[1]['weight'], reverse=True)[:3]
        top_names = [metric[0] for metric in top_metrics]
        avg_weight = sum(metric[1]['weight'] for metric in top_metrics) / 3
        
        impact_text = f"**🔥 Neural Impact Analysis:**\n\nCurrent emphasis: {', '.join(top_names)}. "
        if avg_weight > 0.8:
            impact_text += "High-confidence configuration detected. System optimized for precision evaluation."
        elif avg_weight > 0.6:
            impact_text += "Balanced configuration active. Moderate weighting across evaluation dimensions."
        else:
            impact_text += "Low-weight configuration. Consider increasing key metric priorities for better accuracy."
        
        st.info(impact_text)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← Back to Upload", use_container_width=True):
            st.session_state.page = 'upload'
            st.rerun()
    with col2:
        if st.button("💾 Save Neural Config", use_container_width=True, type="primary"):
            st.success("Configuration saved!")
    with col3:
        if st.button("📤 Export Analysis", use_container_width=True, type="primary"):
            # Create downloadable data as text
            export_data = "ADAMS Neural Evaluation Results\n"
            export_data += "=" * 50 + "\n\n"
            export_data += f"Final Score: {final_score:.1f}\n\n"
            export_data += "Metric Details:\n"
            for name, data in st.session_state.metrics_data.items():
                export_data += f"{name}: Score={data['score']}, Weight={data['weight']:.2f}\n"
            
            st.download_button(
                label="Download Results",
                data=export_data,
                file_name="adams_evaluation_results.txt",
                mime="text/plain"
            )

# Sidebar with additional info
with st.sidebar:
    st.markdown("### 🧠 ADAMS Neural Interface")
    st.markdown("**Version:** 2.0.0-neural")
    st.markdown("**Status:** ✅ Online")
    st.markdown("**Mode:** Interactive Demo")
    
    st.markdown("---")
    st.markdown("### 📊 Current Session")
    st.markdown(f"**Metrics Loaded:** {len(st.session_state.metrics_data)}")
    st.markdown(f"**Page:** {st.session_state.page.title()}")
    
    if st.session_state.processing_complete:
        weighted_sum = sum(data['score'] * data['weight'] for data in st.session_state.metrics_data.values())
        total_weight = sum(data['weight'] for data in st.session_state.metrics_data.values())
        final_score = weighted_sum / total_weight if total_weight > 0 else 0
        st.markdown(f"**Current Score:** {final_score:.1f}")
    
    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")
    if st.button("🔄 Reset Session", use_container_width=True):
        st.session_state.metrics_data = default_metrics.copy()
        st.session_state.processing_complete = False
        st.session_state.page = 'upload'
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🎯 Demo Instructions")
    st.markdown("""
    1. **Upload Tab:** Upload a file and run analysis
    2. **Neural Configuration:** Adjust metric weights
    3. **Watch:** Final score updates in real-time!
    """)