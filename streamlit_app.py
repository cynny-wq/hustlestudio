import streamlit as st
import os
import uuid
import subprocess
import shutil

# 1. CORE WEB PAGE CONFIGURATION
st.set_page_config(
    page_title="HustleStudio Suite", 
    page_icon="🚀", 
    layout="centered"
)

# 2. MOBILE-FIRST RESPONSIVE DESIGN (Custom CSS Injection)
st.markdown("""
    <style>
    /* Expands buttons to full-width and adds padding for easy mobile thumb tapping */
    div.stButton > button:first-child {
        width: 100%;
        padding: 14px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 8px !important;
    }
    /* Adds vertical breathing room to dropdown selection menus on small displays */
    div[data-baseweb="select"] {
        padding: 6px 0;
    }
    /* Styles the custom notification box for generated viral text results */
    .hook-box {
        background-color: #f1f3f6;
        padding: 14px;
        border-radius: 8px;
        margin-bottom: 12px;
        border-left: 5px solid #ff4b4b;
    }
    </style>
""", unsafe_allow_html=True)

# 3. APP HEADERS & LOCALIZED BRANDING COPY
st.title("🚀 HustleStudio Suite")

# The instant web-app shortcut prompt for phone users
st.success(
    "📱 **Hustler Tip:** Want this as a phone app? Tap your browser settings "
    "(3 dots) and click **'Add to Home Screen'** to get an instant shortcut icon on your phone!"
)

st.markdown("Standalone digital tools designed to help Kenyan content creators grow fast.")
# ==========================================
# BLOCK 2: PERSISTENT MEMORY & TABS
# ==========================================

# 1. INITIALIZE GLOBAL PIPELINE STATE KEYS
# This forces Streamlit to remember data across refreshes
if "generated_hooks" not in st.session_state:
    st.session_state.generated_hooks = []
if "current_topic" not in st.session_state:
    st.session_state.current_topic = ""
if "selected_hook" not in st.session_state:
    st.session_state.selected_hook = ""
if "generated_script" not in st.session_state:
    st.session_state.generated_script = ""

# 2. CREATE WORKSPACE NAVIGATION TABS
# Organizes the tool collection into a sequential 3-step workflow pipeline
tab1, tab2, tab3 = st.tabs([
    "💡 1: Viral Hook Bot", 
    "📝 2: AI Script Builder", 
    "🎬 3: Caption King"
])
# ==========================================
# BLOCK 3: TOOL 1 — VIRAL HOOK BOT
# ==========================================
with tab1:
    st.subheader("💡 Tool 1: Viral Hook Bot")
    st.markdown("Beat creative block instantly. Get hooks tailored for local Kenyan audiences.")
    
    # Text input field linked directly to memory state
    topic_input = st.text_input(
        "What is your video about? (e.g., 'selling shoes', 'cooking pilau')", 
        value=st.session_state.current_topic,
        key="hooks_topic_field"
    )
    
    if st.button("⚡ Generate Hooks"):
        cleaned_topic = topic_input.strip()
        if cleaned_topic:
            # Save the active topic to global state
            st.session_state.current_topic = cleaned_topic
            
            # Localized formatting models optimized for Nairobi content trends
            st.session_state.generated_hooks = [
                f"USIWAHI jaribu {cleaned_topic} hapa Kenya kabla ujue hii siri...",
                f"Mbona hakuna mtu anakuambia ukweli kuhusu {cleaned_topic}?",
                f"Hii hapa siri ya {cleaned_topic} yenye matajiri wa Nairobi hawataki ujue.",
                f"Umechoka kuhustle na {cleaned_topic} na haupati matokeo? Hapa ndio mistake unafanya..."
            ]
        else:
            st.warning("⚠️ Please input a topic description first.")

    # Render hooks out of memory state if they exist
    if st.session_state.generated_hooks:
        st.markdown(f"### 🚀 Viral Hooks Generated for: '{st.session_state.current_topic}'")
        st.caption("Click a hook below to push it straight into the AI Script Builder (Tab 2):")
        
        # Loop through hooks and add a data-forwarding pipeline button to each
        for i, hook_text in enumerate(st.session_state.generated_hooks, start=1):
            with st.container():
                # Render using the responsive mobile styling we defined in Block 1
                st.markdown(f"<div class='hook-box'><strong>Hook #{i}:</strong> {hook_text}</div>", unsafe_allow_html=True)
                
                # Assign a unique button key per loop item to prevent Streamlit render conflicts
                if st.button(f"⚡ Use Hook #{i} for my Script", key=f"fwd_hook_{i}"):
                    st.session_state.selected_hook = hook_text
                    st.success("👉 Hook sent! Open the 'AI Script Builder' tab to complete your script.")
