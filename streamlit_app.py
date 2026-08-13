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
