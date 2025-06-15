import streamlit as st
import time
import json

# Configure page
st.set_page_config(
    page_title="ADAMS - RAG Evaluation",
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
    
    /* Data table styling */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Comment section */
    .comment-section {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 245, 255, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
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
if 'dataset_processed' not in st.session_state:
    st.session_state.dataset_processed = None
if 'selected_llm' not in st.session_state:
    st.session_state.selected_llm = 'Qwen'
if 'reviewer_comments' not in st.session_state:
    st.session_state.reviewer_comments = {}

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

# Sample dataset for demonstration
sample_dataset = [
    {
        "Question": "What are the key benefits of using RAG systems in healthcare?",
        "Reference Answer": "RAG systems provide up-to-date medical information, reduce hallucinations, ensure compliance, and enable personalized care.",
        "Model Answer": "RAG systems in healthcare offer several key benefits: 1) Access to up-to-date medical research and guidelines, 2) Reduced hallucination through grounded responses, 3) Compliance with regulatory requirements through traceable sources, and 4) Personalized patient care through dynamic information retrieval.",
        "ADAMS_Score": 8.4
    },
    {
        "Question": "How do transformer architectures handle long sequences?",
        "Reference Answer": "Transformers use attention mechanisms but face quadratic complexity with sequence length, leading to various optimization techniques.",
        "Model Answer": "Transformer architectures handle long sequences through self-attention mechanisms, though they face computational challenges due to quadratic complexity. Modern approaches include attention optimization, sparse attention patterns, and hierarchical processing.",
        "ADAMS_Score": 8.9
    },
    {
        "Question": "What is the difference between supervised and unsupervised learning?",
        "Reference Answer": "Supervised learning uses labeled data for training, while unsupervised learning finds patterns in unlabeled data.",
        "Model Answer": "Supervised learning algorithms learn from labeled training data to make predictions on new data, while unsupervised learning discovers hidden patterns and structures in data without labels, such as clustering and dimensionality reduction.",
        "ADAMS_Score": 9.1
    }
]

if st.session_state.metrics_data is None:
    st.session_state.metrics_data = default_metrics.copy()

# Header
st.markdown('<h1 class="main-title">ADAMS</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #b8bcc8; margin-bottom: 2rem;">Adaptive Domain-Aware Metric Selection</p>', unsafe_allow_html=True)

# Navigation
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📊 Dataset Upload", use_container_width=True, type="primary"):
        st.session_state.page = 'upload'
with col2:
    if st.button("📋 Dataset Review", use_container_width=True, type="primary"):
        st.session_state.page = 'dataset'
with col3:
    if st.button("🎛️ Configuration", use_container_width=True, type="primary"):
        st.session_state.page = 'config'

# Page 1: Upload
if st.session_state.page == 'upload':
    st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
    st.markdown("## 🧠 Dataset Processing")
    st.markdown("Upload your RAG outputs for multi-agent evaluation analysis")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Drop your data into the evaluation system",
        type=['csv', 'json', 'xlsx'],
        help="Supports CSV, JSON, XLSX formats • Max 200MB"
    )
    
    # LLM Judge Selection
    st.markdown("### 🤖 Select LLM Judge")
    llm_options = ['Qwen', 'Deepseek', 'Distilled Qwen', 'Mistral', 'LLaMA 3.1']
    st.session_state.selected_llm = st.selectbox(
        "Choose the LLM judge for evaluation:",
        llm_options,
        index=llm_options.index(st.session_state.selected_llm)
    )
    
    if uploaded_file is not None:
        st.success(f"✅ File uploaded successfully! Selected LLM Judge: **{st.session_state.selected_llm}**")
        
        # Simulate processing
        if st.button("🚀 Launch ADAMS Analysis", use_container_width=True, type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            stages = [
                f"Initializing {st.session_state.selected_llm} evaluation matrix...",
                "Deploying multi-agent analysis swarm...",
                "Processing domain-specific parameters...",
                "Calibrating metric weighting algorithms...",
                "Synthesizing evaluation confidence scores...",
                "ADAMS processing complete ⚡"
            ]
            
            for i, stage in enumerate(stages):
                progress = (i + 1) / len(stages)
                progress_bar.progress(progress)
                status_text.markdown(f'<p class="neon-text">{stage}</p>', unsafe_allow_html=True)
                time.sleep(0.8)
            
            st.session_state.processing_complete = True
            st.session_state.dataset_processed = sample_dataset
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
        
        if st.button("📋 View Processed Dataset", use_container_width=True, type="primary"):
            st.session_state.page = 'dataset'
            st.rerun()
    
    if not st.session_state.processing_complete:
        st.markdown("</div>", unsafe_allow_html=True)

# Page 2: Dataset Review
elif st.session_state.page == 'dataset':
    st.markdown("## 📋 Dataset Review & ADAMS Reconfiguration")
    st.markdown("Review the processed dataset with ADAMS scores and download results")
    
    if st.session_state.dataset_processed:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.markdown(f"### 📊 Processed Dataset (LLM Judge: **{st.session_state.selected_llm}**)")
        
        # Display dataset as table
        import pandas as pd
        df = pd.DataFrame(st.session_state.dataset_processed)
        st.dataframe(df, use_container_width=True)
        
        # Download options
        st.markdown("### 💾 Download Options")
        col1, col2 = st.columns(2)
        
        with col1:
            # Download as CSV
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=f"adams_dataset_{st.session_state.selected_llm.lower().replace(' ', '_')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # Download as JSON
            json_data = df.to_json(orient='records', indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"adams_dataset_{st.session_state.selected_llm.lower().replace(' ', '_')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Statistics
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.markdown("### 📈 Dataset Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Samples", len(df))
        with col2:
            st.metric("Average ADAMS Score", f"{df['ADAMS_Score'].mean():.2f}")
        with col3:
            st.metric("Highest Score", f"{df['ADAMS_Score'].max():.2f}")
        with col4:
            st.metric("Lowest Score", f"{df['ADAMS_Score'].min():.2f}")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("🎛️ Proceed to Configuration", use_container_width=True, type="primary"):
            st.session_state.page = 'config'
            st.rerun()
    
    else:
        st.warning("⚠️ No processed dataset available. Please upload and process a dataset first.")
        if st.button("← Back to Upload", use_container_width=True):
            st.session_state.page = 'upload'
            st.rerun()

# Page 3: Configuration
elif st.session_state.page == 'config':
    st.markdown("## 🎛️ Metric Configuration")
    st.markdown("Real-time metric calibration with reviewer feedback system")
    
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
                key=f"slider_{metric_name}",
                help=f"Current score: {data['score']}"
            )
        
        # Update the session state and recalculate final score in real-time
        for metric_name in st.session_state.metrics_data:
            st.session_state.metrics_data[metric_name]['weight'] = updated_weights[metric_name]
        
        if st.button("↺ Reset to Defaults", use_container_width=True):
            st.session_state.metrics_data = default_metrics.copy()
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Reviewer Comments Section
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.markdown("### 💬 Reviewer Comments & Notes")
        
        # Text area for comments
        reviewer_comment = st.text_area(
            "Add your evaluation comments:",
            value=st.session_state.reviewer_comments.get('main_comment', ''),
            height=150,
            placeholder="Enter your thoughts on the evaluation criteria, weight adjustments, or overall assessment..."
        )
        
        # Save comment mode selection
        comment_mode = st.selectbox(
            "Save as mode:",
            ["Draft", "Review", "Final", "Custom"],
            help="Select the mode for saving your comments"
        )
        
        if comment_mode == "Custom":
            custom_mode = st.text_input("Enter custom mode name:")
            comment_mode = custom_mode if custom_mode else "Custom"
        
        col_save, col_load = st.columns(2)
        with col_save:
            if st.button("💾 Save Comments", use_container_width=True):
                st.session_state.reviewer_comments['main_comment'] = reviewer_comment
                st.session_state.reviewer_comments['mode'] = comment_mode
                st.session_state.reviewer_comments['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
                st.success(f"Comments saved as '{comment_mode}' mode!")
        
        with col_load:
            if st.button("📋 Export Comments", use_container_width=True):
                if st.session_state.reviewer_comments:
                    comment_data = {
                        "comment": st.session_state.reviewer_comments.get('main_comment', ''),
                        "mode": st.session_state.reviewer_comments.get('mode', ''),
                        "timestamp": st.session_state.reviewer_comments.get('timestamp', ''),
                        "llm_judge": st.session_state.selected_llm,
                        "metric_weights": st.session_state.metrics_data
                    }
                    
                    st.download_button(
                        label="Download Comments",
                        data=json.dumps(comment_data, indent=2),
                        file_name=f"reviewer_comments_{comment_mode.lower()}_{time.strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        
        # Calculate final score in real-time
        weighted_sum = sum(data['score'] * data['weight'] for data in st.session_state.metrics_data.values())
        total_weight = sum(data['weight'] for data in st.session_state.metrics_data.values())
        final_score = weighted_sum / total_weight if total_weight > 0 else 0
        
        # Display final score (updates automatically as sliders move)
        st.markdown(f"""
        <div class="score-display">
            <h3 style="color: #b8bcc8; margin-bottom: 1rem;">Final ADAMS Score</h3>
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
        
        # Impact analysis (updates based on current weights)
        top_metrics = sorted(st.session_state.metrics_data.items(), key=lambda x: x[1]['weight'], reverse=True)[:3]
        top_names = [metric[0] for metric in top_metrics]
        avg_weight = sum(metric[1]['weight'] for metric in top_metrics) / 3
        
        impact_text = f"**🔥 Impact Analysis:**\n\nCurrent emphasis: {', '.join(top_names)}. "
        if avg_weight > 0.8:
            impact_text += "High-confidence configuration detected. System optimized for precision evaluation."
        elif avg_weight > 0.6:
            impact_text += "Balanced configuration active. Moderate weighting across evaluation dimensions."
        else:
            impact_text += "Low-weight configuration. Consider increasing key metric priorities for better accuracy."
        
        st.info(impact_text)
        
        # Current session info
        if st.session_state.reviewer_comments:
            st.markdown("#### 📝 Current Session")
            st.markdown(f"**Mode:** {st.session_state.reviewer_comments.get('mode', 'Not set')}")
            if st.session_state.reviewer_comments.get('timestamp'):
                st.markdown(f"**Last saved:** {st.session_state.reviewer_comments['timestamp']}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← Back to Dataset", use_container_width=True):
            st.session_state.page = 'dataset'
            st.rerun()
    with col2:
        if st.button("💾 Save Configuration", use_container_width=True, type="primary"):
            config_data = {
                "metrics": st.session_state.metrics_data,
                "final_score": final_score,
                "llm_judge": st.session_state.selected_llm,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            st.download_button(
                label="Download Configuration",
                data=json.dumps(config_data, indent=2),
                file_name=f"adams_config_{time.strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    with col3:
        if st.button("📤 Export Full Report", use_container_width=True, type="primary"):
            full_report = {
                "dataset": st.session_state.dataset_processed,
                "metrics": st.session_state.metrics_data,
                "final_score": final_score,
                "llm_judge": st.session_state.selected_llm,
                "reviewer_comments": st.session_state.reviewer_comments,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            st.download_button(
                label="Download Full Report",
                data=json.dumps(full_report, indent=2),
                file_name=f"adams_full_report_{time.strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

# Sidebar with additional info
with st.sidebar:
    st.markdown("### 🧠 ADAMS Interface")
    st.markdown("**Version:** 2.0.0")
    st.markdown("**Status:** ✅ Online")
    st.markdown("**Mode:** Interactive Demo")
    
    st.markdown("---")
    st.markdown("### 📊 Current Session")
    st.markdown(f"**Metrics Loaded:** {len(st.session_state.metrics_data)}")
    st.markdown(f"**Page:** {st.session_state.page.title()}")
    st.markdown(f"**LLM Judge:** {st.session_state.selected_llm}")
    
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
        st.session_state.dataset_processed = None
        st.session_state.reviewer_comments = {}
        st.session_state.page = 'upload'
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🎯 Demo Instructions")
    st.markdown("""
    1. **Upload:** Select file and LLM judge
    2. **Dataset:** Review processed results
    3. **Configuration:** Adjust weights & add comments
    4. **Export:** Download configurations and reports
    """)