# ==========================================
# BLOCK 4: TOOL 2 — AI SCRIPT BUILDER
# ==========================================
with tab2:
    st.subheader("📝 Tool 2: AI Script Builder")
    st.markdown("Turn your selected hook into a full, high-retention video script with visual cues and a clear Call-To-Action (CTA).")
    
    # 1. LIVE SECURITY API KEY VALIDATION CHANNELS
    # Pulls securely from either cloud secrets environment maps or local runtimes
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))
    
    if not GROQ_API_KEY:
        st.error("🔑 **System Configuration Missing:** Please set your `GROQ_API_KEY` in your Streamlit Secrets panel to enable AI Generation features.")

    # 2. DATA PIPELINE DROPPING INPUT LAYER
    # Auto-populates text dynamically if a button was clicked in Tab 1
    active_hook = st.text_area(
        "Your Selected Video Hook:", 
        value=st.session_state.selected_hook,
        help="You can click a hook from Tab 1 to load it here automatically, or type a custom one manually."
    )

    delivery_style = st.selectbox(
        "🎭 Video Delivery Style", 
        [
            "Energetic & Fast-Paced", 
            "Storytelling & Emotional", 
            "Educational & Corporate", 
            "Comedic / Local Vibe (Sheng Mix)"
        ]
    )

    # 3. HIGH-SPEED CLOUD RUNTIME COMPILATION TRIPS
    if st.button("🔥 Generate Full High-Retention Script") and GROQ_API_KEY:
        if active_hook.strip():
            with st.spinner("🧠 Writing your high-retention script via Cloud LLM Engine..."):
                try:
                    from groq import Groq # Localized import pattern protects baseline performance
                    client = Groq(api_key=GROQ_API_KEY)
                    
                    system_prompt = (
                        "You are an expert short-form content scriptwriter specializing in TikTok, Reels, and YouTube Shorts "
                        "for the East African ecosystem. Create highly engaging video scripts using clear text formatting. "
                        "Include structural placeholders like [Visual Cue], [Audio / Sound Effect], and [On-Screen Text]. "
                        "Keep the style direct, authentic, and optimized for high completion rates. Use Kenyan context where appropriate."
                    )
                    
                    user_prompt = f"""
                    Write a short-form video script (30-60 seconds) based on this information:
                    - Video Hook: "{active_hook}"
                    - General Topic: "{st.session_state.current_topic}"
                    - Tone/Style: {delivery_style}
                    
                    Format the output cleanly. Break the response into 4 distinct blocks:
                    1. 🚨 HOOK (The raw text to say in the first 3 seconds)
                    2. 📦 BODY STORY (2-3 punchy, high-value lines)
                    3. 🎬 VISUAL / SHOOTING INSTRUCTIONS (Simple guide on how to record this with a mobile phone)
                    4. 🎯 CALL TO ACTION (CTA tailored to gain followers or profile clicks)
                    """

                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        model="llama3-70b-8192",  # Standard stable high-capacity inference engine token tracking
                        temperature=0.7
                    )
                    
                    # Store generated payload buffer back to memory mapping layers
                    st.session_state.generated_script = chat_completion.choices.message.content
                    
                except Exception as e:
                    st.error(f"⚠️ Script Generation Failure: {str(e)}")
        else:
            st.warning("⚠️ Please select or type a hook first before generating a script.")

    # 4. RENDER DATA FROM PERSISTENT WORKSPACE CACHE
    if st.session_state.generated_script:
        st.markdown("### 🎬 Your Generated Video Blueprint")
        st.markdown(st.session_state.generated_script)
        st.info("💡 **Next Step:** Copy your script, record the video on your phone, and then upload it to the **Caption King** tab above to burn your custom titles!")
