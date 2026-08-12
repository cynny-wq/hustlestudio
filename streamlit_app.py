import streamlit as st
import whisper
import os
import subprocess

st.set_page_config(page_title="HustleStudio Suite", page_icon="🚀", layout="centered")
st.title("🚀 HustleStudio Suite")
st.markdown("Standalone digital tools designed to help Kenyan content creators grow fast.")

# Clean product navigation desk layout
tab1, tab2 = st.tabs(["💡 Tool 1: Viral Hook Bot", "🎬 Tool 2: Caption King"])

# ==========================================
# TOOL 1: KENYAN VIRAL HOOKS
# ==========================================
with tab1:
    st.subheader("💡 Tool 1: Viral Hook Bot")
    st.markdown("Beat creative block instantly. Get hooks tailored for local audiences.")
    topic = st.text_input("What is your video about? (e.g., 'selling shoes', 'cooking pilau')", key="hooks_topic_field")
    
    if st.button("⚡ Generate Hooks"):
        if topic.strip():
            t = topic.strip()
            st.markdown(f"### 🚀 Viral Hooks Generated for: '{t}'")
            st.markdown(f"1. **🚨 USIWAHI jaribu {t} hapa Kenya kabla ujue hii siri...**")
            st.markdown(f"2. **💡 Mbona hakuna mtu anakuambia ukweli kuhusu {t}?**")
            st.markdown(f"3. **🤫 Hii hapa siri ya {t} yenye matajiri wa Nairobi hawataki ujue.**")
            st.markdown(f"4. **🔥 Umechoka kuhustle na {t} na haupati matokeo? Hapa ndio mistake unafanya...**")
        else:
            st.warning("⚠️ Please input a topic description first.")

# ==========================================
# TOOL 2: CAPTION KING (SUBTITLE ENGINE)
# ==========================================
with tab2:
    st.subheader("🎬 Tool 2: Caption King")
    st.markdown("Upload your video file to burn clean, styled mobile titles automatically.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        font_style = st.selectbox("🔤 Font Type", ["Impact", "Arial", "Trebuchet MS"])
    with col2:
        text_position = st.selectbox("📍 Screen Position", ["Bottom Center", "Middle Center", "Top Center"])
    with col3:
        font_color = st.selectbox("🎨 Accent Color", ["Yellow", "White", "Cyan"])
        
    uploaded_file = st.file_uploader("Upload Video (MP4)", type=["mp4"], key="video_uploader_field")
    
    if uploaded_file is not None:
        # Save file directly onto disk workspace
        with open("input_video.mp4", "wb") as f:
            f.write(uploaded_file.read())
            
        if st.button("🔥 Burn Custom Subtitles"):
            with st.spinner("🎬 Step 1: Extracting audio and transcribing speech text..."):
                model = whisper.load_model("base")
                result = model.transcribe("input_video.mp4")
                
                with open("subtitles.srt", "w", encoding="utf-8") as srt:
                    for i, segment in enumerate(result['segments'], start=1):
                        start, end, text = segment['start'], segment['end'], segment['text'].strip()
                        
                        def format_time(seconds):
                            h, m, s = int(seconds // 3600), int((seconds % 3600) // 60), int(seconds % 60)
                            ms = int((seconds % 1) * 1000)
                            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
                        srt.write(f"{i}\n{format_time(start)} --> {format_time(end)}\n{text}\n\n")
                        
            with st.spinner("🔥 Step 2: Running layout styles and burning captions..."):
                align = "2" if text_position == "Bottom Center" else ("10" if text_position == "Middle Center" else "6")
                color = "&H00FFFF" if font_color == "Yellow" else ("&FFFFFF" if font_color == "White" else "&HFFFF00")
                
                style_str = f"Fontname={font_style},Fontsize=22,PrimaryColour={color},OutlineColour=&H000000,BorderStyle=1,Outline=2,Alignment={align}"
                cmd = f'ffmpeg -i input_video.mp4 -vf "subtitles=subtitles.srt:force_style=\'{style_str}\'" -c:a copy output_captioned.mp4 -y'
                
                process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                if process.returncode == 0 and os.path.exists("output_captioned.mp4"):
                    st.success("✅ Video captioned perfectly!")
                    with open("output_captioned.mp4", "rb") as video_file:
                        st.video(video_file.read())
                else:
                    st.error("❌ Encoding runtime error during compilation processing.")
