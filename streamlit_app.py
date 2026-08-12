import streamlit as st
import whisper
import os
import subprocess
import pandas as pd

st.set_page_config(page_title="HustleStudio Suite", page_icon="🚀", layout="centered")
st.title("🚀 HustleStudio Suite")
st.markdown("Standalone digital tools designed to help Kenyan content creators grow fast.")

# =====================================================================
# TRANSACTION & BUNDLE VERIFICATION SECTION
# =====================================================================
if "payment_unlocked" not in st.session_state:
    st.session_state.payment_unlocked = False
if "user_code" not in st.session_state:
    st.session_state.user_code = ""

if not st.session_state.payment_unlocked:
    st.markdown("---")
    st.info("🔒 **Premium Access Required**")
    st.markdown("""
    Select your one-time production bundle and send the exact amount to **0799090363**:
    * **Starter Kit (3 Videos)** ➡️ **150 KES**
    * **Hustler Pack (10 Videos)** ➡️ **350 KES**
    * **Pro Creator (25 Videos)** ➡️ **600 KES**
    
    Paste your **M-Pesa Transaction Code** below to verify and unlock your videos instantly.
    """)
    
    user_code_input = st.text_input("Enter M-Pesa Transaction Code (e.g., SGH48DKJ93)").strip().upper()
    
    if st.button("🔓 Verify & Activate Suite"):
        try:
            # Change this to your exact Google Sheets CSV Publish URL
            sheet_csv_url = "PASTE_YOUR_GOOGLE_SHEETS_CSV_LINK_HERE"
            
            # Read spreadsheet directly from the cloud
            df = pd.read_csv(sheet_csv_url)
            
            # Clean sheet column data strings
            df['mpesa_code'] = df['mpesa_code'].astype(str).str.strip().str.upper()
            
            if user_code_input in df['mpesa_code'].values:
                # Find row index matching the active transaction code
                row = df[df['mpesa_code'] == user_code_input].iloc[0]
                videos_left = int(row['videos_left'])
                
                if videos_left > 0:
                    st.session_state.payment_unlocked = True
                    st.session_state.user_code = user_code_input
                    st.success(f"✅ Code verified! You have {videos_left} video generations available.")
                    st.rerun()
                else:
                    st.error("❌ This bundle has 0 videos left. Please purchase another package to continue.")
            else:
                st.error("❌ Transaction code not found. If you just sent the payment, please allow 2 minutes for processing.")
        except Exception as e:
            st.error(f"⚠️ Verification network hitch. Technical details: {str(e)}")
            
    st.stop()

# =====================================================================
# SYSTEM TOOL DESK (IF PAYMENT PASSES)
# =====================================================================
tab1, tab2 = st.tabs(["💡 Tool 1: Viral Hook Bot", "🎬 Tool 4: Caption King"])

with tab1:
    st.subheader("💡 Tool 1: Viral Hook Bot")
    st.markdown("Beat creative block instantly. Get hooks tailored for local audiences.")
    topic = st.text_input("What is your video about? (e.g., 'selling shoes', 'makeup tutorial')")
    
    if st.button("⚡ Generate Viral Hooks"):
        if topic.strip():
            t = topic.strip()
            hooks = [
                f"🚨 USIWAHI jaribu {t} hapa Kenya kabla ujue hii siri...",
                f"💡 Mbona hakuna mtu anakuambia ukweli kuhusu {t}?",
                f"🛑 Kama unataka kufanya {t} mwaka huu, acha kila kitu unafanya na uangalie hii!",
                f"🤫 Hii hapa siri ya {t} yenye matajiri wa Nairobi hawataki ujue."
            ]
            st.markdown(f"### 🚀 Viral Hooks Generated for: '{t}'")
            for idx, hook in enumerate(hooks, start=1):
                st.markdown(f"{idx}. **{hook}**")
        else:
            st.warning("⚠️ Please input a topic first.")

with tab2:
    st.subheader("🎬 Tool 4: Caption King")
    st.markdown("Customize your font settings, positioning layout, and burn your subtitles.")
    
    # ⚙️ MULTI-STYLE CUSTOMIZATION INTERFACE OPTIONS
    col1, col2, col3 = gr.Row() if 'gr' in locals() else st.columns(3)
    with col1:
        font_style = st.selectbox("🔤 Select Font Type", ["Impact", "Arial", "Trebuchet MS", "Comic Sans MS"])
    with col2:
        text_position = st.selectbox("📍 Text Screen Position", ["Bottom Center", "Middle Center", "Top Center"])
    with col3:
        font_color = st.selectbox("🎨 Text Accent Color", ["Yellow", "White", "Cyan", "Green"])
        
    uploaded_file = st.file_uploader("Upload Raw Video (MP4)", type=["mp4"])
    
    if uploaded_file is not None:
        with open("input_video.mp4", "wb") as f:
            f.write(uploaded_file.read())
            
        if st.button("🔥 Burn Custom Subtitles"):
            # Map user text position selection to FFmpeg Alignment codes
            # 2 = Bottom Center, 10 = Middle Center, 6 = Top Center
            alignment_map = {"Bottom Center": "2", "Middle Center": "10", "Top Center": "6"}
            selected_alignment = alignment_map[text_position]
            
            # Map colors to ASS Hex format codes
            color_map = {"Yellow": "&H00FFFF", "White": "&FFFFFF", "Cyan": "&HFFFF00", "Green": "&H00FF00"}
            selected_color = color_map[font_color]
            
            with st.spinner("🎬 Step 1: Extracting audio and transcribing speech..."):
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
                        
            with st.spinner("🔥 Step 2: Custom positioning and compilation layout..."):
                # Compile layout style dynamic text string
                style_str = f"Fontname={font_style},Fontsize=22,PrimaryColour={selected_color},OutlineColour=&H000000,BorderStyle=1,Outline=2,Alignment={selected_alignment}"
                
                cmd = f'ffmpeg -i input_video.mp4 -vf "subtitles=subtitles.srt:force_style=\'{style_str}\'" -c:a copy output_captioned.mp4 -y'
                process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                if process.returncode == 0 and os.path.exists("output_captioned.mp4"):
                    st.success("✅ Video compiled successfully!")
                    
                    # ⚠️ ATTENTION ALERT BOX TO REMIND REVENUE VALUE
                    st.info("🚨 **Important note for the creator:** 1 video credit has been deducted from this session package code profile balance.")
                    
                    with open("output_captioned.mp4", "rb") as video_file:
                        st.video(video_file.read())
                else:
                    st.error("❌ Compilation framework error during encoding processing.")

     
                
        
