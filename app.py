"""
Meeting Summarizer - Web UI
Beautiful, user-friendly interface for non-technical users

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

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    .stTextArea textarea {
        font-family: 'Monaco', 'Menlo', monospace;
        font-size: 14px;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
    .cost-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        margin: 1rem 0;
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
    st.header("⚙️ Settings")
    
    # Model selection
    model = st.selectbox(
        "AI Model",
        options=["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
        index=0,
        help="GPT-3.5: Fast & cheap ($0.01/meeting)\nGPT-4: Best quality ($0.20/meeting)"
    )
    
    st.markdown("---")
    
    # Output options
    st.subheader("📄 Generate")
    generate_email = st.checkbox("Follow-up Email", value=True)
    generate_brief = st.checkbox("Executive Brief", value=False)
    
    st.markdown("---")
    
    # Meeting date
    st.subheader("📅 Meeting Date")
    use_custom_date = st.checkbox("Use custom date", value=False)
    
    if use_custom_date:
        meeting_date = st.date_input("Date", value=datetime.now())
        date_str = meeting_date.strftime("%B %d, %Y")
    else:
        date_str = datetime.now().strftime("%B %d, %Y")
        st.info(f"Using today: {date_str}")
    
    st.markdown("---")
    
    # Info
    st.subheader("ℹ️ About")
    st.caption("Version 1.0.0")
    st.caption("Built with ❤️ by Oleg")
    
    # API key status
    st.markdown("---")
    if Config.OPENAI_API_KEY and Config.OPENAI_API_KEY != "your-key-here":
        st.success("✅ API key configured")
    else:
        st.error("❌ No API key found")
        st.caption("Add OPENAI_API_KEY to .env file")

# Main content
tab1, tab2, tab3 = st.tabs(["📝 Summarize Meeting", "📂 Batch Process", "📊 Recent Summaries"])

# TAB 1: Single Meeting
with tab1:
    st.header("Enter Your Meeting Notes")
    
    # Input method selection
    input_method = st.radio(
        "Choose input method:",
        ["Type/Paste Notes", "Upload File"],
        horizontal=True
    )
    
    notes = ""
    
    if input_method == "Type/Paste Notes":
        notes = st.text_area(
            "Meeting Notes",
            height=300,
            placeholder="""Example:

Project Alpha Planning - Jan 15, 2024
Attendees: John (Engineering), Sarah (Design), Mike (Client)

Budget: $75k approved
Timeline: Launch by March 15

Decisions:
- Going with approach B for backend
- John leads engineering, Sarah handles design
- Weekly check-ins every Tuesday 2pm

Action Items:
- John: API documentation by Friday
- Sarah: Performance testing this week
- Oleg: Send weekly update template to Mike

Risks:
- Timeline is tight if we hit technical issues
- External API vendor hasn't confirmed timeline

