import streamlit as st
import os
import tempfile
import subprocess
import cv2
import numpy as np


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Hustle Studio",
    page_icon="🚀",
    layout="centered"
)


# ============================================================
# 2. HUSTLE STUDIO UI / CSS
# ============================================================

st.markdown("""
<style>

/* =========================================================
   GLOBAL
   ========================================================= */

.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* =========================================================
   BUTTONS
   ========================================================= */

div.stButton > button:first-child {
    width: 100%;
    min-height: 48px;
    padding: 12px 16px !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    transition: all 0.2s ease;
}

div.stButton > button:first-child:hover {
    transform: translateY(-1px);
}


/* =========================================================
   SELECT BOXES
   ========================================================= */

div[data-baseweb="select"] {
    margin-bottom: 8px;
}


/* =========================================================
   TEXT INPUTS
   ========================================================= */

div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea {
    border-radius: 10px !important;
}


/* =========================================================
   DARK CARDS
   ========================================================= */

.workflow-card {
    background: #171a21;
    border: 1px solid #30343d;
    padding: 22px;
    border-radius: 14px;
    margin: 14px 0;
    color: #ffffff !important;
    box-shadow: 0 4px 18px rgba(0,0,0,0.15);
}

.workflow-card * {
    color: #ffffff !important;
}


.result-card {
    background: #171a21;
    border: 1px solid #30343d;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 12px;
    color: #ffffff !important;
    border-left: 4px solid #ff4b4b;
}

.result-card * {
    color: #ffffff !important;
}


/* =========================================================
   FREE PLAN CARDS
   ========================================================= */

.usage-card {
    background: #171a21;
    border: 1px solid #353943;
    padding: 13px 15px;
    border-radius: 10px;
    margin-bottom: 8px;
    color: #ffffff !important;
    font-size: 14px;
}

.usage-card strong {
    color: #ffffff !important;
}


/* =========================================================
   HERO WORKFLOW
   ========================================================= */

.hero-workflow {
    background: linear-gradient(
        135deg,
        #171a21,
        #20242d
    );
    border: 1px solid #353943;
    border-radius: 16px;
    padding: 24px;
    margin: 18px 0 25px 0;
    text-align: center;
}

.hero-workflow-title {
    font-size: 18px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 18px;
}

.workflow-steps {
    font-size: 16px;
    font-weight: 700;
    color: #ffffff;
    line-height: 2;
}


/* =========================================================
   SECTION LABEL
   ========================================================= */

.section-label {
    background: #171a21;
    border: 1px solid #30343d;
    padding: 12px 15px;
    border-radius: 10px;
    margin: 20px 0 12px 0;
    color: #ffffff !important;
    font-weight: 700;
}


/* =========================================================
   SMALL TEXT
   ========================================================= */

.small-note {
    color: #aeb4c0 !important;
    font-size: 14px;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 768px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: 1rem;
    }

    h1 {
        font-size: 2rem !important;
    }

    h2 {
        font-size: 1.6rem !important;
    }

    h3 {
        font-size: 1.3rem !important;
    }

    .workflow-card {
        padding: 16px;
    }

    .hero-workflow {
        padding: 18px;
    }

    .workflow-steps {
        font-size: 14px;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. BRANDING
# ============================================================

st.title("🚀 Hustle Studio")

st.success(
    "📱 **Hustler Tip:** Tap your browser's 3 dots and choose "
    "**Add to Home Screen** to use Hustle Studio like a phone app."
)

st.markdown(
    "Create better content faster — from idea to ready-to-post video."
)


# ============================================================
# 4. FREE PLAN LIMITS
# ============================================================

FREE_LIMITS = {
    "ideas": 10,
    "hooks": 10,
    "scripts": 5,
    "captions": 3
}


# ============================================================
# 5. SESSION STATE
# ============================================================

if "workspace_data" not in st.session_state:

    st.session_state.workspace_data = {
        "current_topic": "",
        "selected_idea": "",
        "hooks": [],
        "selected_hook": "",
        "script": "",
        "captions": "",
        "processed_video_data": None,

        "free_ideas_left": 10,
        "free_hooks_left": 10,
        "free_scripts_left": 5,
        "free_captions_left": 3,

        "idea_results": []
    }


defaults = {
    "current_topic": "",
    "selected_idea": "",
    "hooks": [],
    "selected_hook": "",
    "script": "",
    "captions": "",
    "processed_video_data": None,

    "free_ideas_left": 10,
    "free_hooks_left": 10,
    "free_scripts_left": 5,
    "free_captions_left": 3,

    "idea_results": []
}


for key, value in defaults.items():

    if key not in st.session_state.workspace_data:
        st.session_state.workspace_data[key] = value


# ============================================================
# 6. USAGE FUNCTIONS
# ============================================================

def usage_available(key):

    return st.session_state.workspace_data[key] > 0


def use_credit(key):

    if st.session_state.workspace_data[key] > 0:

        st.session_state.workspace_data[key] -= 1

        return True

    return False


def upgrade_message(feature):

    st.error(
        f"🔒 Your free {feature} limit has been reached."
    )

    st.info(
        "💰 Upgrade in the Monetization Portal when paid "
        "plans are connected."
    )


# ============================================================
# 7. SIDEBAR
# ============================================================

st.sidebar.title("🚀 Hustle Studio")

st.sidebar.markdown("---")

workspace_selection = st.sidebar.radio(
    "Navigate",
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
    💡 Ideas — <strong>{st.session_state.workspace_data['free_ideas_left']} left</strong>
    </div>

    <div class="usage-card">
    🔥 Hooks — <strong>{st.session_state.workspace_data['free_hooks_left']} left</strong>
    </div>

    <div class="usage-card">
    📝 Scripts — <strong>{st.session_state.workspace_data['free_scripts_left']} left</strong>
    </div>

    <div class="usage-card">
    🎬 Captions — <strong>{st.session_state.workspace_data['free_captions_left']} left</strong>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Free limits are currently session-based."
)


# ============================================================
# 8. STRATEGY STUDIO
# ============================================================

if workspace_selection == "🧠 Strategy Studio":

    st.subheader("🧠 Strategy Studio")

    st.markdown(
        "Your complete creator workflow:"
    )

    # --------------------------------------------------------
    # WORKFLOW CARD
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="hero-workflow">

            <div class="hero-workflow-title">
                🚀 YOUR CREATOR WORKFLOW
            </div>

            <div class="workflow-steps">
                💡 Idea
                &nbsp;→&nbsp;
                🔥 Hook
                &nbsp;→&nbsp;
                📝 Script
                &nbsp;→&nbsp;
                🎬 Caption
                &nbsp;→&nbsp;
                📱 Post
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # NICHE / STYLE
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        niche = st.selectbox(
            "🎯 Video Niche",
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
            "🎭 Delivery Style",
            [
                "Comedic / Local Vibe (Sheng Mix)",
                "Energetic & Fast-Paced",
                "Storytelling & Emotional",
                "Educational & Corporate"
            ]
        )


    # ========================================================
    # STEP 1 — CONTENT IDEA
    # ========================================================

    st.markdown(
        """
        <div class="section-label">
        💡 STEP 1 — FIND YOUR CONTENT IDEA
        </div>
        """,
        unsafe_allow_html=True
    )

    idea_topic = st.text_input(
        "What do you want to create content about?",
        placeholder="Example: Starting a business with KSh 5,000",
        key="idea_topic_input"
    )

    if st.button("💡 Generate 10 Content Ideas"):

        if not idea_topic.strip():

            st.warning(
                "⚠️ Enter a topic first."
            )

        elif not usage_available(
            "free_ideas_left"
        ):

            upgrade_message(
                "content idea generations"
            )

        else:

            use_credit(
                "free_ideas_left"
            )

            clean_topic = idea_topic.strip()

            ideas = [

                f"3 mistakes beginners make with {clean_topic}",

                f"The truth nobody tells you about {clean_topic}",

                f"How I would start {clean_topic} with KSh 5,000",

                f"5 things I wish I knew before starting {clean_topic}",

                f"Stop doing this if you want to succeed with {clean_topic}",

                f"Beginner vs expert: {clean_topic}",

                f"Can you actually make money from {clean_topic}?",

                f"The biggest mistake people make with {clean_topic}",

                f"A day in the life of someone doing {clean_topic}",

                f"What nobody warns you about {clean_topic}"

            ]

            st.session_state.workspace_data[
                "idea_results"
            ] = ideas

            st.success(
                f"🎉 Ideas generated! "
                f"{st.session_state.workspace_data['free_ideas_left']} "
                f"generation(s) remaining."
            )


    # ========================================================
    # DISPLAY IDEAS
    # ========================================================

    if st.session_state.workspace_data["idea_results"]:

        st.markdown("### 🚀 Choose an Idea")

        for index, idea in enumerate(
            st.session_state.workspace_data[
                "idea_results"
            ]
        ):

            st.markdown(
                f"""
                <div class="result-card">
                    <strong>Idea #{index + 1}</strong><br><br>
                    {idea}
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                f"🔥 Use Idea #{index + 1}",
                key=f"use_idea_{index}"
            ):

                st.session_state.workspace_data[
                    "selected_idea"
                ] = idea

                st.session_state.workspace_data[
                    "current_topic"
                ] = idea

                st.success(
                    "✅ Idea selected!"
                )


    # ========================================================
    # SELECTED IDEA
    # ========================================================

    selected_idea = (
        st.session_state.workspace_data[
            "selected_idea"
        ]
    )

    if selected_idea:

        st.markdown("### ✅ Selected Idea")

        st.markdown(
            f"""
            <div class="workflow-card">
                💡 <strong>{selected_idea}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # STEP 2 — HOOKS
    # ========================================================

    st.markdown(
        """
        <div class="section-label">
        🔥 STEP 2 — CREATE YOUR HOOK
        </div>
        """,
        unsafe_allow_html=True
    )

    hook_topic = st.text_input(
        "Topic for your hooks",
        value=st.session_state.workspace_data[
            "current_topic"
        ],
        key="hook_topic_input"
    )

    if st.button("🔥 Generate 5 Viral Hooks"):

        if not hook_topic.strip():

            st.warning(
                "⚠️ Select an idea or enter a topic."
            )

        elif not usage_available(
            "free_hooks_left"
        ):

            upgrade_message(
                "hook generations"
            )

        else:

            use_credit(
                "free_hooks_left"
            )

            clean_topic = hook_topic.strip()

            st.session_state.workspace_data[
                "current_topic"
            ] = clean_topic

            hooks = [

                f"STOP scrolling! Nobody tells you this about {clean_topic}.",

                f"Mbona nobody is talking about {clean_topic}?",

                f"If I had to start {clean_topic} from zero, here's what I'd do.",

                f"Umeanza {clean_topic}? Don't make this mistake.",

                f"The biggest mistake people make with {clean_topic} is this..."

            ]

            st.session_state.workspace_data[
                "hooks"
            ] = hooks

            st.success(
                f"🔥 Hooks generated! "
                f"{st.session_state.workspace_data['free_hooks_left']} "
                f"generation(s) remaining."
            )


    # ========================================================
    # DISPLAY HOOKS
    # ========================================================

    if st.session_state.workspace_data["hooks"]:

        st.markdown("### 🎯 Choose Your Hook")

        for index, hook in enumerate(
            st.session_state.workspace_data[
                "hooks"
            ]
        ):

            st.markdown(
                f"""
                <div class="result-card">
                    <strong>Hook #{index + 1}</strong><br><br>
                    {hook}
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                f"📝 Use Hook #{index + 1}",
                key=f"use_hook_{index}"
            ):

                st.session_state.workspace_data[
                    "selected_hook"
                ] = hook

                st.success(
                    "✅ Hook selected!"
                )


    # ========================================================
    # SELECTED HOOK
    # ========================================================

    selected_hook = (
        st.session_state.workspace_data[
            "selected_hook"
        ]
    )

    if selected_hook:

        st.markdown("### 🔥 Selected Hook")

        st.markdown(
            f"""
            <div class="workflow-card">
                🔥 <strong>{selected_hook}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # STEP 3 — SCRIPT
    # ========================================================

    st.markdown(
        """
        <div class="section-label">
        📝 STEP 3 — BUILD YOUR SCRIPT
        </div>
        """,
        unsafe_allow_html=True
    )

    script_topic = (
        st.session_state.workspace_data[
            "current_topic"
        ]
    )

    script_hook = (
        st.session_state.workspace_data[
            "selected_hook"
        ]
    )

    if not script_hook:

        st.info(
            "👆 Choose a hook above first."
        )


    if st.button(
        "📝 Generate My Script"
    ):

        if not script_hook:

            st.warning(
                "⚠️ Select a hook first."
            )

        elif not usage_available(
            "free_scripts_left"
        ):

            upgrade_message(
                "script generations"
            )

        else:

            use_credit(
                "free_scripts_left"
            )


            # ------------------------------------------------
            # SCRIPT STYLE
            # ------------------------------------------------

            if style == "Comedic / Local Vibe (Sheng Mix)":

                body = (
                    f"Wasee wengi wanaingia kwa "
                    f"{script_topic} wakidhani ni rahisi. "
                    f"Lakini kuna mistake moja ambayo inaweza "
                    f"kupotezea time na pesa."
                )

                cta = (
                    "Follow Hustle Studio for more practical "
                    "Kenyan creator and hustle tips."
                )


            elif style == "Energetic & Fast-Paced":

                body = (
                    f"Here's what you need to know about "
                    f"{script_topic}. First, understand the basics. "
                    f"Second, avoid the common mistakes. "
                    f"Third, stay consistent."
                )

                cta = (
                    "Follow for more quick tips."
                )


            elif style == "Storytelling & Emotional":

                body = (
                    f"When I first started learning about "
                    f"{script_topic}, I quickly realized that "
                    f"most people only show the success. "
                    f"They don't show the mistakes behind it."
                )

                cta = (
                    "Follow to see the real journey."
                )


            else:

                body = (
                    f"When approaching {script_topic}, "
                    f"focus on the fundamentals first. "
                    f"Then build a consistent process "
                    f"that you can repeat."
                )

                cta = (
                    "Follow for more practical strategies."
                )


            script = f"""
## 🚨 HOOK

{script_hook}


## 📦 BODY

{body}


## 🎬 VISUAL INSTRUCTIONS

**Shot 1 — 0-3 seconds**

Look directly at the camera and deliver the hook.


**Shot 2 — 3-15 seconds**

Show yourself explaining the main point.


**Shot 3 — 15-30 seconds**

Show an example, product, location, screen recording,
or demonstration.


**Shot 4 — Final seconds**

Return to the camera and deliver the CTA.


## 🎯 CALL TO ACTION

{cta}


## 🎥 RECORDING TIP

Keep the camera vertical.

Use good lighting.

Remove unnecessary pauses.

Change your visual every few seconds.

Add captions when editing.
"""

            st.session_state.workspace_data[
                "script"
            ] = script

            st.success(
                f"🎉 Script ready! "
                f"{st.session_state.workspace_data['free_scripts_left']} "
                f"generation(s) remaining."
            )


    # ========================================================
    # DISPLAY SCRIPT
    # ========================================================

    if st.session_state.workspace_data["script"]:

        st.markdown("### 🎬 Your Script")

        st.markdown(
            st.session_state.workspace_data[
                "script"
            ]
        )


        # ====================================================
        # STEP 4 — CAPTION
        # ====================================================

        st.markdown(
            """
            <div class="section-label">
            📲 STEP 4 — READY-TO-POST CAPTION
            </div>
            """,
            unsafe_allow_html=True
        )

        current_topic = (
            st.session_state.workspace_data[
                "current_topic"
            ]
        )

        social_caption = f"""
🔥 {current_topic}

Most people don't realize this until it's too late.

Watch till the end and let me know what you think 👇

Follow for more practical content.

#Kenya #KenyanCreators #HustleKE #ContentCreator
"""

        st.session_state.workspace_data[
            "captions"
        ] = social_caption

        st.text_area(
            "Copy this caption:",
            value=social_caption,
            height=180
        )

        st.success(
            "🎉 Your idea is now a complete content package!"
        )

        st.markdown(
            """
            <div class="workflow-card">

            <strong>🚀 WHAT'S NEXT?</strong>

            <br><br>

            1️⃣ Record your video

            <br>

            2️⃣ Open 🎬 Caption King Studio

            <br>

            3️⃣ Upload your video

            <br>

            4️⃣ Add your captions

            <br>

            5️⃣ Download and post 📱

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# 9. CAPTION KING STUDIO
# ============================================================

elif workspace_selection == "🎬 Caption King Studio":

    st.title("🎬 Caption King Studio")

    st.markdown(
        "Turn your recorded video into a captioned short-form video."
    )

    trials_left = (
        st.session_state.workspace_data[
            "free_captions_left"
        ]
    )

    if trials_left > 0:

        st.success(
            f"🎁 You have **{trials_left}** free caption "
            f"export(s) remaining."
        )

    else:

        st.error(
            "🔒 Your free caption exports have been used."
        )

        st.info(
            "Visit the Monetization Portal to view upgrade options."
        )


    uploaded_video = st.file_uploader(
        "Upload your raw MP4 video",
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
            "Accent Color",
            "#FF4B4B"
        )


    if st.button(
        "🎬 Create Captioned Video"
    ):

        if uploaded_video is None:

            st.error(
                "❌ Please upload a video first."
            )

        elif not usage_available(
            "free_captions_left"
        ):

            upgrade_message(
                "caption exports"
            )

        else:

            with st.spinner(
                "🎬 Processing your video..."
            ):

                temp_input_path = None
                temp_silent_path = None
                temp_final_path = None

                try:

                    # ----------------------------------------
                    # SAVE INPUT
                    # ----------------------------------------

                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".mp4"
                    ) as temp_input:

                        temp_input.write(
                            uploaded_video.read()
                        )

                        temp_input_path = (
                            temp_input.name
                        )


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
                    # OUTPUT
                    # ----------------------------------------

                    temp_silent_path = tempfile.mktemp(
                        suffix=".mp4"
                    )

                    fourcc = (
                        cv2.VideoWriter_fourcc(
                            *"mp4v"
                        )
                    )

                    out = cv2.VideoWriter(
                        temp_silent_path,
                        fourcc,
                        fps,
                        (width, height)
                    )


                    # ----------------------------------------
                    # CAPTION TEXT
                    # ----------------------------------------

                    subtitle_text = (
                        st.session_state.workspace_data[
                            "current_topic"
                        ]
                        or "Hustle Studio"
                    )


                    # ----------------------------------------
                    # COLOR
                    # ----------------------------------------

                    hex_color = (
                        accent_color.lstrip("#")
                    )

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

                    if font_style == "Impact Bold":

                        font_face = (
                            cv2.FONT_HERSHEY_TRIPLEX
                        )

                    elif font_style == "Montserrat ExtraBold":

                        font_face = (
                            cv2.FONT_HERSHEY_DUPLEX
                        )

                    else:

                        font_face = (
                            cv2.FONT_HERSHEY_COMPLEX
                        )


                    font_scale = max(
                        1.0,
                        width / 450.0
                    )

                    thickness = max(
                        2,
                        int(font_scale * 2.5)
                    )


                    # ----------------------------------------
                    # FRAME LOOP
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

                    temp_final_path = tempfile.mktemp(
                        suffix=".mp4"
                    )

                    ffmpeg_cmd = [
                        "ffmpeg",
                        "-y",
                        "-i",
                        temp_silent_path,
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
                        temp_final_path
                    ]

                    subprocess.run(
                        ffmpeg_cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=True
                    )


                    # ----------------------------------------
                    # SAVE OUTPUT
                    # ----------------------------------------

                    with open(
                        temp_final_path,
                        "rb"
                    ) as video_file:

                        st.session_state.workspace_data[
                            "processed_video_data"
                        ] = video_file.read()


                    use_credit(
                        "free_captions_left"
                    )


                    st.success(
                        "🎉 Your captioned video is ready!"
                    )

                    st.rerun()


                except Exception as error:

                    st.error(
                        f"❌ Video processing error: {error}"
                    )


                finally:

                    for temp_path in [
                        temp_input_path,
                        temp_silent_path,
                        temp_final_path
                    ]:

                        if (
                            temp_path
                            and os.path.exists(
                                temp_path
                            )
                        ):

                            try:

                                os.unlink(
                                    temp_path
                                )

                            except Exception:

                                pass


    # ========================================================
    # VIDEO OUTPUT
    # ========================================================

    if (
        st.session_state.workspace_data[
            "processed_video_data"
        ] is not None
    ):

        st.markdown("---")

        st.subheader("🎉 Your Finished Video")

        st.video(
            st.session_state.workspace_data[
                "processed_video_data"
            ]
        )

        st.download_button(
            label="📥 Download Captioned Video",
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
        "Choose the plan that matches your creator workflow."
    )


    # ========================================================
    # FREE PLAN
    # ========================================================

    st.subheader("🆓 Free Creator")

    st.markdown(
        """
        <div class="workflow-card">

        <h3>🆓 Free Creator</h3>

        <p>
        Try the complete Hustle Studio workflow.
        </p>

        <ul>
            <li>10 content idea generations</li>
            <li>10 hook generations</li>
            <li>5 script generations</li>
            <li>3 caption exports</li>
            <li>Mobile-friendly workflow</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown("---")


    # ========================================================
    # WEEKLY PLAN
    # ========================================================

    st.subheader("🚀 Hustler Weekly")

    st.markdown(
        """
        <div class="workflow-card">

        <h3>🚀 Hustler Weekly</h3>

        <h2>KSh 150</h2>

        <p>
        7 days of higher creator limits.
        </p>

        <ul>
            <li>More content ideas</li>
            <li>More hooks</li>
            <li>More scripts</li>
            <li>More caption exports</li>
            <li>Full creator workflow</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )


    if st.button(
        "🚀 Unlock Weekly Plan",
        key="weekly_payment"
    ):

        st.info(
            "📲 M-Pesa payment integration will be added "
            "during the monetization stage."
        )


    st.markdown("---")


    # ========================================================
    # PRO PLAN
    # ========================================================

    st.subheader("🏆 Creator Pro")

    st.markdown(
        """
        <div class="workflow-card">

        <h3>🏆 Creator Pro</h3>

        <h2>KSh 500 / month</h2>

        <p>
        For serious creators.
        </p>

        <ul>
            <li>High AI limits</li>
            <li>More video exports</li>
            <li>Advanced creator tools</li>
            <li>Priority processing</li>
            <li>Future creator analytics</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )


    if st.button(
        "🏆 Unlock Creator Pro",
        key="pro_payment"
    ):

        st.info(
            "📲 M-Pesa subscription integration will be "
            "added during the monetization stage."
        )


# ============================================================
# 11. FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🚀 Hustle Studio — Idea → Hook → Script → Caption → Post"
)
