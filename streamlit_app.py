import streamlit as st

# ==========================================
# BLOCK 1: CONFIGURATION & CUSTOM STYLE
# ==========================================

st.set_page_config(
    page_title="HustleStudio Suite", 
    page_icon="🚀", 
    layout="centered"
)

st.markdown("""
    <style>
    div.stButton > button:first-child {
        width: 100%;
        padding: 14px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] {
        padding: 6px 0;
    }
    .hook-box {
        background-color: #f1f3f6;
        padding: 14px;
        border-radius: 8px;
        margin-bottom: 12px;
        border-left: 5px solid #ff4b4b;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 HustleStudio Suite")

st.success(
    "📱 **Hustler Tip:** Want this as a phone app? Tap your browser settings "
    "(3 dots) and click **'Add to Home Screen'** to get an instant shortcut icon on your phone!"
)

st.markdown("Standalone digital tools designed to help Kenyan content creators grow fast.")

# ==========================================
# BLOCK 2: PERSISTENT MEMORY & TABS
# ==========================================

if "generated_hooks" not in st.session_state:
    st.session_state.generated_hooks = []
if "current_topic" not in st.session_state:
    st.session_state.current_topic = ""
if "selected_hook" not in st.session_state:
    st.session_state.selected_hook = ""
if "generated_script" not in st.session_state:
    st.session_state.generated_script = ""

tab1, tab2, tab3 = st.tabs([
    "💡 1: Viral Hook Bot", 
    "📝 2: Local Script Builder", 
    "🎬 3: Caption King"
])

# ==========================================
# BLOCK 3: TOOL 1 — VIRAL HOOK BOT (Free)
# ==========================================
with tab1:
    st.subheader("💡 Tool 1: Viral Hook Bot")
    st.markdown("Beat creative block instantly. Get hooks tailored for local Kenyan audiences.")
    
    topic_input = st.text_input(
        "What is your video about? (e.g., 'selling shoes', 'cooking pilau')", 
        value=st.session_state.current_topic,
        key="hooks_topic_field"
    )
    
    if st.button("⚡ Generate Hooks"):
        cleaned_topic = topic_input.strip()
        if cleaned_topic:
            st.session_state.current_topic = cleaned_topic
            
            st.session_state.generated_hooks = [
                f"USIWAHI jaribu {cleaned_topic} hapa Kenya kabla ujue hii siri...",
                f"Mbona hakuna mtu anakuambia ukweli kuhusu {cleaned_topic}?",
                f"Hii hapa siri ya {cleaned_topic} yenye matajiri wa Nairobi hawataki ujue.",
                f"Umechoka kuhustle na {cleaned_topic} na haupati matokeo? Hapa ndio mistake unafanya..."
            ]
        else:
            st.warning("⚠️ Please input a topic description first.")

    if st.session_state.generated_hooks:
        st.markdown(f"### 🚀 Viral Hooks Generated for: '{st.session_state.current_topic}'")
        st.caption("Click a hook below to push it straight into the Script Builder (Tab 2):")
        
        for i, hook_text in enumerate(st.session_state.generated_hooks, start=1):
            with st.container():
                st.markdown(f"<div class='hook-box'><strong>Hook #{i}:</strong> {hook_text}</div>", unsafe_allow_html=True)
                
                if st.button(f"⚡ Use Hook #{i} for my Script", key=f"fwd_hook_{i}"):
                    st.session_state.selected_hook = hook_text
                    st.success("👉 Hook sent! Open the 'Local Script Builder' tab to complete your script.")

# ==========================================
# BLOCK 4: TOOL 2 — LOCAL SCRIPT BUILDER (100% Free)
# ==========================================
with tab2:
    st.subheader("📝 Tool 2: Local Script Builder")
    st.markdown("Turn your selected hook into a structured script configuration without using AI credits.")
    
    active_hook = st.text_area(
        "Your Selected Video Hook:", 
        value=st.session_state.selected_hook,
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

    if st.button("🔥 Compile High-Retention Script"):
        if active_hook.strip():
            topic = st.session_state.current_topic if st.session_state.current_topic else "this industry"
            
            # Localized architectural templates mapping based on user selection
            if delivery_style == "Comedic / Local Vibe (Sheng Mix)":
                script_body = f"Wasee wengi wanadhani {topic} ni mchezo, lakini ukweli ni kwamba unahitaji strategy safi. Sio kila siku unacheza bahati nasibu hapa Nairobi."
                cta = f"Kama unataka kuacha kuangusha amani na {topic}, nifollow sasa hivi upate maujuzi kila siku!"
            elif delivery_style == "Energetic & Fast-Paced":
                script_body = f"Stop scrolling! Most people fail at {topic} because they skip the most important foundation step. You need to focus on what actually moves the needle."
                cta = f"Hit that follow button right now if you want to scale your {topic} game this month!"
            elif delivery_style == "Storytelling & Emotional":
                script_body = f"When I first started looking into {topic}, I lost so much time trying to figure it out alone. Nobody was willing to share the real steps to success."
                cta = f"Drop a comment sharing your biggest challenge with {topic}, and let's win together."
            else:  # Educational & Corporate
                script_body = f"Data shows that efficiency in {topic} relies on clear preparation and avoiding repetitive administrative bottlenecks."
                cta = f"Save this video for reference and follow this page for weekly market breakdowns."

            # Structure compiled engine text block
            st.session_state.generated_script = f"""### 🚨 1. HOOK
"{active_hook}"

### 📦 2. BODY STORY
* **[Visual Cue]:** Close up shot talking directly to the mobile phone lens.
* **[Script Text]:** {script_body}

### 🎬 3. VISUAL / SHOOTING INSTRUCTIONS
* Use clean daylight facing a window.
* Cut every 3 seconds to keep video retention graph high.
* Add bold, dynamic on-screen text overlays matching keywords.

### 🎯 4. CALL TO ACTION (CTA)
* **[Script Text]:** {cta}
"""
            st.balloons()
        else:
            st.warning("⚠️ Please provide or select a video hook first.")

    if st.session_state.generated_script:
        st.markdown("### 🎬 Your Compiled Video Script")
        st.markdown(st.session_state.generated_script)

# ==========================================
# BLOCK 5: TOOL 3 — CAPTION KING (100% Free)
# ==========================================
with tab3:
    st.subheader("🎬 Tool 3: Caption King")
    st.markdown("Generate platform descriptions and comment anchors using static algorithms.")

    script_context = st.text_area(
        "Script Reference for Caption Design:",
        value=st.session_state.generated_script,
        height=150,
    )

    platform = st.selectbox(
        "📲 Target Social Platform",
        ["TikTok", "Instagram Reels", "YouTube Shorts", "Facebook Reels"]
    )

    if st.button("👑 Compile Viral Captions"):
        if script_context.strip():
            topic = st.session_state.current_topic if st.session_state.current_topic else "Hustle"
            
            # Static generation formulas bypassing cloud costs entirely
            st.markdown("### 🏆 Your Caption Optimization Package")
            st.markdown(f"""
### 💥 Caption Variant 1
"The raw truth about {topic} that nobody tells you... 🤫 Watch till the end! #{platform}Tips"

### 💥 Caption Variant 2
"Don't make this mistake in Kenya! 🛑 Drop your thoughts below. 👇"

### 🏷️ Optimized Local Hashtag Pack
`#KenyaTikTok #NairobiHustle #GainWithMchina #{platform}Marketing #{topic}Kenya #ContentCreatorKE #Biashara`

### 📌 Comment Pin Strategy
* **Pin this question:** *"Ni mistake gani ushawai fanya ukijaribu hii? Let's talk in the comments! 👇"*
""")
        else:
            st.warning("⚠️ Please provide a video script or text context first.")
