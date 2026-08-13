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
    st.markdown("Turn your selected hook into a structured script config mapped to your specific business niche.")
    
    active_hook = st.text_area(
        "Your Selected Video Hook:", 
        value=st.session_state.selected_hook,
    )

    video_niche = st.selectbox(
        "🎯 Select Video Niche / Category",
        [
            "General Hustle & Business",
            "Fashion & Thrift (Mitumba/Bales)",
            "Real Estate & Housing (Bedsitters/Apartments)",
            "Food & Cooking (Pilau/Local Recipes)",
            "Tech & Gadget Reviews"
        ]
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
            topic = st.session_state.current_topic if st.session_state.current_topic else "this business"
            
            script_body = ""
            cta = ""

            if video_niche == "Fashion & Thrift (Mitumba/Bales)":
                if delivery_style == "Comedic / Local Vibe (Sheng Mix)":
                    script_body = f"Wasee wanadhani kuuza {topic} ni kwenda tu Gikomba asubuhi na kuchagua nguo. Ukweli ni kwamba unapigwa character development na supplier usipochunga!"
                    cta = f"Kama unataka kupata zile camera pieces safi za {topic} bila kuoshwa, nifollow sasa hivi!"
                else:
                    script_body = f"The secret to making margins with {topic} isn't just buying cheap bales. It's about styling the pieces uniquely on camera so they look like high-end designer wear."
                    cta = f"We restock unique items weekly. Click the link in our bio to join our exclusive WhatsApp group!"

            elif video_niche == "Real Estate & Housing (Bedsitters/Apartments)":
                if delivery_style == "Storytelling & Emotional":
                    script_body = f"When you are looking for houses around Nairobi, agents will show you a place and call it '5 minutes from the highway' town, only to find out you need a whole safari to get there."
                    cta = f"Don't get scammed by fake house listings. Drop a comment with your budget and I'll find a match."
                else:
                    script_body = f"Before signing that lease or paying a deposit for {topic}, you must inspect the water consistency, tokens billing system, and security structure of that zone."
                    cta = f"Share this video with a friend who is planning to relocate or upgrade houses soon!"

            elif video_niche == "Food & Cooking (Pilau/Local Recipes)":
                script_body = f"Siri ya {topic} kunoga sio kuweka viungo mingi sana. Ni timing! Ukikimbiza moto, kila kitu kinaungua na unapoteza ule ladha halisi ya nyumbani."
                cta = f"Tafadhali hit that follow button for more quick, budget-friendly Kenyan recipes every week!"

            elif video_niche == "Tech & Gadget Reviews":
                script_body = f"People always overpay for specifications they don't even use. You don't need a high-end flagship setup just to run basic operations for your {topic} tasks."
                cta = f"Drop the name of your current phone model in the comments, and I'll tell you if it's time to upgrade!"

            else:  # General Hustle & Business
                if delivery_style == "Comedic / Local Vibe (Sheng Mix)":
                    script_body = f"Wasee wengi wanadhani {topic} ni mchezo, lakini ukweli ni kwamba unahitaji strategy safi. Sio kila siku unacheza bahati nasibu hapa Nairobi."
                    cta = f"Kama unataka kuacha kuangusha amani na {topic}, nifollow sasa hivi upate maujuzi kila siku!"
                elif delivery_style == "Energetic & Fast-Paced":
                    script_body = f"Stop scrolling! Most people fail at {topic} because they skip the most important foundation step. You need to focus on what actually moves the needle."
                    cta = f"Hit that follow button right now if you want to scale your {topic} game this month!"
                else:
                    script_body = f"Success in {topic} requires consistency. The market shifts daily in East Africa, and those who track data manually are getting left behind."
                    cta = f"Save this video for reference and follow this page for weekly market breakdowns."

            st.session_state.generated_script = f"""### 🚨 1. HOOK
"{active_hook}"

### 📦 2. BODY STORY
* **[Niche Target]:** {video_niche}
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

    # Indentation explicitly aligned to separate structural levels safely
    if st.button("👑 Compile Viral Captions"):
        if script_context.strip():