# ==========================================
# BLOCK 5: TOOL 3 — CAPTION KING
# ==========================================
with tab3:
    st.subheader("🎬 Tool 3: Caption King")
    st.markdown("Upload your video file to burn clean, styled mobile titles automatically.")
    
    # 1. LIVE SECURITY API KEY VALIDATION CHANNELS
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))
    
    if not GROQ_API_KEY:
        st.error("🔑 **System Configuration Missing:** Please set your `GROQ_API_KEY` in your Streamlit Secrets panel to enable video features.")
    
    # Vertical stacked video style parameter configs
    font_style = st.selectbox("🔤 Font Type", ["Impact", "Arial", "Trebuchet MS"])
    text_position = st.selectbox("📍 Screen Position", ["Bottom Center", "Middle Center", "Top Center"])
    font_color = st.selectbox("🎨 Accent Color", ["Yellow", "White", "Cyan"])
        
    uploaded_file = st.file_uploader("Upload Video (MP4)", type=["mp4"], key="video_uploader_field")
    
    if uploaded_file is not None and GROQ_API_KEY:
        if st.button("🔥 Burn Custom Subtitles"):
            
            # STAGE 1 CRITICAL THREAD-SAFETY FIX: Generate a unique folder workspace per user execution block
            session_id = str(uuid.uuid4())
            working_dir = os.path.join("tmp", session_id)
            os.makedirs(working_dir, exist_ok=True)
            
            input_path = os.path.join(working_dir, "input_video.mp4")
            srt_path = os.path.join(working_dir, "subtitles.srt")
            output_path = os.path.join(working_dir, "output_captioned.mp4")
            
            try:
                # Save the uploaded byte buffer stream to the isolated workspace folder path
                with open(input_path, "wb") as f:
                    f.write(uploaded_file.read())
                    
                # STAGE 3 PERFORMANCE UPGRADE: Fast API-driven Cloud Transcription Engine
                with st.spinner("⚡ Step 1: Transcribing speech instantly via Cloud Engine..."):
                    from groq import Groq
                    client = Groq(api_key=GROQ_API_KEY)
                    
                    with open(input_path, "rb") as video_file:
                        transcription = client.audio.transcriptions.create(
                            file=video_file,
                            model="whisper-large-v3",
                            response_format="srt", # Request native SRT caption styling blocks directly from cloud
                            prompt="This audio contains Kenyan English, Swahili, and Nairobi Sheng slang like hustler, matatu, baze, wapi, rada, form." # Dynamic localization engine seed context
                        )
                    
                    # Save raw cloud subtitle text straight into workspace environment directories
                    with open(srt_path, "w", encoding="utf-8") as srt:
                        srt.write(str(transcription))
                            
                with st.spinner("🔥 Step 2: Running layout styles and burning captions..."):
                    align = "2" if text_position == "Bottom Center" else ("10" if text_position == "Middle Center" else "6")
                    color = "&H00FFFF" if font_color == "Yellow" else ("&FFFFFF" if font_color == "White" else "&HFFFF00")
                    
                    # Custom subtitle font specifications layout mapping dictionary values
                    style_str = f"Fontname={font_style},Fontsize=22,PrimaryColour={color},OutlineColour=&H000000,BorderStyle=1,Outline=2,Alignment={align}"
                    
                    # STAGE 1 MOBILE COMPATIBILITY FIX: Force native H.264 video rendering maps (-c:v libx264)
                    cmd = [
                        "ffmpeg", "-i", input_path,
                        "-vf", f"subtitles={srt_path}:force_style='{style_str}'",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p",
                        "-c:a", "copy", output_path, "-y"
                    ]
                    
                    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    
                if process.returncode == 0 and os.path.exists(output_path):
                    st.success("✅ Video captioned perfectly!")
                    with open(output_path, "rb") as video_file:
                        st.video(video_file.read())
                else:
                    st.error("❌ Encoding runtime error during compilation processing.")
                    st.sidebar.error(f"FFmpeg Log Error: {process.stderr}")
                    
            except Exception as e:
                st.error(f"⚠️ Application Processing Error: {str(e)}")
                
            finally:
                # Cleanup: Securely drop file traces out of physical disk structures instantly
                if os.path.exists(working_dir):
                    shutil.rmtree(working_dir)

