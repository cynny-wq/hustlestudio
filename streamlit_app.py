import streamlit as st
import os
import tempfile
import subprocess
import cv2
import numpy as np


# ============================================================
# 1. CORE PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Hustle Studio",
    page_icon="🚀",
    layout="centered"
)


# ============================================================
# 2. MOBILE-FIRST DESIGN
# ============================================================

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

.result-card {
    background-color: #f8f9fa;
    padding: 16px;
    border-radius: 8px;
    margin-bottom: 16px;
    border-left: 5px solid #ff4b4b;
}

.usage-card {
    background-color: #f8f9fa;
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 8px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. BRANDING
# ============================================================

st.title("🚀 Hustle Studio")

st.success(
    "📱 **Hustler Tip:** Want this as a phone app? "
    "Tap your browser settings (3 dots) and choose "
    "'Add to Home Screen' to create a shortcut."
)

st.markdown(
    "Standalone digital tools designed to help Kenyan content creators grow fast."
)


# ============================================================
# 4. FREE PLAN CONFIGURATION
# ============================================================

FREE_LIMITS = {
    "ideas": 10,
    "hooks": 10,
    "scripts": 5,
    "captions": 3
}


# ============================================================
# 5. PERSISTENT SESSION WORKSPACE
# ============================================================

if "workspace_data" not in st.session_state:

    st.session_state.workspace_data = {
        "hooks": [],
        "script": "",
        "captions": "",
        "current_topic": "",
        "processed_video_data": None,

        # Free usage counters
        "free_ideas_left": FREE_LIMITS["ideas"],
        "free_hooks_left": FREE_LIMITS["hooks"],
        "free_scripts_left": FREE_LIMITS["scripts"],
        "free_captions_left": FREE_LIMITS["captions"],
    }


# Protect against older versions of the app
defaults = {
    "free_ideas_left": FREE_LIMITS["ideas"],
    "free_hooks_left": FREE_LIMITS["hooks"],
    "free_scripts_left": FREE_LIMITS["scripts"],
    "free_captions_left": FREE_LIMITS["captions"],
    "processed_video_data": None,
}

for key, value in defaults.items():

    if key not in st.session_state.workspace_data:
        st.session_state.workspace_data[key] = value


# ============================================================
# 6. HELPER FUNCTIONS
# ============================================================

def usage_available(usage_key):
    """
    Check whether the user still has free usage available.
    """

    return st.session_state.workspace_data[usage_key] > 0


def use_credit(usage_key):
    """
    Deduct one free usage credit.
    """

    if st.session_state.workspace_data[usage_key] > 0:
        st.session_state.workspace_data[usage_key] -= 1
        return True

    return False


def show_upgrade_message(feature_name):
    """
    Display a consistent upgrade message.
    """

    st.error(
        f"🔒 Your free {feature_name} limit has been reached."
    )

    st.info(
        "💰 Upgrade through the Monetization Portal when "
        "paid plans are enabled."
    )


# ============================================================
# 7. SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("🚀 Hustle Studio")
st.sidebar.markdown("---")

workspace_selection = st.sidebar.radio(
    "Navigate Workspace",
    [
        "🧠 Strategy Studio",
        "🎬 Caption King Studio",
        "👤 Monetization Portal"
    ]
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 🆓 Free Plan")

st.sidebar.markdown(
    f"""
    <div class="usage-card">
    💡 Content Ideas<br>
    <strong>{st.session_state.workspace_data['free_ideas_left']}</strong> left
    </div>

    <div class="usage-card">
    🔥 Hook Generations<br>
    <strong>{st.session_state.workspace_data['free_hooks_left']}</strong> left
    </div>

    <div class="usage-card">
    📝 Script Generations<br>
    <strong>{st.session_state.workspace_data['free_scripts_left']}</strong> left
    </div>

    <div class="usage-card">
    🎬 Caption Exports<br>
    <strong>{st.session_state.workspace_data['free_captions_left']}</strong> left
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Free limits reset when a new Streamlit session starts. "
    "Account-based monthly limits will be added later."
)


# ============================================================
# 8. STRATEGY STUDIO
# ============================================================

if workspace_selection == "🧠 Strategy Studio":

    st.subheader("🧠 Strategy Studio")

    st.markdown(
        "Go from an idea to a complete localized production roadmap."
    )

    # --------------------------------------------------------
    # Niche and style
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        niche = st.selectbox(
            "🎯 Select Video Niche",
            [
                "General Hustle & Business",
                "Fashion & Thrift (Mitumba/Bales)",
                "Real Estate & Housing (Bedsitters/Apartments)",
                "Food & Cooking (Pilau/Local Recipes)",
                "Tech & Gadget Reviews",
                "Football & Sports",
                "Beauty & Lifestyle",
                "Motivation & Personal Growth"
            ]
        )

    with col2:

        style = st.selectbox(
            "🎭 Select Delivery Style",
            [
                "Comedic / Local Vibe (Sheng Mix)",
                "Energetic & Fast-Paced",
                "Storytelling & Emotional",
                "Educational & Corporate"
            ]
        )

    topic = st.text_input(
        "💡 What is your video topic?",
        value=st.session_state.workspace_data["current_topic"],
        placeholder="Example: Starting a business with KSh 5,000"
    )

    # ========================================================
    # CONTENT IDEA GENERATOR
    # ========================================================

    st.markdown("---")
    st.subheader("💡 Content Idea Generator")

    st.markdown(
        "Don't know what to post? Generate quick content directions."
    )

    idea_topic = st.text_input(
        "Enter a niche or topic for content ideas",
        placeholder="Example: Kenyan football"
    )

    if st.button("💡 Generate Content Ideas"):

        if not idea_topic.strip():

            st.warning("⚠️ Enter a topic first.")

        elif not usage_available("free_ideas_left"):

            show_upgrade_message("content idea")

        else:

            use_credit("free_ideas_left")

            clean_idea_topic = idea_topic.strip()

            ideas = [
                f"3 mistakes people make when starting {clean_idea_topic}",
                f"The truth nobody tells you about {clean_idea_topic}",
                f"How I would start {clean_idea_topic} with KSh 5,000",
                f"5 things I wish I knew before starting {clean_idea_topic}",
                f"Stop doing this if you want to succeed in {clean_idea_topic}",
                f"Beginner vs expert: {clean_idea_topic}",
                f"Can you actually make money with {clean_idea_topic}?",
                f"The biggest scam people should avoid in {clean_idea_topic}",
                f"A day in the life of someone doing {clean_idea_topic}",
                f"Things nobody warns you about when entering {clean_idea_topic}"
            ]

            st.session_state.workspace_data["idea_results"] = ideas

            st.success(
                f"Generated 10 ideas. "
                f"You have {st.session_state.workspace_data['free_ideas_left']} "
                f"free idea generations left."
            )

    if "idea_results" in st.session_state.workspace_data:

        st.markdown("### 🚀 Your Content Ideas")

        for index, idea in enumerate(
            st.session_state.workspace_data["idea_results"],
            start=1
        ):

            st.markdown(
                f"<div class='result-card'>"
                f"<strong>Idea #{index}</strong><br>{idea}"
                f"</div>",
                unsafe_allow_html=True
            )


    # ========================================================
    # COMPLETE PRODUCTION PACKAGE
    # ========================================================

    st.markdown("---")

    if st.button("🔥 Generate Complete Production Package"):

        if not topic.strip():

            st.warning(
                "⚠️ Please provide a video topic first."
            )

        else:

            # ------------------------------------------------
            # Check both hook and script limits
            # ------------------------------------------------

            if not usage_available("free_hooks_left"):

                show_upgrade_message("hook")

            elif not usage_available("free_scripts_left"):

                show_upgrade_message("script")

            else:

                clean_topic = topic.strip()

                st.session_state.workspace_data[
                    "current_topic"
                ] = clean_topic

                # Deduct credits only when generation starts
                use_credit("free_hooks_left")
                use_credit("free_scripts_left")


                # ============================================
                # HOOK GENERATION
                # ============================================

                hooks = [
                    f"USIWAHI jaribu {clean_topic} hapa Kenya kabla ujue hii siri...",

                    f"Mbona hakuna mtu anakuambia ukweli kuhusu {clean_topic}?",

                    f"Hii hapa siri ya {clean_topic} yenye watu wengi hawataki ujue.",

                    f"Umechoka kuhustle na {clean_topic} na haupati matokeo? "
                    f"Hapa ndio mistake unafanya...",

                    f"Kama ungeanza {clean_topic} leo, hii ndio kitu "
                    f"ningekuambia kwanza."
                ]


                # ============================================
                # SCRIPT VARIABLES
                # ============================================

                script_body = ""
                cta_text = ""
                hashtags = ""


                # ============================================
                # MITUMBA
                # ============================================

                if niche == "Fashion & Thrift (Mitumba/Bales)":

                    hashtags = (
                        "#MitumbaKenya #Gikomba #NairobiFashion "
                        "#ThriftKE #Biashara"
                    )

                    if style == "Comedic / Local Vibe (Sheng Mix)":

                        script_body = (
                            f"Wasee wanadhani kuuza {clean_topic} "
                            f"ni kwenda tu Gikomba mapema kuchagua nguo. "
                            f"Ukweli ni kwamba unapigwa character development "
                            f"na supplier usipochunga!"
                        )

                        cta_text = (
                            "Kama unataka tips za kupata pieces safi, "
                            "nifollow sasa hivi!"
                        )

                    elif style == "Energetic & Fast-Paced":

                        script_body = (
                            f"Stop scrolling! Most people fail at "
                            f"{clean_topic} because they focus on cheap stock "
                            f"instead of quality pieces."
                        )

                        cta_text = (
                            "Follow for more Kenyan business tips!"
                        )

                    elif style == "Storytelling & Emotional":

                        script_body = (
                            f"When I first started looking into "
                            f"{clean_topic}, I made expensive mistakes. "
                            f"Nobody explained the real process to me."
                        )

                        cta_text = (
                            "Follow so you can avoid the mistakes I made."
                        )

                    else:

                        script_body = (
                            f"When evaluating {clean_topic}, "
                            f"focus on inventory velocity, margins "
                            f"and customer demand."
                        )

                        cta_text = (
                            "Follow for more business insights."
                        )


                # ============================================
                # REAL ESTATE
                # ============================================

                elif niche == "Real Estate & Housing (Bedsitters/Apartments)":

                    hashtags = (
                        "#NairobiRentals #Kilimani "
                        "#BedsitterChronicles #Roysambu #KenyaRealEstate"
                    )

                    if style == "Comedic / Local Vibe (Sheng Mix)":

                        script_body = (
                            f"Ukitafuta keja Nairobi, ma-agent watakuambia "
                            f"place iko five minutes from the highway. "
                            f"Ukifika unapata ni safari mzima!"
                        )

                        cta_text = (
                            "Drop your budget and let's talk!"
                        )

                    elif style == "Energetic & Fast-Paced":

                        script_body = (
                            f"Before you pay a deposit for {clean_topic}, "
                            f"check water, security and electricity first."
                        )

                        cta_text = (
                            "Share this with someone looking for a house."
                        )

                    elif style == "Storytelling & Emotional":

                        script_body = (
                            "Moving into my first apartment felt like a dream "
                            "until hidden costs started appearing."
                        )

                        cta_text = (
                            "Follow for more real estate lessons."
                        )

                    else:

                        script_body = (
                            f"When evaluating {clean_topic}, "
                            f"calculate total monthly costs, not just rent."
                        )

                        cta_text = (
                            "Follow for more property insights."
                        )


                # ============================================
                # FOOD
                # ============================================

                elif niche == "Food & Cooking (Pilau/Local Recipes)":

                    hashtags = (
                        "#KenyanFood #PilauSecrets "
                        "#NairobiEats #SwahiliCooking #Chapo"
                    )

                    script_body = (
                        f"Siri ya {clean_topic} kunoga sio kuweka viungo "
                        f"mingi sana. Ni timing! Ukikimbiza moto, "
                        f"unapoteza ile ladha halisi."
                    )

                    cta_text = (
                        "Follow for more Kenyan recipes!"
                    )


                # ============================================
                # TECH
                # ============================================

                elif niche == "Tech & Gadget Reviews":

                    hashtags = (
                        "#TechKenya #NairobiGadgets "
                        "#iPhoneKenya #AndroidKE #Unboxing"
                    )

                    script_body = (
                        f"Wasee wengi wanatumia pesa kwa specs "
                        f"ambazo hawatawahi kutumia. Before buying "
                        f"{clean_topic}, focus on what you actually need."
                    )

                    cta_text = (
                        "Comment the phone you're using!"
                    )


                # ============================================
                # FOOTBALL
                # ============================================

                elif niche == "Football & Sports":

                    hashtags = (
                        "#FootballKenya #KenyaFootball "
                        "#FootballTikTok #SportsKE"
                    )

                    script_body = (
                        f"Wasee wengi wanaangalia {clean_topic} "
                        f"lakini hawajui hii part muhimu. "
                        f"Kama unataka kuboresha game yako, "
                        f"focus on consistency and smart training."
                    )

                    cta_text = (
                        "Follow for more football content!"
                    )


                # ============================================
                # BEAUTY
                # ============================================

                elif niche == "Beauty & Lifestyle":

                    hashtags = (
                        "#BeautyKenya #KenyanCreators "
                        "#LifestyleKE #NairobiBeauty"
                    )

                    script_body = (
                        f"If you're trying {clean_topic}, "
                        f"don't just copy what you see online. "
                        f"Find what actually works for you."
                    )

                    cta_text = (
                        "Follow for more beauty and lifestyle tips."
                    )


                # ============================================
                # MOTIVATION
                # ============================================

                elif niche == "Motivation & Personal Growth":

                    hashtags = (
                        "#MotivationKenya #GrowthMindset "
                        "#KenyanCreators #HustleKE"
                    )

                    script_body = (
                        f"Most people wait until everything is perfect "
                        f"before starting {clean_topic}. "
                        f"The truth is, you learn by starting."
                    )

                    cta_text = (
                        "Follow if you're building something from zero."
                    )


                # ============================================
                # GENERAL BUSINESS
                # ============================================

                else:

                    hashtags = (
                        "#NairobiHustle #BiasharaMkononi "
                        "#KenyanCreators #HustleKE"
                    )

                    if style == "Comedic / Local Vibe (Sheng Mix)":

                        script_body = (
                            f"Wasee wengi wanadhani kuingia kwa "
                            f"{clean_topic} ni kubahatisha tu. "
                            f"Ukikosa strategy safi ya kucheza na wateja, "
                            f"utajipata unarudi nyuma."
                        )

                        cta_text = (
                            "Follow for more Kenyan hustle tips!"
                        )

                    else:

                        script_body = (
                            f"Success with {clean_topic} doesn't happen "
                            f"by chance. You need a clear strategy, "
                            f"consistent execution and attention to customers."
                        )

                        cta_text = (
                            "Follow for more business strategies."
                        )


                # ============================================
                # SAVE GENERATED PACKAGE
                # ============================================

                st.session_state.workspace_data["hooks"] = hooks

                st.session_state.workspace_data["script"] = f"""
### 📝 STRUCTURED SCRIPT ROADMAP

#### 🚨 Phase 1: The Hook

**Selected Hook:**

{hooks[0]}

Speak with energy during the first 3 seconds.

#### 📦 Phase 2: The Core Body

**Visual Direction:**

Mid-shot framing. Look directly into the mobile camera.

**Script:**

{script_body}

#### 🎬 Phase 3: Pacing & Direction

- Cut or change visual every few seconds.
- Add on-screen text for important keywords.
- Keep the background clean.
- Avoid long introductions.
- Get to the value quickly.

#### 🎯 Phase 4: Call To Action

{cta_text}
"""

                st.session_state.workspace_data["captions"] = (
                    f"🎯 The truth about {clean_topic} "
                    f"that nobody shares... 🤫\n\n"
                    f"Watch till the end!\n\n"
                    f"🏷️ Viral Tag Pack:\n"
                    f"{hashtags}\n"
                    f"#ContentCreatorKE"
                )

                st.success(
                    "🚀 Production package generated!"
                )

                st.info(
                    f"Free usage remaining — "
                    f"Hooks: {st.session_state.workspace_data['free_hooks_left']} | "
                    f"Scripts: {st.session_state.workspace_data['free_scripts_left']}"
                )


    # ========================================================
    # DISPLAY PRODUCTION PACKAGE
    # ========================================================

    if st.session_state.workspace_data["script"]:

        st.markdown("---")

        st.subheader(
            "🚀 Your Complete Production Strategy Package"
        )

        with st.expander(
            "💡 1. Localized Hook Variations",
            expanded=True
        ):

            for index, hook in enumerate(
                st.session_state.workspace_data["hooks"],
                start=1
            ):

                st.markdown(
                    f"<div class='result-card'>"
                    f"<strong>Hook Option #{index}:</strong><br>"
                    f"{hook}"
                    f"</div>",
                    unsafe_allow_html=True
                )


        with st.expander(
            "📝 2. High-Retention Script & Video Direction",
            expanded=True
        ):

            st.markdown(
                st.session_state.workspace_data["script"]
            )


        with st.expander(
            "📲 3. Social Media Optimization Kit",
            expanded=True
        ):

            st.text_area(
                "Copy Caption Pack:",
                value=st.session_state.workspace_data["captions"],
                height=150
            )


# ============================================================
# 9. CAPTION KING
# ============================================================

elif workspace_selection == "🎬 Caption King Studio":

    st.title("🎬 Caption King Studio")

    st.markdown(
        "Burn stylized text directly into your short-form video."
    )

    trials_left = (
        st.session_state.workspace_data[
            "free_captions_left"
        ]
    )

    if trials_left > 0:

        st.success(
            f"🎁 **Free Trial Active:** "
            f"You have **{trials_left} out of "
            f"{FREE_LIMITS['captions']}** free caption exports left."
        )

    else:

        st.error(
            "🔒 Your free caption exports have been used."
        )

        st.info(
            "💡 Visit the Monetization Portal to view upgrade options."
        )


    uploaded_video = st.file_uploader(
        "Upload your raw MP4 video clip (Max 25MB)",
        type=["mp4", "mov"]
    )


    col1, col2, col3 = st.columns(3)

    with col1:

        font_style = st.selectbox(
            "Subtitle Font",
            [
                "Impact Bold",
                "Montserrat ExtraBold",
                "Sheng Modern"
            ]
        )

    with col2:

        caption_pos = st.selectbox(
            "Text Position",
            [
                "Center",
                "Lower Third",
                "Top Drop"
            ]
        )

    with col3:

        accent_color = st.color_picker(
            "Accent Highlight Color",
            "#FF4B4B"
        )


    if st.button("🎬 Run Subtitle Generation"):

        if uploaded_video is None:

            st.error(
                "❌ Please upload a valid MP4 video first."
            )

        elif not usage_available("free_captions_left"):

            show_upgrade_message("caption export")

        else:

            with st.spinner(
                "🧠 Processing your video..."
            ):

                temp_input_path = None
                temp_silent_video_path = None
                temp_final_mux_path = None

                try:

                    # ----------------------------------------
                    # SAVE INPUT VIDEO
                    # ----------------------------------------

                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".mp4"
                    ) as temp_input:

                        temp_input.write(
                            uploaded_video.read()
                        )

                        temp_input_path = temp_input.name


                    # ----------------------------------------
                    # OPEN VIDEO
                    # ----------------------------------------

                    cap = cv2.VideoCapture(
                        temp_input_path
                    )

                    width = int(
                        cap.get(
                            cv2.CAP_PROP_FRAME_WIDTH
                        )
                    )

                    height = int(
                        cap.get(
                            cv2.CAP_PROP_FRAME_HEIGHT
                        )
                    )

                    fps = cap.get(
                        cv2.CAP_PROP_FPS
                    )

                    if fps == 0 or np.isnan(fps):

                        fps = 30.0


                    # ----------------------------------------
                    # OUTPUT VIDEO
                    # ----------------------------------------

                    temp_silent_video_path = tempfile.mktemp(
                        suffix=".mp4"
                    )

                    fourcc = cv2.VideoWriter_fourcc(
                        *"mp4v"
                    )

                    out = cv2.VideoWriter(
                        temp_silent_video_path,
                        fourcc,
                        fps,
                        (width, height)
                    )


                    # ----------------------------------------
                    # CAPTION TEXT
                    # ----------------------------------------

                    subtitle_text = (
                        "Hustle Studio Content"
                    )

                    current_topic = (
                        st.session_state.workspace_data[
                            "current_topic"
                        ]
                    )

                    if current_topic:

                        subtitle_text = (
                            f"Siri ya {current_topic} Kenya!"
                        )


                    # ----------------------------------------
                    # COLOR
                    # ----------------------------------------

                    hex_color = accent_color.lstrip("#")

                    bg_color_bgr = tuple(
                        int(
                            hex_color[i:i + 2],
                            16
                        )
                        for i in (4, 2, 0)
                    )


                    # ----------------------------------------
                    # FONT
                    # ----------------------------------------

                    font_face = cv2.FONT_HERSHEY_SIMPLEX

                    if font_style == "Impact Bold":

                        font_face = cv2.FONT_HERSHEY_TRIPLEX

                    elif font_style == "Montserrat ExtraBold":

                        font_face = cv2.FONT_HERSHEY_DUPLEX

                    elif font_style == "Sheng Modern":

                        font_face = cv2.FONT_HERSHEY_COMPLEX


                    font_scale = max(
                        1.0,
                        width / 450.0
                    )

                    thickness = max(
                        2,
                        int(font_scale * 2.5)
                    )


                    # ----------------------------------------
                    # FRAME PROCESSING
                    # ----------------------------------------

                    while cap.isOpened():

                        ret, frame = cap.read()

                        if not ret:
                            break


                        (
                            text_w,
                            text_h
                        ), baseline = cv2.getTextSize(
                            subtitle_text,
                            font_face,
                            font_scale,
                            thickness
                        )


                        x = int(
                            (width - text_w) / 2
                        )


                        if caption_pos == "Center":

                            y = int(
                                (height + text_h) / 2
                            )

                        elif caption_pos == "Top Drop":

                            y = int(
                                height * 0.2
                            )

                        else:

                            y = int(
                                height * 0.75
                            )


                        pad_x = int(
                            20 * font_scale
                        )

                        pad_y = int(
                            15 * font_scale
                        )


                        # Background
                        cv2.rectangle(
                            frame,
                            (
                                x - pad_x,
                                y - text_h - pad_y
                            ),
                            (
                                x + text_w + pad_x,
                                y + baseline + pad_y
                            ),
                            bg_color_bgr,
                            -1
                        )


                        # Black outline
                        cv2.putText(
                            frame,
                            subtitle_text,
                            (x, y),
                            font_face,
                            font_scale,
                            (0, 0, 0),
                            thickness + 3,
                            cv2.LINE_AA
                        )


                        # White text
                        cv2.putText(
                            frame,
                            subtitle_text,
                            (x, y),
                            font_face,
                            font_scale,
                            (255, 255, 255),
                            thickness,
                            cv2.LINE_AA
                        )


                        out.write(frame)


                    cap.release()
                    out.release()


                    # ----------------------------------------
                    # RESTORE AUDIO
                    # ----------------------------------------

                    temp_final_mux_path = tempfile.mktemp(
                        suffix=".mp4"
                    )

                    ffmpeg_cmd = [
                        "ffmpeg",
                        "-y",
                        "-i",
                        temp_silent_video_path,
                        "-i",
                        temp_input_path,
                        "-map",
                        "0:v:0",
                        "-map",
                        "1:a:0?",
                        "-c:v",
                        "libx264",
                        "-pix_fmt",
                        "yuv420p",
                        "-c:a",
                        "aac",
                        "-shortest",
                        temp_final_mux_path
                    ]


                    subprocess.run(
                        ffmpeg_cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=True
                    )


                    # ----------------------------------------
                    # STORE OUTPUT
                    # ----------------------------------------

                    with open(
                        temp_final_mux_path,
                        "rb"
                    ) as video_file:

                        st.session_state.workspace_data[
                            "processed_video_data"
                        ] = video_file.read()


                    # ----------------------------------------
                    # DEDUCT CREDIT ONLY AFTER SUCCESS
                    # ----------------------------------------

                    use_credit(
                        "free_captions_left"
                    )


                    st.success(
                        "🎉 Captioned video created successfully!"
                    )

                    st.rerun()


                except Exception as error:

                    st.error(
                        f"❌ Video Processing Error: {error}"
                    )


                finally:

                    # ----------------------------------------
                    # CLEAN TEMP FILES
                    # ----------------------------------------

                    for temp_path in [
                        temp_input_path,
                        temp_silent_video_path,
                        temp_final_mux_path
                    ]:

                        if temp_path and os.path.exists(
                            temp_path
                        ):

                            try:

                                os.unlink(temp_path)

                            except Exception:

                                pass


    # ========================================================
    # OUTPUT VIDEO
    # ========================================================

    if (
        st.session_state.workspace_data[
            "processed_video_data"
        ] is not None
    ):

        st.markdown("---")

        st.success(
            "🎉 Your captioned video is ready!"
        )

        st.video(
            st.session_state.workspace_data[
                "processed_video_data"
            ]
        )

        st.download_button(
            label="📥 Download Subtitled Video",
            data=st.session_state.workspace_data[
                "processed_video_data"
            ],
            file_name="hustlestudio_captioned.mp4",
            mime="video/mp4"
        )


# ============================================================
# 10. MONETIZATION PORTAL
# ============================================================

elif workspace_selection == "👤 Monetization Portal":

    st.title("👤 Monetization Portal")

    st.markdown(
        "Unlock more tools and higher usage limits."
    )


    # ========================================================
    # FREE PLAN
    # ========================================================

    st.subheader("🆓 Free Strategy Plan")

    st.markdown(
        f"""
        <div style="
            background-color:#f8f9fa;
            padding:20px;
            border-radius:10px;
            border:1px solid #ddd;
            color:#222;
        ">

        <h3>Free</h3>

        <p>Perfect for trying Hustle Studio.</p>

        <ul>
            <li>10 content idea generations</li>
            <li>10 hook generations</li>
            <li>5 script generations</li>
            <li>3 caption exports</li>
            <li>Mobile-friendly creator workflow</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown("---")


    # ========================================================
    # WEEKLY PLAN
    # ========================================================

    st.subheader("🚀 Weekly Pass")

    st.markdown(
        """
        <div style="
            background-color:#fff;
            padding:20px;
            border-radius:8px;
            border:1px solid #ddd;
            text-align:center;
            color:#333;
        ">

        <h3>🚀 Weekly Pass</h3>

        <h2 style="color:#ff4b4b;">
        KSh 150
        </h2>

        <p>7 days of creator tools</p>

        <p>
        • Higher usage limits<br>
        • More subtitle exports<br>
        • Full creator workflow<br>
        • Priority processing when available
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    if st.button(
        "Unlock Weekly Access Pass",
        key="pay_weekly"
    ):

        st.info(
            "📲 M-Pesa payment integration will be connected "
            "in the next monetization stage."
        )


    st.markdown("---")


    # ========================================================
    # PRO PLAN
    # ========================================================

    st.subheader("🏆 Creator Pro")

    st.markdown(
        """
        <div style="
            background-color:#fff;
            padding:20px;
            border-radius:8px;
            border:2px solid #ff4b4b;
            text-align:center;
            color:#333;
        ">

        <h3>🏆 Creator Pro</h3>

        <h2 style="color:#ff4b4b;">
        KSh 500
        </h2>

        <p>Per month</p>

        <p>
        • Higher AI usage<br>
        • More caption exports<br>
        • Advanced creator tools<br>
        • Priority processing<br>
        • Future analytics features
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    if st.button(
        "Unlock Creator Pro",
        key="pay_monthly"
    ):

        st.info(
            "📲 M-Pesa subscription integration will be "
            "connected in the next monetization stage."
        )


# ============================================================
# 11. FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🚀 Hustle Studio — Built for creators who want to hustle smarter."
)
