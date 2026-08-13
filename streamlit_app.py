


import streamlit as st
import os
import tempfile
import subprocess
import cv2
import numpy as np

st.set_page_config(page_title="Hustle Studio", page_icon="🚀", layout="wide")

# ============================================================
# UI / CSS
# ============================================================
st.markdown("""
<style>
.block-container { max-width: 1100px; padding-top: 2rem; padding-bottom: 4rem; }
div.stButton > button:first-child { width: 100%; min-height: 48px; padding: 12px 16px !important; font-size: 16px !important; font-weight: 700 !important; border-radius: 10px !important; }
div[data-baseweb="select"] { margin-bottom: 8px; }
div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea { border-radius: 10px !important; }
.workflow-card, .result-card, .usage-card, .section-label { color: #ffffff !important; background: #171a21; border: 1px solid #30343d; }
.workflow-card { padding: 22px; border-radius: 14px; margin: 14px 0; }
.workflow-card * { color: #ffffff !important; }
.result-card { padding: 18px; border-radius: 12px; margin-bottom: 12px; border-left: 4px solid #ff4b4b; }
.result-card * { color: #ffffff !important; }
.usage-card { padding: 13px 15px; border-radius: 10px; margin-bottom: 8px; font-size: 14px; }
.usage-card strong { color: #ffffff !important; }
.hero-workflow { background: linear-gradient(135deg, #171a21, #20242d); border: 1px solid #353943; border-radius: 16px; padding: 24px; margin: 18px 0 25px; text-align: center; color: #ffffff !important; }
.hero-workflow-title { font-size: 18px; font-weight: 800; color: #ffffff !important; margin-bottom: 18px; }
.workflow-steps { font-size: 16px; font-weight: 700; color: #ffffff !important; line-height: 2; }
.section-label { padding: 12px 15px; border-radius: 10px; margin: 20px 0 12px; font-weight: 700; }
@media (max-width: 768px) { .block-container { padding-left: 1rem; padding-right: 1rem; padding-top: 1rem; } .workflow-card { padding: 16px; } .hero-workflow { padding: 18px; } .workflow-steps { font-size: 14px; } }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Hustle Studio")
st.success("📱 **Hustler Tip:** Tap your browser's 3 dots and choose **Add to Home Screen** to use Hustle Studio like a phone app.")
st.markdown("Create better content faster — from idea to ready-to-post video.")

# ============================================================
# SESSION STATE / FREE LIMITS
# ============================================================
if "hs" not in st.session_state:
    st.session_state.hs = {
        "current_topic": "", "selected_idea": "", "idea_results": [],
        "hooks": [], "selected_hook": "", "script": "", "caption": "",
        "processed_video": None, "ideas_left": 10, "hooks_left": 10,
        "scripts_left": 5, "captions_left": 3
    }
hs = st.session_state.hs

def has_credit(key):
    return hs[key] > 0

def use_credit(key):
    if hs[key] > 0:
        hs[key] -= 1
        return True
    return False

def limit_message(name):
    st.error(f"🔒 Your free {name} limit has been reached.")
    st.info("💰 Paid plans can be connected to the Monetization Portal later.")

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.title("🚀 Hustle Studio")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigate", ["🧠 Strategy Studio", "🎬 Caption King Studio", "👤 Monetization Portal"])
st.sidebar.markdown("---")
st.sidebar.markdown("### 🆓 Free Plan")
st.sidebar.markdown(f"""
<div class="usage-card">💡 Ideas — <strong>{hs['ideas_left']} left</strong></div>
<div class="usage-card">🔥 Hooks — <strong>{hs['hooks_left']} left</strong></div>
<div class="usage-card">📝 Scripts — <strong>{hs['scripts_left']} left</strong></div>
<div class="usage-card">🎬 Captions — <strong>{hs['captions_left']} left</strong></div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.caption("Creator Content Packs use 1 script credit. Free limits are session-based in this version.")

# ============================================================
# VIRAL ANALYZER
# ============================================================
if page == "🔥 Viral Analyzer":

    st.title("🔥 Viral Analyzer")
    st.write(
        "Score your idea, hook, caption, or script before you post it."
    )

    st.markdown("""
<div class="hero-workflow">
    <div class="hero-workflow-title">📈 TEST YOUR CONTENT BEFORE POSTING</div>
    <div class="workflow-steps">
        🎯 Hook → 👀 Curiosity → ❤️ Emotion → 🇰🇪 Relevance → ⏱️ Retention → 🚀 Viral Score
    </div>
</div>
""", unsafe_allow_html=True)

    analyzer_text = st.text_area(
        "📝 Paste your video idea, hook, caption, or script",
        placeholder=(
            "Example: I started selling shoes with KSh 3,000. "
            "Here's what nobody warned me about..."
        ),
        height=180,
        key="analyzer_text"
    )

    col1, col2 = st.columns(2)

    with col1:
        analyzer_platform = st.selectbox(
            "📱 Platform",
            ["TikTok", "Instagram Reels", "YouTube Shorts"],
            key="analyzer_platform"
        )

    with col2:
        analyzer_audience = st.selectbox(
            "🎯 Audience",
            [
                "Kenyan Audience",
                "African Audience",
                "Global Audience",
                "Business / Hustle Audience",
                "Young Creators"
            ],
            key="analyzer_audience"
        )

    if st.button("🔥 Analyze My Content", key="analyze_content"):

        if not analyzer_text.strip():
            st.warning("⚠️ Paste something to analyze first.")

        else:
            text = analyzer_text.strip()
            lower = text.lower()

            # Simple rule-based analysis keeps this version usable
            # without requiring another API key.
            hook_points = 5

            curiosity_words = [
                "secret", "nobody", "mistake", "truth", "warning",
                "why", "how", "before", "never", "hidden", "actually",
                "don't", "didn't", "what"
            ]

            emotion_words = [
                "money", "fear", "mistake", "success", "failure",
                "dream", "shocking", "love", "hate", "struggle",
                "loss", "win", "secret", "warning"
            ]

            local_words = [
                "kenya", "kenyan", "nairobi", "m-pesa", "mpesa",
                "ksh", "shilling", "sheng", "matatu", "mombasa",
                "kisumu", "eldoret", "hustle"
            ]

            curiosity_hits = sum(
                1 for word in curiosity_words if word in lower
            )
            emotion_hits = sum(
                1 for word in emotion_words if word in lower
            )
            local_hits = sum(
                1 for word in local_words if word in lower
            )

            word_count = len(text.split())

            if len(text) <= 80:
                curiosity_score = 8
            elif len(text) <= 160:
                curiosity_score = 7
            else:
                curiosity_score = 5

            curiosity_score = min(
                10,
                curiosity_score + min(2, curiosity_hits)
            )

            emotion_score = min(
                10,
                5 + min(5, emotion_hits)
            )

            relevance_score = 6

            if analyzer_audience == "Kenyan Audience":
                relevance_score = min(
                    10,
                    7 + min(3, local_hits)
                )
            elif analyzer_audience == "African Audience":
                relevance_score = min(
                    10,
                    6 + min(4, local_hits)
                )
            else:
                relevance_score = 7

            retention_score = 7

            if "3 " in lower or "3 things" in lower:
                retention_score += 1
            if "step" in lower or "steps" in lower:
                retention_score += 1
            if "first" in lower or "then" in lower:
                retention_score += 1

            retention_score = min(10, retention_score)

            hook_score = 6

            strong_openers = [
                "stop", "wait", "nobody", "here's", "this is",
                "i started", "if you're", "before you", "don't"
            ]

            if any(opener in lower for opener in strong_openers):
                hook_score += 2

            if "?" in text:
                hook_score += 1

            if "!" in text:
                hook_score += 1

            hook_score = min(10, hook_score)

            viral_score = round(
                (
                    hook_score
                    + curiosity_score
                    + emotion_score
                    + relevance_score
                    + retention_score
                ) / 5,
                1
            )

            if viral_score >= 8.5:
                rating = "🔥 VERY STRONG"
                rating_message = "This has strong short-form potential."
            elif viral_score >= 7:
                rating = "🚀 GOOD POTENTIAL"
                rating_message = "The idea is solid, but the opening can be stronger."
            elif viral_score >= 5.5:
                rating = "⚠️ NEEDS WORK"
                rating_message = "There is a usable idea here, but the packaging needs improvement."
            else:
                rating = "🔧 WEAK"
                rating_message = "Rework the hook and make the value clearer."

            weaknesses = []

            if hook_score < 8:
                weaknesses.append(
                    "Your opening is not strong enough to stop scrolling."
                )

            if curiosity_score < 8:
                weaknesses.append(
                    "Add a curiosity gap, specific result, mistake, or unexpected claim."
                )

            if emotion_score < 7:
                weaknesses.append(
                    "Give the viewer a stronger reason to care emotionally."
                )

            if relevance_score < 8:
                weaknesses.append(
                    "Make the example more specific to your target audience."
                )

            if retention_score < 8:
                weaknesses.append(
                    "Break the content into quick steps, examples, or visual changes."
                )

            if word_count > 100:
                weaknesses.append(
                    "The text is long. Make the first section faster and more direct."
                )

            if not weaknesses:
                weaknesses.append(
                    "No major weakness detected. Test multiple versions and compare results."
                )

            # Generate an improved hook without pretending it came from live trends.
            topic_hint = text.split(".")[0].strip()

            if "ksh" in lower or "kenya" in lower or "kenyan" in lower:
                improved_hook = (
                    f"🇰🇪 I tried {topic_hint.lower()} — here's the mistake "
                    "I wish someone warned me about."
                )
            elif "how" in lower:
                improved_hook = (
                    f"STOP scrolling — here's the part about {topic_hint.lower()} "
                    "that most beginners get wrong."
                )
            else:
                improved_hook = (
                    f"Nobody tells you this about {topic_hint.lower()} — "
                    "but it can save you time and money."
                )

            hs["analysis"] = {
                "score": viral_score,
                "rating": rating,
                "message": rating_message,
                "hook": hook_score,
                "curiosity": curiosity_score,
                "emotion": emotion_score,
                "relevance": relevance_score,
                "retention": retention_score,
                "weaknesses": weaknesses,
                "improved_hook": improved_hook,
                "platform": analyzer_platform
            }

            st.success("🎉 Analysis complete!")

    if "analysis" in hs and hs["analysis"]:

        result = hs["analysis"]

        st.markdown("### 🚀 Overall Viral Score")

        score_col1, score_col2 = st.columns(2)

        with score_col1:
            st.metric(
                "Viral Potential",
                f"{result['score']}/10"
            )

        with score_col2:
            st.metric(
                "Rating",
                result["rating"]
            )

        st.info(result["message"])

        st.markdown("### 📊 Content Scorecard")

        score_items = [
            ("🎯 Hook Strength", result["hook"]),
            ("👀 Curiosity", result["curiosity"]),
            ("❤️ Emotional Pull", result["emotion"]),
            ("🇰🇪 Audience Relevance", result["relevance"]),
            ("⏱️ Retention Potential", result["retention"])
        ]

        for label, score in score_items:
            st.markdown(f"**{label} — {score}/10**")
            st.progress(score / 10)

        st.markdown("### ⚠️ What You Should Improve")

        for weakness in result["weaknesses"]:
            st.markdown(f"• {weakness}")

        st.markdown("### 🔥 Improved Hook")

        st.markdown(
            f"""
<div class="result-card">
    <strong>🚀 Try this:</strong><br><br>
    {result["improved_hook"]}
</div>
""",
            unsafe_allow_html=True
        )

        st.caption(
            f"Analyzed for {result['platform']}. "
            "This score is a content-quality estimate, not a guarantee of views."
        )


# ============================================================
# CREATOR CONTENT PACK
# ============================================================
if page == "🚀 Creator Content Pack":


    st.title("🚀 Creator Content Pack")
    st.write("One topic → a complete ready-to-post content package.")

    st.markdown("""
<div class="hero-workflow">
    <div class="hero-workflow-title">⚡ ONE TOPIC → COMPLETE CONTENT</div>
    <div class="workflow-steps">
        💡 Idea → 🔥 Hooks → 📝 Script → 📲 Caption → #️⃣ Hashtags → 🎯 CTA
    </div>
</div>
""", unsafe_allow_html=True)

    topic = st.text_input(
        "🎯 What is your video about?",
        placeholder="Example: How to start a small business with KSh 5,000",
        key="pack_topic"
    )

    col1, col2 = st.columns(2)

    with col1:
        niche = st.selectbox(
            "📌 Niche",
            [
                "Business & Hustle",
                "Food & Cooking",
                "Fashion & Beauty",
                "Football & Sports",
                "Tech",
                "Motivation",
                "Lifestyle",
                "Comedy"
            ],
            key="pack_niche"
        )

    with col2:
        style = st.selectbox(
            "🎭 Style",
            [
                "Energetic",
                "Comedic / Sheng",
                "Storytelling",
                "Educational"
            ],
            key="pack_style"
        )

    if st.button("🚀 Generate Complete Content Pack", key="generate_pack"):

        if not topic.strip():
            st.warning("⚠️ Enter a topic first.")

        elif not has_credit("scripts_left"):
            limit_message("content pack generations")

        else:
            use_credit("scripts_left")

            topic_clean = topic.strip()

            if style == "Comedic / Sheng":
                hooks = [
                    f"Wasee, mbona nobody anawaambia hii kuhusu {topic_clean}?",
                    f"Ukiendelea kufanya hivi na {topic_clean}, utajipata kwa shida 😂",
                    f"Nilijifunza hii kuhusu {topic_clean} the hard way...",
                    f"Si kila mtu anakuambia ukweli kuhusu {topic_clean}.",
                    f"Kama unaanza {topic_clean}, WATCH THIS kwanza."
                ]
                body = (
                    f"Let's be honest — {topic_clean} sounds simple until you "
                    f"actually try it. The biggest mistake is starting without "
                    f"a clear plan. Start small, test what works, then improve."
                )
                cta = "Follow for more practical Kenyan creator and hustle tips."

            elif style == "Storytelling":
                hooks = [
                    f"I wish someone had told me this about {topic_clean}.",
                    f"This changed the way I think about {topic_clean}.",
                    f"Nobody prepared me for this part of {topic_clean}.",
                    f"Here's what I learned after getting {topic_clean} wrong.",
                    f"If I could start {topic_clean} again, I'd do this first."
                ]
                body = (
                    f"Most people only show the result. What they don't show "
                    f"is the learning process behind {topic_clean}. Start with "
                    f"one simple step, learn from the result, and keep improving."
                )
                cta = "Follow to see more real lessons and practical strategies."

            elif style == "Educational":
                hooks = [
                    f"3 things you need to know about {topic_clean}.",
                    f"Here's the simplest way to understand {topic_clean}.",
                    f"Before you start {topic_clean}, know these 3 things.",
                    f"The biggest mistake beginners make with {topic_clean}.",
                    f"Let me explain {topic_clean} in 30 seconds."
                ]
                body = (
                    f"First, understand the basics of {topic_clean}. Second, "
                    f"avoid trying to do everything at once. Third, measure "
                    f"what works and repeat it consistently."
                )
                cta = "Save this video and follow for more simple explanations."

            else:
                hooks = [
                    f"STOP scrolling! You need to know this about {topic_clean}.",
                    f"Here's what nobody tells you about {topic_clean}.",
                    f"If you're doing {topic_clean}, don't make this mistake.",
                    f"Want better results with {topic_clean}? Start here.",
                    f"This one change can improve your approach to {topic_clean}."
                ]
                body = (
                    f"If you're serious about {topic_clean}, don't overcomplicate "
                    f"it. Focus on one clear goal, create useful content, and "
                    f"stay consistent long enough to learn what your audience wants."
                )
                cta = "Follow for more useful content and practical tips."

            best_hook = hooks[0]

            script = f"""HOOK:
{best_hook}

BODY:
{body}

VISUAL PLAN:
1. Start with a close-up talking to camera.
2. Show a quick example, product, screen recording, or demonstration.
3. Add 2–3 quick visual changes while explaining the main point.
4. End by looking directly at the camera for the CTA.

CTA:
{cta}
"""

            hashtags = (
                "#Kenya #KenyanCreators #ContentCreator #HustleKE "
                "#TikTokKenya #InstagramReels #YouTubeShorts "
                f"#{niche.replace(' ', '').replace('&', '')}"
            )

            hs["pack"] = {
                "topic": topic_clean,
                "hooks": hooks,
                "script": script,
                "caption": (
                    f"🔥 {topic_clean}\n\n"
                    f"Most people overlook this. Here's what you need to know. "
                    f"Save this for later and share it with someone who needs it.\n\n"
                    f"{cta}"
                ),
                "hashtags": hashtags,
                "cta": cta
            }

            st.success("🎉 Your complete content pack is ready!")

    if "pack" in hs and hs["pack"]:

        pack = hs["pack"]

        st.markdown("### 💡 Your Content Idea")
        st.markdown(
            f"""
<div class="workflow-card">
    <strong>{pack["topic"]}</strong>
</div>
""",
            unsafe_allow_html=True
        )

        st.markdown("### 🔥 5 Viral Hooks")

        for i, hook in enumerate(pack["hooks"], 1):
            st.markdown(
                f"""
<div class="result-card">
    <strong>Hook {i}</strong><br><br>{hook}
</div>
""",
                unsafe_allow_html=True
            )

        st.markdown("### 📝 Ready-to-Record Script")
        st.text_area(
            "Script",
            value=pack["script"],
            height=300,
            key="pack_script_display"
        )

        st.markdown("### 📲 Ready-to-Post Caption")
        st.text_area(
            "Caption",
            value=pack["caption"],
            height=160,
            key="pack_caption_display"
        )

        st.markdown("### #️⃣ Hashtags")
        st.code(pack["hashtags"])

        st.markdown("### 🎯 Call To Action")
        st.markdown(
            f"""
<div class="workflow-card">
    🎯 {pack["cta"]}
</div>
""",
            unsafe_allow_html=True
        )

        download_text = (
            "HUSTLE STUDIO — CREATOR CONTENT PACK\n\n"
            f"TOPIC:\n{pack['topic']}\n\n"
            "HOOKS:\n"
            + "\n".join(
                f"{i}. {hook}" for i, hook in enumerate(pack["hooks"], 1)
            )
            + f"\n\nSCRIPT:\n{pack['script']}"
            + f"\nCAPTION:\n{pack['caption']}"
            + f"\n\nHASHTAGS:\n{pack['hashtags']}"
            + f"\n\nCTA:\n{pack['cta']}"
        )

        st.download_button(
            "📥 Download Content Pack",
            data=download_text,
            file_name="hustlestudio_content_pack.txt",
            mime="text/plain",
            key="download_pack"
        )


# ============================================================
# AI SUBTITLES
# ============================================================
if page == "🎙️ AI Subtitles":

    st.title("🎙️ AI Subtitles")
    st.write(
        "Upload a video and automatically turn spoken words into burned-in captions."
    )

    st.markdown("""
<div class="hero-workflow">
    <div class="hero-workflow-title">🎬 VIDEO → AI TRANSCRIPT → CAPTIONS</div>
    <div class="workflow-steps">
        📤 Upload → 🎙️ Transcribe → ✨ Style → 🎬 Burn In → 📥 Download
    </div>
</div>
""", unsafe_allow_html=True)

    st.success(
        "🆓 **Free transcription:** Hustle Studio uses the open-source "
        "Whisper model locally for subtitles. No OpenAI API key is required."
    )

    st.caption(
        "The first transcription may take longer because the Whisper model "
        "needs to download and load on the server."
    )

    subtitle_video = st.file_uploader(
        "📤 Upload your video",
        type=["mp4", "mov", "m4v"],
        help="MP4 is recommended for the best compatibility."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        subtitle_size = st.select_slider(
            "🔤 Caption Size",
            options=["Small", "Medium", "Large"],
            value="Medium",
            key="subtitle_size"
        )

    with col2:
        subtitle_position = st.selectbox(
            "📍 Position",
            ["Bottom", "Center", "Top"],
            key="subtitle_position"
        )

    with col3:
        subtitle_color = st.color_picker(
            "🎨 Caption Color",
            "#FFFFFF",
            key="subtitle_color"
        )

    st.caption(
        "Whisper runs locally on the app server. No OpenAI transcription API call is required."
    )

    if st.button("🎙️ Generate AI Subtitles", key="generate_ai_subtitles"):

        if subtitle_video is None:
            st.error("❌ Please upload a video first.")

        elif not has_credit("captions_left"):
            limit_message("caption exports")

        else:

            input_path = None
            audio_path = None
            output_path = None
            ass_path = None

            try:

                with st.spinner(
                    "🎙️ Loading Whisper and transcribing your video..."
                ):

                    # Import only when the feature is used so the rest of
                    # Hustle Studio can start normally.
                    from faster_whisper import WhisperModel

                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".mp4"
                    ) as temp_input:
                        temp_input.write(subtitle_video.read())
                        input_path = temp_input.name

                    audio_path = tempfile.mktemp(suffix=".wav")

                    extract_audio_cmd = [
                        "ffmpeg",
                        "-y",
                        "-i", input_path,
                        "-vn",
                        "-ac", "1",
                        "-ar", "16000",
                        "-c:a", "pcm_s16le",
                        audio_path
                    ]

                    subprocess.run(
                        extract_audio_cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=True
                    )

                    # CPU + int8 keeps the free/local version much lighter.
                    # The model is cached by faster-whisper after first use.
                    model = WhisperModel(
                        "tiny",
                        device="cpu",
                        compute_type="int8"
                    )

                    segments, info = model.transcribe(
                        audio_path,
                        beam_size=1,
                        vad_filter=True,
                        condition_on_previous_text=False
                    )

                    segment_list = list(segments)

                    if not segment_list:
                        raise RuntimeError(
                            "No speech was detected in the video."
                        )

                    def srt_timestamp(seconds):
                        seconds = max(0.0, float(seconds or 0.0))
                        total_ms = int(round(seconds * 1000))

                        hours = total_ms // 3600000
                        total_ms %= 3600000
                        minutes = total_ms // 60000
                        total_ms %= 60000
                        secs = total_ms // 1000
                        millis = total_ms % 1000

                        return (
                            f"{hours:02d}:{minutes:02d}:{secs:02d},"
                            f"{millis:03d}"
                        )

                    transcript_lines = []
                    srt_lines = []

                    for index, segment in enumerate(segment_list, start=1):

                        text = str(segment.text).strip()

                        if not text:
                            continue

                        start_time = float(segment.start)
                        end_time = float(segment.end)

                        transcript_lines.append(text)

                        srt_lines.extend([
                            str(index),
                            (
                                f"{srt_timestamp(start_time)} --> "
                                f"{srt_timestamp(end_time)}"
                            ),
                            text,
                            ""
                        ])

                    if not transcript_lines:
                        raise RuntimeError(
                            "Whisper did not return readable speech."
                        )

                    with tempfile.NamedTemporaryFile(
                        mode="w",
                        delete=False,
                        suffix=".srt",
                        encoding="utf-8"
                    ) as srt_file:
                        srt_file.write("\n".join(srt_lines))
                        srt_path = srt_file.name

                    hs["subtitle_transcript"] = "\n".join(
                        transcript_lines
                    )

                with st.spinner("🎬 Styling and burning captions..."):

                    clean_color = subtitle_color.lstrip("#")

                    if len(clean_color) != 6:
                        clean_color = "FFFFFF"

                    rr = clean_color[0:2]
                    gg = clean_color[2:4]
                    bb = clean_color[4:6]

                    ass_color = f"&H00{bb}{gg}{rr}"

                    size_map = {
                        "Small": 34,
                        "Medium": 44,
                        "Large": 56
                    }

                    font_size = size_map.get(
                        subtitle_size,
                        44
                    )

                    alignment_map = {
                        "Bottom": 2,
                        "Center": 5,
                        "Top": 8
                    }

                    alignment = alignment_map.get(
                        subtitle_position,
                        2
                    )

                    ass_path = tempfile.mktemp(suffix=".ass")

                    ass_content = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: HustleStudio,Arial,{font_size},{ass_color},&H00000000,&H00000000,&H99000000,1,0,0,0,100,100,0,0,1,3,1,{alignment},80,80,55,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

                    def ass_timestamp(seconds):
                        seconds = max(0.0, float(seconds or 0.0))

                        hours = int(seconds // 3600)
                        minutes = int((seconds % 3600) // 60)
                        secs = int(seconds % 60)
                        centiseconds = int(
                            round((seconds - int(seconds)) * 100)
                        )

                        if centiseconds >= 100:
                            secs += 1
                            centiseconds = 0

                        return (
                            f"{hours}:{minutes:02d}:{secs:02d}."
                            f"{centiseconds:02d}"
                        )

                    event_lines = []

                    for segment in segment_list:

                        text = str(segment.text).strip()

                        if not text:
                            continue

                        safe_text = (
                            text
                            .replace("\\", r"\\")
                            .replace("{", r"\{")
                            .replace("}", r"\}")
                            .replace("\n", r"\N")
                        )

                        event_lines.append(
                            "Dialogue: 0,"
                            f"{ass_timestamp(segment.start)},"
                            f"{ass_timestamp(segment.end)},"
                            f"HustleStudio,,0,0,0,,{safe_text}"
                        )

                    ass_content += "\n".join(event_lines)

                    with open(
                        ass_path,
                        "w",
                        encoding="utf-8"
                    ) as ass_file:
                        ass_file.write(ass_content)

                    output_path = tempfile.mktemp(suffix=".mp4")

                    # Use a simple FFmpeg filter path. Forward slashes are
                    # required inside the filter expression on Windows.
                    ass_filter_path = ass_path.replace("\\", "/").replace(":", r"\:")

                    burn_cmd = [
                        "ffmpeg",
                        "-y",
                        "-i", input_path,
                        "-vf", f"ass='{ass_filter_path}'",
                        "-map", "0:v:0",
                        "-map", "0:a:0?",
                        "-c:v", "libx264",
                        "-preset", "veryfast",
                        "-crf", "23",
                        "-pix_fmt", "yuv420p",
                        "-c:a", "aac",
                        "-b:a", "128k",
                        "-movflags", "+faststart",
                        "-shortest",
                        output_path
                    ]

                    subprocess.run(
                        burn_cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=True
                    )

                    with open(output_path, "rb") as finished_video:
                        hs["subtitle_video"] = finished_video.read()

                    use_credit("captions_left")

                st.success(
                    "🎉 AI subtitles are ready — and this version did not "
                    "use your OpenAI API key!"
                )

            except ImportError:
                st.error(
                    "❌ faster-whisper is not installed. "
                    "Add it to requirements.txt and redeploy."
                )

            except FileNotFoundError:
                st.error(
                    "❌ FFmpeg is not available in this Streamlit environment."
                )

            except subprocess.CalledProcessError:
                st.error(
                    "❌ FFmpeg could not process this video. "
                    "Try a standard MP4 file."
                )

            except Exception as error:
                st.error(
                    f"❌ Subtitle generation failed: {error}"
                )

            finally:

                for path in [
                    input_path,
                    audio_path,
                    output_path,
                    ass_path,
                    locals().get("srt_path")
                ]:

                    if path and os.path.exists(path):

                        try:
                            os.unlink(path)
                        except Exception:
                            pass


    if hs.get("subtitle_video"):

        st.markdown("---")
        st.subheader("🎉 Finished Video")

        st.video(hs["subtitle_video"])

        st.download_button(
            "📥 Download Captioned Video",
            data=hs["subtitle_video"],
            file_name="hustlestudio_ai_subtitles.mp4",
            mime="video/mp4",
            key="download_ai_subtitles"
        )

        if hs.get("subtitle_transcript"):

            with st.expander("📝 View Transcript"):

                st.text_area(
                    "Transcript",
                    value=hs["subtitle_transcript"],
                    height=220,
                    key="subtitle_transcript_display"
                )


# ============================================================
# STRATEGY STUDIO
# ============================================================
if page == "🧠 Strategy Studio":


    st.subheader("🧠 Strategy Studio")
    st.write("Your complete creator workflow:")
    st.markdown("""
<div class="hero-workflow">
    <div class="hero-workflow-title">🚀 YOUR CREATOR WORKFLOW</div>
    <div class="workflow-steps">💡 Idea &nbsp;→&nbsp; 🔥 Hook &nbsp;→&nbsp; 📝 Script &nbsp;→&nbsp; 🎬 Caption &nbsp;→&nbsp; 📱 Post</div>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        niche = st.selectbox("🎯 Video Niche", ["General Hustle & Business", "Fashion & Thrift", "Real Estate & Housing", "Food & Cooking", "Tech & Gadget Reviews", "Football & Sports", "Beauty & Lifestyle", "Motivation & Personal Growth"])
    with col2:
        style = st.selectbox("🎭 Delivery Style", ["Comedic / Local Vibe (Sheng Mix)", "Energetic & Fast-Paced", "Storytelling & Emotional", "Educational & Corporate"])

    st.markdown('<div class="section-label">💡 STEP 1 — FIND YOUR CONTENT IDEA</div>', unsafe_allow_html=True)
    idea_topic = st.text_input("What do you want to create content about?", placeholder="Example: Starting a business with KSh 5,000")
    if st.button("💡 Generate 10 Content Ideas", key="generate_ideas"):
        if not idea_topic.strip():
            st.warning("⚠️ Enter a topic first.")
        elif not has_credit("ideas_left"):
            limit_message("content idea generations")
        else:
            use_credit("ideas_left")
            topic = idea_topic.strip()
            hs["current_topic"] = topic
            hs["idea_results"] = [
                f"3 mistakes beginners make with {topic}", f"The truth nobody tells you about {topic}",
                f"How I would start {topic} with KSh 5,000", f"5 things I wish I knew before starting {topic}",
                f"Stop doing this if you want to succeed with {topic}", f"Beginner vs expert: {topic}",
                f"Can you actually make money from {topic}?", f"The biggest mistake people make with {topic}",
                f"A day in the life of someone doing {topic}", f"What nobody warns you about {topic}"
            ]
            st.success(f"🎉 Ideas generated! {hs['ideas_left']} generation(s) remaining.")

    if hs["idea_results"]:
        st.markdown("### 🚀 Choose an Idea")
        for i, idea in enumerate(hs["idea_results"]):
            st.markdown(f'<div class="result-card"><strong>Idea #{i + 1}</strong><br><br>{idea}</div>', unsafe_allow_html=True)
            if st.button(f"🔥 Use Idea #{i + 1}", key=f"use_idea_{i}"):
                hs["selected_idea"] = idea
                hs["current_topic"] = idea
                st.success("✅ Idea selected!")

    if hs["selected_idea"]:
        st.markdown("### ✅ Selected Idea")
        st.markdown(f'<div class="workflow-card">💡 <strong>{hs["selected_idea"]}</strong></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">🔥 STEP 2 — CREATE YOUR HOOK</div>', unsafe_allow_html=True)
    hook_topic = st.text_input("Topic for your hooks", value=hs["current_topic"], key="hook_topic")
    if st.button("🔥 Generate 5 Viral Hooks", key="generate_hooks"):
        if not hook_topic.strip():
            st.warning("⚠️ Select an idea or enter a topic.")
        elif not has_credit("hooks_left"):
            limit_message("hook generations")
        else:
            use_credit("hooks_left")
            topic = hook_topic.strip()
            hs["current_topic"] = topic
            hs["hooks"] = [
                f"STOP scrolling! Nobody tells you this about {topic}.",
                f"Mbona nobody is talking about {topic}?",
                f"If I had to start {topic} from zero, here's what I'd do.",
                f"Umeanza {topic}? Don't make this mistake.",
                f"The biggest mistake people make with {topic} is this..."
            ]
            st.success(f"🔥 Hooks generated! {hs['hooks_left']} generation(s) remaining.")

    if hs["hooks"]:
        st.markdown("### 🎯 Choose Your Hook")
        for i, hook in enumerate(hs["hooks"]):
            st.markdown(f'<div class="result-card"><strong>Hook #{i + 1}</strong><br><br>{hook}</div>', unsafe_allow_html=True)
            if st.button(f"📝 Use Hook #{i + 1}", key=f"use_hook_{i}"):
                hs["selected_hook"] = hook
                st.success("✅ Hook selected!")

    if hs["selected_hook"]:
        st.markdown("### 🔥 Selected Hook")
        st.markdown(f'<div class="workflow-card">🔥 <strong>{hs["selected_hook"]}</strong></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">📝 STEP 3 — BUILD YOUR SCRIPT</div>', unsafe_allow_html=True)
    if not hs["selected_hook"]:
        st.info("👆 Choose a hook above first.")
    if st.button("📝 Generate My Script", key="generate_script"):
        if not hs["selected_hook"]:
            st.warning("⚠️ Select a hook first.")
        elif not has_credit("scripts_left"):
            limit_message("script generations")
        else:
            use_credit("scripts_left")
            topic = hs["current_topic"]
            hook = hs["selected_hook"]
            if style == "Comedic / Local Vibe (Sheng Mix)":
                body = f"Wasee wengi wanaingia kwa {topic} wakidhani ni rahisi. Lakini kuna mistake moja ambayo inaweza kupotezea time na pesa."
                cta = "Follow for more practical Kenyan creator and hustle tips."
            elif style == "Energetic & Fast-Paced":
                body = f"Here's what you need to know about {topic}. Understand the basics, avoid common mistakes, and stay consistent."
                cta = "Follow for more quick tips."
            elif style == "Storytelling & Emotional":
                body = f"When I first started learning about {topic}, I realized most people only show the success. They don't show the mistakes."
                cta = "Follow to see the real journey."
            else:
                body = f"When approaching {topic}, focus on the fundamentals first. Then build a consistent process you can repeat."
                cta = "Follow for more practical strategies."
            hs["script"] = f"""## 🚨 HOOK

{hook}

## 📦 BODY

{body}

## 🎬 VISUAL INSTRUCTIONS

**Shot 1 — 0-3 seconds:** Look directly at the camera and deliver the hook.

**Shot 2 — 3-15 seconds:** Explain the main point.

**Shot 3 — 15-30 seconds:** Show an example, product, location, screen recording, or demonstration.

**Shot 4 — Final seconds:** Return to the camera and deliver the CTA.

## 🎯 CALL TO ACTION

{cta}

## 🎥 RECORDING TIP

Keep the camera vertical. Use good lighting. Remove unnecessary pauses. Change your visual every few seconds. Add captions when editing.
"""
            st.success(f"🎉 Script ready! {hs['scripts_left']} generation(s) remaining.")

    if hs["script"]:
        st.markdown("### 🎬 Your Script")
        st.markdown(hs["script"])
        st.markdown('<div class="section-label">📲 STEP 4 — READY-TO-POST CAPTION</div>', unsafe_allow_html=True)
        hs["caption"] = f"""🔥 {hs['current_topic']}

Most people don't realize this until it's too late.

Watch till the end and let me know what you think 👇

Follow for more practical content.

#Kenya #KenyanCreators #HustleKE #ContentCreator"""
        st.text_area("Copy this caption:", value=hs["caption"], height=180, key="caption_box")
        st.success("🎉 Your content package is ready!")
        st.markdown("""
<div class="workflow-card">
<strong>🚀 WHAT'S NEXT?</strong><br><br>
1️⃣ Record your video<br><br>2️⃣ Open 🎬 Caption King Studio<br><br>3️⃣ Upload your video<br><br>4️⃣ Add your captions<br><br>5️⃣ Download and post 📱
</div>
""", unsafe_allow_html=True)

# ============================================================
# CAPTION KING STUDIO
# ============================================================
elif page == "🎬 Caption King Studio":
    st.title("🎬 Caption King Studio")
    st.markdown("Turn your recorded video into a captioned short-form video.")
    if hs["captions_left"] > 0:
        st.success(f"🎁 You have **{hs['captions_left']}** free caption export(s) remaining.")
    else:
        st.error("🔒 Your free caption exports have been used.")

    uploaded_video = st.file_uploader("Upload your video", type=["mp4", "mov"])
    col1, col2, col3 = st.columns(3)
    with col1:
        font_style = st.selectbox("Subtitle Font", ["Impact Bold", "Montserrat ExtraBold", "Sheng Modern"])
    with col2:
        caption_pos = st.selectbox("Text Position", ["Center", "Lower Third", "Top Drop"])
    with col3:
        accent_color = st.color_picker("Accent Color", "#FF4B4B")

    st.caption("This basic version burns one selected text line across the video. Automatic speech-to-text captions can be added later.")

    if st.button("🎬 Create Captioned Video", key="create_video"):
        if uploaded_video is None:
            st.error("❌ Please upload a video first.")
        elif not has_credit("captions_left"):
            limit_message("caption exports")
        else:
            input_path = silent_path = final_path = None
            try:
                with st.spinner("🎬 Processing your video..."):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_input:
                        temp_input.write(uploaded_video.read())
                        input_path = temp_input.name

                    cap = cv2.VideoCapture(input_path)
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    if fps == 0 or np.isnan(fps):
                        fps = 30.0

                    silent_path = tempfile.mktemp(suffix=".mp4")
                    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                    out = cv2.VideoWriter(silent_path, fourcc, fps, (width, height))

                    subtitle_text = hs["current_topic"] or "Hustle Studio"
                    rgb = accent_color.lstrip("#")
                    accent_bgr = (int(rgb[4:6], 16), int(rgb[2:4], 16), int(rgb[0:2], 16))
                    font_face = cv2.FONT_HERSHEY_TRIPLEX if font_style == "Impact Bold" else cv2.FONT_HERSHEY_DUPLEX if font_style == "Montserrat ExtraBold" else cv2.FONT_HERSHEY_COMPLEX
                    font_scale = max(0.8, width / 900.0)
                    thickness = max(2, int(font_scale * 2.5))

                    while cap.isOpened():
                        ret, frame = cap.read()
                        if not ret:
                            break
                        (text_w, text_h), baseline = cv2.getTextSize(subtitle_text, font_face, font_scale, thickness)
                        x = max(10, int((width - text_w) / 2))
                        if caption_pos == "Center":
                            y = int((height + text_h) / 2)
                        elif caption_pos == "Top Drop":
                            y = max(text_h + 30, int(height * 0.20))
                        else:
                            y = int(height * 0.78)
                        pad_x = int(20 * font_scale)
                        pad_y = int(15 * font_scale)
                        cv2.rectangle(frame, (max(0, x - pad_x), max(0, y - text_h - pad_y)), (min(width, x + text_w + pad_x), min(height, y + baseline + pad_y)), accent_bgr, -1)
                        cv2.putText(frame, subtitle_text, (x, y), font_face, font_scale, (0, 0, 0), thickness + 3, cv2.LINE_AA)
                        cv2.putText(frame, subtitle_text, (x, y), font_face, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
                        out.write(frame)

                    cap.release()
                    out.release()
                    final_path = tempfile.mktemp(suffix=".mp4")
                    subprocess.run(["ffmpeg", "-y", "-i", silent_path, "-i", input_path, "-map", "0:v:0", "-map", "1:a:0?", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", final_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                    with open(final_path, "rb") as video_file:
                        hs["processed_video"] = video_file.read()
                    use_credit("captions_left")
                st.success("🎉 Your captioned video is ready!")
            except FileNotFoundError:
                st.error("❌ FFmpeg is not available in this Streamlit environment.")
            except subprocess.CalledProcessError:
                st.error("❌ FFmpeg could not finish processing this video.")
            except Exception as error:
                st.error(f"❌ Video processing error: {error}")
            finally:
                for path in [input_path, silent_path, final_path]:
                    if path and os.path.exists(path):
                        try:
                            os.unlink(path)
                        except Exception:
                            pass

    if hs["processed_video"] is not None:
        st.markdown("---")
        st.subheader("🎉 Your Finished Video")
        st.video(hs["processed_video"])
        st.download_button("📥 Download Captioned Video", data=hs["processed_video"], file_name="hustlestudio_captioned.mp4", mime="video/mp4", key="download_video")

# ============================================================
# MONETIZATION PORTAL
# ============================================================
else:
    st.title("👤 Monetization Portal")
    st.markdown("Simple plans for creators who want more from Hustle Studio.")

    st.subheader("🆓 Free Creator")
    st.markdown("""
<div class="workflow-card">
<h3>🆓 Free Creator</h3>
<p>Try the Hustle Studio workflow.</p>
<ul><li>10 content idea generations</li><li>10 hook generations</li><li>5 script generations</li><li>3 caption exports</li><li>Mobile-friendly workflow</li></ul>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🚀 Hustler Weekly")
    st.markdown("""
<div class="workflow-card">
<h3>🚀 Hustler Weekly</h3><h2>KSh 150</h2>
<p>7 days of higher creator limits.</p>
<ul><li>More ideas</li><li>More hooks</li><li>More scripts</li><li>More caption exports</li><li>Full creator workflow</li></ul>
</div>
""", unsafe_allow_html=True)
    if st.button("🚀 Unlock Weekly Plan", key="weekly_plan"):
        st.info("📲 M-Pesa payment integration can be connected here.")

    st.markdown("---")
    st.subheader("🏆 Creator Pro")
    st.markdown("""
<div class="workflow-card">
<h3>🏆 Creator Pro</h3><h2>KSh 500 / month</h2>
<p>For serious creators.</p>
<ul><li>Higher AI limits</li><li>More video exports</li><li>Advanced creator tools</li><li>Priority processing</li><li>Future creator analytics</li></ul>
</div>
""", unsafe_allow_html=True)
    if st.button("🏆 Unlock Creator Pro", key="pro_plan"):
        st.info("📲 M-Pesa subscription integration can be connected here.")

st.markdown("---")
st.caption("🚀 Hustle Studio — Idea → Hook → Script → Caption → Post")