Next meeting: Tuesday Jan 22, 2pm
""",
            help="Paste your meeting notes here. Include names, dates, decisions, and action items for best results."
        )
    else:
        uploaded_file = st.file_uploader(
            "Choose a text file",
            type=['txt', 'md'],
            help="Upload a .txt or .md file with your meeting notes"
        )
        if uploaded_file is not None:
            notes = uploaded_file.read().decode('utf-8')
            st.success(f"✅ Loaded {len(notes.split())} words from {uploaded_file.name}")
            with st.expander("Preview uploaded content"):
                st.text(notes[:500] + "..." if len(notes) > 500 else notes)
    
    # Tips expander
    with st.expander("💡 Tips for Better Results"):
        st.markdown("""
        **Include these for best summaries:**
        - ✅ Participant names ("John will...", "Sarah mentioned...")
        - ✅ Explicit decisions ("We decided to...", "Agreed on...")
        - ✅ Dates and deadlines ("by Friday", "March 15")
        - ✅ Action items with owners
        - ✅ Risks or blockers
        
        **Avoid:**
        - ❌ Super vague notes ("discussed stuff")
        - ❌ Missing context ("it's due soon" - when?)
        - ❌ No names ("someone will do it" - who?)
        """)
    
    # Process button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        process_button = st.button(
            "🚀 Generate Summary",
            type="primary",
            use_container_width=True,
            disabled=not notes.strip()
        )
    
    # Process meeting
    if process_button and notes.strip():
        with st.spinner("🤖 AI is analyzing your meeting notes..."):
            try:
                # Create summarizer
                summarizer = MeetingSummarizer(model=model, verbose=False)
                
                # Process
                results = summarizer.process_meeting(
                    notes=notes,
                    date=date_str,
                    generate_email=generate_email,
                    generate_brief=generate_brief
                )
                
                # Store in session state
                st.session_state.results = results
                st.session_state.cost_summary = summarizer.get_cost_summary()
                
                st.success("✅ Summary generated successfully!")
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Make sure your API key is configured in .env file")
    
    # Display results
    if st.session_state.results:
        st.markdown("---")
        st.header("📄 Results")
        
        results = st.session_state.results
        
        # Cost summary
        if st.session_state.cost_summary:
            cost = st.session_state.cost_summary
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Model", cost['model'])
            with col2:
                st.metric("Tokens", f"{cost['total_tokens']:,}")
            with col3:
                st.metric("API Calls", cost['api_calls'])
            with col4:
                st.metric("Cost", f"${cost['total_cost']:.4f}")
        
        st.markdown("---")
        
        # Summary
        st.subheader("📋 Meeting Summary")
        st.markdown(results['summary'])
        
        # Download button for summary
        st.download_button(
            label="⬇️ Download Summary",
            data=results['summary'],
            file_name=f"meeting_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )
        
        # Email
        if 'email' in results:
            st.markdown("---")
            st.subheader("📧 Follow-up Email")
            st.text_area("Email Draft", results['email'], height=300, key="email_output")
            
            st.download_button(
                label="⬇️ Download Email",
                data=results['email'],
                file_name=f"meeting_email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        
        # Executive Brief
        if 'brief' in results:
            st.markdown("---")
            st.subheader("📊 Executive Brief")
            st.text_area("Brief", results['brief'], height=300, key="brief_output")
            
            st.download_button(
                label="⬇️ Download Brief",
                data=results['brief'],
                file_name=f"executive_brief_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

# TAB 2: Batch Processing
with tab2:
    st.header("Batch Process Multiple Meetings")
    
    st.info("📁 Upload multiple text files to process them all at once")
    
    uploaded_files = st.file_uploader(
        "Choose text files",
        type=['txt', 'md'],
        accept_multiple_files=True,
        help="Select multiple meeting notes files to process in batch"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} files uploaded")
        
        # Show file list
        with st.expander("📋 Files to process"):
            for file in uploaded_files:
                st.text(f"• {file.name}")
        
        # Batch process button
        if st.button("🚀 Process All Files", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results_list = []
            total_cost = 0
            
            for i, file in enumerate(uploaded_files):
                status_text.text(f"Processing {file.name}...")
                
                try:
                    notes = file.read().decode('utf-8')
                    
                    summarizer = MeetingSummarizer(model=model, verbose=False)
                    result = summarizer.process_meeting(
                        notes=notes,
                        generate_email=generate_email,
                        generate_brief=generate_brief
                    )
                    
                    cost = summarizer.get_cost_summary()
                    total_cost += cost['total_cost']
                    
                    results_list.append({
                        'filename': file.name,
                        'result': result,
                        'cost': cost
                    })
                    
                except Exception as e:
                    st.warning(f"⚠️ Failed to process {file.name}: {str(e)}")
                
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            status_text.text("✅ Batch processing complete!")
            
            # Summary
            st.success(f"Processed {len(results_list)}/{len(uploaded_files)} files successfully")
            st.info(f"💰 Total cost: ${total_cost:.4f}")
            
            # Show results
            for item in results_list:
                with st.expander(f"📄 {item['filename']}"):
                    st.markdown(item['result']['summary'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            "⬇️ Download Summary",
                            data=item['result']['summary'],
                            file_name=f"{item['filename']}_summary.md",
                            key=f"download_summary_{item['filename']}"
                        )
                    with col2:
                        if 'email' in item['result']:
                            st.download_button(
                                "⬇️ Download Email",
                                data=item['result']['email'],
                                file_name=f"{item['filename']}_email.txt",
                                key=f"download_email_{item['filename']}"
                            )

# TAB 3: Recent Summaries
with tab3:
    st.header("Recent Summaries")
    
    output_dir = Config.OUTPUT_DIR
    
    if os.path.exists(output_dir):
        # Get all summary files
        summary_files = sorted(
            glob.glob(os.path.join(output_dir, "meeting_summary_*.md")),
            key=os.path.getmtime,
            reverse=True
        )
        
        if summary_files:
            st.info(f"📁 Found {len(summary_files)} recent summaries")
            
            # Show recent summaries
            for file_path in summary_files[:10]:  # Show last 10
                filename = os.path.basename(file_path)
                timestamp = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                with st.expander(f"📄 {timestamp.strftime('%B %d, %Y %H:%M')} - {filename}"):
                    try:
                        with open(file_path, 'r') as f:
                            content = f.read()
                        st.markdown(content)
                        
                        st.download_button(
                            "⬇️ Download",
                            data=content,
                            file_name=filename,
                            key=f"download_{filename}"
                        )
                    except Exception as e:
                        st.error(f"Error reading file: {e}")
        else:
            st.info("📭 No summaries yet. Process your first meeting in the 'Summarize Meeting' tab!")
    else:
        st.info("📭 Output directory doesn't exist yet. Process your first meeting to create it!")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("💡 Tip: Use Cmd+K (Mac) or Ctrl+K (Windows) to search")
with col2:
    st.caption("⚡ Average processing time: 10-30 seconds")
with col3:
    st.caption("💰 Cost per meeting: $0.01-0.20")
