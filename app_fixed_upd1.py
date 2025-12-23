"""
Meeting Summarizer - Web UI
Modern dark theme design inspired by crypto trading platforms

Run with: streamlit run app.py
"""

import streamlit as st
import os
from datetime import datetime
from agent import MeetingSummarizer
from config import Config
import glob

# Page config
st.set_page_config(
    page_title="Meeting Summarizer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Dark theme with modern design
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --bg-primary: #1a1d29;
        --bg-secondary: #252836;
        --bg-tertiary: #2d3142;
        --accent-purple: #9b87f5;
        --accent-green: #4ade80;
        --accent-red: #f87171;
        --text-primary: #ffffff;
        --text-secondary: #9ca3af;
        --border-color: #374151;
    }
    
    /* Global background */
    .stApp {
        background-color: var(--bg-primary);
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Headers */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, var(--accent-purple) 0%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .sub-header {
        text-align: center;
        color: var(--text-secondary);
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--bg-secondary);
        border-right: 1px solid var(--border-color);
    }
    
    [data-testid="stSidebar"] .element-container {
        color: var(--text-primary);
    }
    
    /* Cards/Containers */
    .card {
        background-color: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .metric-card {
        background-color: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
    
    .metric-card .metric-label {
        color: var(--text-secondary);
        font-size: 0.875rem;
        margin-bottom: 0.5rem;
    }
    
    .metric-card .metric-value {
        color: var(--text-primary);
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    /* Text areas */
    .stTextArea textarea {
        background-color: var(--bg-tertiary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-family: 'SF Mono', 'Monaco', 'Menlo', monospace;
        font-size: 14px;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--accent-purple) !important;
        box-shadow: 0 0 0 2px rgba(155, 135, 245, 0.2) !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, var(--accent-purple) 0%, #7c3aed 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(155, 135, 245, 0.3);
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background-color: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        color: var(--text-primary);
    }
    
    /* Checkboxes */
    .stCheckbox {
        color: var(--text-primary);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        color: var(--text-secondary);
        padding: 0.75rem 1.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--accent-purple);
        color: white;
        border-color: var(--accent-purple);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: var(--text-primary);
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary);
    }
    
    [data-testid="stMetricDelta"] {
        color: var(--accent-green);
    }
    
    /* Success/Info/Warning boxes */
    .success-box {
        background-color: rgba(74, 222, 128, 0.1);
        border: 1px solid var(--accent-green);
        border-radius: 12px;
        padding: 1rem;
        color: var(--accent-green);
        margin: 1rem 0;
    }
    
    .info-box {
        background-color: rgba(155, 135, 245, 0.1);
        border: 1px solid var(--accent-purple);
        border-radius: 12px;
        padding: 1rem;
        color: var(--accent-purple);
        margin: 1rem 0;
    }
    
    .warning-box {
        background-color: rgba(248, 113, 113, 0.1);
        border: 1px solid var(--accent-red);
        border-radius: 12px;
        padding: 1rem;
        color: var(--accent-red);
        margin: 1rem 0;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background-color: var(--bg-tertiary);
        border: 2px dashed var(--border-color);
        border-radius: 12px;
        padding: 2rem;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--accent-purple);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        color: var(--text-primary);
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background-color: var(--accent-purple);
    }
    
    /* Download button */
    .stDownloadButton button {
        background-color: var(--bg-tertiary);
        border: 1px solid var(--accent-purple);
        color: var(--accent-purple);
        border-radius: 12px;
        padding: 0.5rem 1rem;
    }
    
    .stDownloadButton button:hover {
        background-color: var(--accent-purple);
        color: white;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background-color: var(--bg-tertiary);
        border-radius: 12px;
        padding: 0.5rem;
    }
    
    /* File type badge */
    .file-type-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    
    .badge-summary {
        background-color: rgba(155, 135, 245, 0.2);
        color: var(--accent-purple);
        border: 1px solid var(--accent-purple);
    }
    
    .badge-email {
        background-color: rgba(74, 222, 128, 0.2);
        color: var(--accent-green);
        border: 1px solid var(--accent-green);
    }
    
    .badge-brief {
        background-color: rgba(251, 191, 36, 0.2);
        color: #fbbf24;
        border: 1px solid #fbbf24;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Markdown output */
    .markdown-text-container {
        background-color: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        color: var(--text-primary);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = None
if 'cost_summary' not in st.session_state:
    st.session_state.cost_summary = None

# Header
st.markdown('<div class="main-header">🤖 Meeting Summarizer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Transform messy meeting notes into structured summaries in seconds</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")
    
    # Model selection
    model = st.selectbox(
        "AI Model",
        options=["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
        index=0,
        help="GPT-3.5: Fast & cheap\nGPT-4: Best quality"
    )
    
    st.markdown("---")
    
    # Output options - CLEAR SELECTION
    st.markdown("### 📄 What to Generate")
    
    output_choice = st.radio(
        "Choose outputs:",
        [
            "📋 Summary Only",
            "📧 Email Only", 
            "📊 Brief Only",
            "📋📧 Summary + Email",
            "📋📊 Summary + Brief",
            "📧📊 Email + Brief",
            "📋📧📊 All Three"
        ],
        index=None,  # No default selection
        help="Select what you want to generate"
    )
    
    # Parse selection
    if output_choice:
        generate_summary = "📋" in output_choice
        generate_email = "📧" in output_choice
        generate_brief = "📊" in output_choice
    else:
        generate_summary = False
        generate_email = False
        generate_brief = False
        st.warning("⚠️ Please select what to generate")
    
    st.markdown("---")
    
    # Meeting date
    st.markdown("### 📅 Meeting Date")
    use_custom_date = st.checkbox("Custom date", value=False)
    
    if use_custom_date:
        meeting_date = st.date_input("Date", value=datetime.now())
        date_str = meeting_date.strftime("%B %d, %Y")
    else:
        date_str = datetime.now().strftime("%B %d, %Y")
        st.info(f"📅 {date_str}")
    
    st.markdown("---")
    
    # API key status
    st.markdown("### 🔐 API Status")
    if Config.OPENAI_API_KEY and Config.OPENAI_API_KEY != "your-key-here":
        st.success("✅ Connected")
    else:
        st.error("❌ No API key")
        st.caption("Add to .env file")
    
    st.markdown("---")
    
    # Info
    st.markdown("### ℹ️ About")
    st.caption("Version 1.0.0")
    st.caption("Built with ❤️")

# Main content with tabs
tab1, tab2, tab3 = st.tabs(["📝 Summarize", "📂 Batch Process", "📊 History"])

# TAB 1: Single Meeting
with tab1:
    # Input method selection
    col1, col2 = st.columns([1, 1])
    with col1:
        input_method = st.radio(
            "Input Method",
            ["✍️ Type/Paste", "📁 Upload File"],
            horizontal=True,
            label_visibility="collapsed"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    notes = ""
    
    if input_method == "✍️ Type/Paste":
        notes = st.text_area(
            "Meeting Notes",
            height=350,
            placeholder="""📝 Paste your meeting notes here...

Example format:

Project Alpha - Jan 15, 2024
Team: John (Eng), Sarah (Design), Mike (Client)

💰 Budget: $75k approved
📅 Launch: March 15

Decisions:
✓ Approach B for backend
✓ John leads eng, Sarah design
✓ Weekly check-ins Tuesday 2pm

Action Items:
→ John: API docs by Friday
→ Sarah: Performance testing
→ Oleg: Update template to Mike

🚨 Risks:
• Tight timeline
• External API not confirmed
""",
            label_visibility="collapsed"
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload meeting notes",
            type=['txt', 'md'],
            label_visibility="collapsed"
        )
        if uploaded_file is not None:
            notes = uploaded_file.read().decode('utf-8')
            st.success(f"✅ Loaded {len(notes.split())} words from **{uploaded_file.name}**")
    
    # Tips expander
    with st.expander("💡 Tips for Better Results"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **✅ Include:**
            - Participant names
            - Explicit decisions
            - Dates & deadlines
            - Action items with owners
            - Risks or blockers
            """)
        with col2:
            st.markdown("""
            **❌ Avoid:**
            - Vague notes
            - Missing context
            - No names/dates
            - Unclear ownership
            """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Process button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        process_button = st.button(
            "🚀 Generate Summary",
            type="primary",
            use_container_width=True,
            disabled=not notes.strip() or not output_choice  # Disabled if no notes OR no selection
        )
    
    # Process meeting
    if process_button and notes.strip() and output_choice:
        with st.spinner("🤖 AI is analyzing your meeting..."):
            try:
                # Create summarizer
                summarizer = MeetingSummarizer(model=model, verbose=False)
                
                # Always generate summary first (needed for email/brief generation)
                summary = summarizer.summarize_meeting(notes, date_str)
                
                results = {'summary': summary}
                
                # Generate email if requested
                if generate_email:
                    email = summarizer.generate_email(summary)
                    results['email'] = email
                
                # Generate brief if requested
                if generate_brief:
                    brief = summarizer.generate_exec_brief(summary)
                    results['brief'] = brief
                
                # Store in session state
                st.session_state.results = results
                st.session_state.cost_summary = summarizer.get_cost_summary()
                st.session_state.show_summary = generate_summary
                
                st.success("✅ Generated successfully!")
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Check your .env configuration")
    
    # Display results
    if st.session_state.results:
        st.markdown("---")
        
        results = st.session_state.results
        show_summary = st.session_state.get('show_summary', True)
        
        # Cost metrics in cards
        if st.session_state.cost_summary:
            cost = st.session_state.cost_summary
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Model</div>
                    <div class="metric-value">{cost['model'].split('-')[0].upper()}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Tokens</div>
                    <div class="metric-value">{cost['total_tokens']:,}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">API Calls</div>
                    <div class="metric-value">{cost['api_calls']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Cost</div>
                    <div class="metric-value" style="color: var(--accent-green);">${cost['total_cost']:.4f}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Summary (only if user selected it)
        if show_summary and 'summary' in results:
            st.markdown("### 📋 Meeting Summary")
            st.markdown(f'<div class="markdown-text-container">{results["summary"]}</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            with col2:
                st.download_button(
                    label="⬇️ Download",
                    data=results['summary'],
                    file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
        
        # Email (only if user selected it)
        if 'email' in results:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📧 Follow-up Email")
            st.text_area("", results['email'], height=300, key="email_output", label_visibility="collapsed")
            
            col1, col2 = st.columns([3, 1])
            with col2:
                st.download_button(
                    label="⬇️ Download",
                    data=results['email'],
                    file_name=f"email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        # Executive Brief (only if user selected it)
        if 'brief' in results:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📊 Executive Brief")
            st.text_area("", results['brief'], height=300, key="brief_output", label_visibility="collapsed")
            
            col1, col2 = st.columns([3, 1])
            with col2:
                st.download_button(
                    label="⬇️ Download",
                    data=results['brief'],
                    file_name=f"brief_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

# TAB 2: Batch Processing
with tab2:
    st.markdown("### 📂 Batch Process Multiple Meetings")
    
    st.info("Upload multiple files to process them all at once")
    
    uploaded_files = st.file_uploader(
        "Drop files here",
        type=['txt', 'md'],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        st.success(f"✅ **{len(uploaded_files)} files** ready to process")
        
        # Show file list
        with st.expander("📋 Files"):
            for file in uploaded_files:
                st.text(f"• {file.name}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Batch process button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Process All Files", type="primary", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                results_list = []
                total_cost = 0
                
                for i, file in enumerate(uploaded_files):
                    status_text.text(f"Processing {file.name}...")
                    
                    try:
                        notes = file.read().decode('utf-8')
                        
                        summarizer = MeetingSummarizer(model=model, verbose=False)
                        
                        # Generate summary first (always needed)
                        summary = summarizer.summarize_meeting(notes)
                        result = {'summary': summary}
                        
                        # Generate email if requested
                        if generate_email:
                            email = summarizer.generate_email(summary)
                            result['email'] = email
                        
                        # Generate brief if requested
                        if generate_brief:
                            brief = summarizer.generate_exec_brief(summary)
                            result['brief'] = brief
                        
                        cost = summarizer.get_cost_summary()
                        total_cost += cost['total_cost']
                        
                        results_list.append({
                            'filename': file.name,
                            'result': result,
                            'cost': cost,
                            'show_summary': generate_summary
                        })
                        
                    except Exception as e:
                        st.warning(f"⚠️ Failed: {file.name}")
                    
                    progress_bar.progress((i + 1) / len(uploaded_files))
                
                status_text.text("✅ Complete!")
                
                # Summary
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Processed", f"{len(results_list)}/{len(uploaded_files)}")
                with col2:
                    st.metric("Total Cost", f"${total_cost:.4f}")
                
                # Show results
                for item in results_list:
                    with st.expander(f"📄 {item['filename']}"):
                        # Show summary if selected
                        if item.get('show_summary', True) and 'summary' in item['result']:
                            st.markdown(item['result']['summary'])
                        
                        # Show email if generated
                        if 'email' in item['result']:
                            st.markdown("### 📧 Email")
                            st.text(item['result']['email'][:500] + "..." if len(item['result']['email']) > 500 else item['result']['email'])
                        
                        # Show brief if generated
                        if 'brief' in item['result']:
                            st.markdown("### 📊 Brief")
                            st.text(item['result']['brief'][:500] + "..." if len(item['result']['brief']) > 500 else item['result']['brief'])
                        
                        # Download buttons
                        cols = st.columns(3)
                        col_idx = 0
                        
                        if item.get('show_summary', True) and 'summary' in item['result']:
                            with cols[col_idx]:
                                st.download_button(
                                    "⬇️ Summary",
                                    data=item['result']['summary'],
                                    file_name=f"{item['filename']}_summary.md",
                                    key=f"dl_s_{item['filename']}"
                                )
                            col_idx += 1
                        
                        if 'email' in item['result']:
                            with cols[col_idx]:
                                st.download_button(
                                    "⬇️ Email",
                                    data=item['result']['email'],
                                    file_name=f"{item['filename']}_email.txt",
                                    key=f"dl_e_{item['filename']}"
                                )
                            col_idx += 1
                        
                        if 'brief' in item['result']:
                            with cols[col_idx]:
                                st.download_button(
                                    "⬇️ Brief",
                                    data=item['result']['brief'],
                                    file_name=f"{item['filename']}_brief.txt",
                                    key=f"dl_b_{item['filename']}"
                                )

# TAB 3: Recent Summaries - IMPROVED WITH FILE TYPE BADGES
with tab3:
    st.markdown("### 📊 Recent Summaries")
    
    output_dir = Config.OUTPUT_DIR
    
    if os.path.exists(output_dir):
        # Get all files (summaries, emails, briefs)
        all_files = {
            'summaries': sorted(glob.glob(os.path.join(output_dir, "meeting_summary_*.md")), key=os.path.getmtime, reverse=True),
            'emails': sorted(glob.glob(os.path.join(output_dir, "meeting_followup_email_*.txt")), key=os.path.getmtime, reverse=True),
            'briefs': sorted(glob.glob(os.path.join(output_dir, "executive_brief_*.txt")), key=os.path.getmtime, reverse=True)
        }
        
        total_files = len(all_files['summaries']) + len(all_files['emails']) + len(all_files['briefs'])
        
        if total_files > 0:
            # Show counts
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📋 Summaries", len(all_files['summaries']))
            with col2:
                st.metric("📧 Emails", len(all_files['emails']))
            with col3:
                st.metric("📊 Briefs", len(all_files['briefs']))
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Combine and sort all files by time
            all_files_list = []
            
            for file_path in all_files['summaries']:
                all_files_list.append({
                    'path': file_path,
                    'type': 'summary',
                    'icon': '📋',
                    'badge_class': 'badge-summary',
                    'label': 'Summary',
                    'time': os.path.getmtime(file_path)
                })
            
            for file_path in all_files['emails']:
                all_files_list.append({
                    'path': file_path,
                    'type': 'email',
                    'icon': '📧',
                    'badge_class': 'badge-email',
                    'label': 'Email',
                    'time': os.path.getmtime(file_path)
                })
            
            for file_path in all_files['briefs']:
                all_files_list.append({
                    'path': file_path,
                    'type': 'brief',
                    'icon': '📊',
                    'badge_class': 'badge-brief',
                    'label': 'Brief',
                    'time': os.path.getmtime(file_path)
                })
            
            # Sort by time (newest first)
            all_files_list.sort(key=lambda x: x['time'], reverse=True)
            
            # Show recent files (last 20)
            for file_info in all_files_list[:20]:
                filename = os.path.basename(file_info['path'])
                timestamp = datetime.fromtimestamp(file_info['time'])
                
                # Create expander label with colored badge
                # Use different emoji/style for each type
                if file_info['type'] == 'summary':
                    badge = "🟣 Summary"
                elif file_info['type'] == 'email':
                    badge = "🟢 Email"
                else:  # brief
                    badge = "🟡 Brief"
                
                expander_label = f"{file_info['icon']} {timestamp.strftime('%b %d, %Y • %H:%M')}  •  {badge}"
                
                with st.expander(expander_label, expanded=False):
                    try:
                        with open(file_info['path'], 'r') as f:
                            content = f.read()
                        
                        if file_info['type'] == 'summary':
                            st.markdown(content)
                        else:
                            st.text_area("", content, height=300, key=f"view_{filename}", label_visibility="collapsed")
                        
                        st.download_button(
                            "⬇️ Download",
                            data=content,
                            file_name=filename,
                            key=f"dl_{filename}",
                            use_container_width=False
                        )
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.info("📭 No files yet. Process your first meeting!")
    else:
        st.info("📭 No output directory yet. Process a meeting to create it!")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("💡 GPT-3.5: $0.01/meeting")
with col2:
    st.caption("⚡ Processing: 10-30 sec")
with col3:
    st.caption("🔐 Secure & Private")
