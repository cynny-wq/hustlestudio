import streamlit as st
import whisper
import os
import subprocess

# Set page title and theme layout
st.set_page_config(page_title="HustleStudio Suite", page_icon="🚀", layout="centered")

st.title("🚀 HustleStudio Suite")
st.markdown("Standalone digital tools designed to help Kenyan content creators grow fast.")

# Create the tab navigation
tab1, tab2 = st.tabs(["💡 Tool 1: Viral Hook Bot", "🎬 Tool 4: Caption King"])
import pandas as pd

# Initialize tracking state in the user's browser session
if "payment_unlocked" not in st.session_state:
    st.session_state.payment_unlocked = False

if not st.session_state.payment_unlocked:
    st.markdown("---")
    st.info("🔒 **Premium Access Required**")
    st.markdown("""
    Spend **200 KES** once to save thousands on editing fees and eliminate hours of creative block this month.
    
    ### How to Unlock Instantly:
    1. Go to M-Pesa -> **Send Money**
    2. Enter Phone Number: **[0799090363]**
    3. Amount: **200 KES**
    4. Once you send, paste your **M-Pesa Transaction Code** below to activate your 30-day access.
    """)
    
    user_code = st.text_input("Enter M-Pesa Transaction Code (e.g., SGH48DKJ93)").strip().upper()
    
    if st.button("🔓 Verify & Activate Suite"):
        try:
            # Replace the link below with your actual Google Sheets CSV Publish link
            sheet_csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT73hZNiNltEbq8LwrJjr8gXbrgeSbAHlaMKvtkb3Ahja9lxsIGeybwJz8CJ7fQ_Qibee2D3h-EKV-i/pub?output=csv"
            
            # Read your active spreadsheet from the cloud instantly
            df = pd.read_csv(sheet_csv_url)
            
            # Convert all codes in your sheet to clean, uppercase text strings
            valid_codes = df['mpesa_code'].astype(str).str.strip().str.upper().tolist()
            
            if user_code in valid_codes:
                st.session_state.payment_unlocked = True
                st.success("✅ Payment verified! Unlocking your creator tools...")
                st.rerun()
            else:
                st.error("❌ Transaction code not found. If you just sent the payment, please allow 2 minutes for activation.")
               except Exception as e:
            st.error(f"⚠️ System verification glitch. Error details: {str(e)}")

            
    st.stop() # Prevents users from seeing your tools unless unlocked

# ==========================================
# TAB 1: KENYAN VIRAL HOOK GENERATOR
# ==========================================
with tab1:
    st.subheader("💡 Tool 1: Viral Hook Bot")
    st.markdown("Beat creative block instantly. Get hooks tailored for local audiences.")
    
    topic = st.text_input("What is your video about? (e.g., 'selling clothes', 'cooking pilau')", key="topic_input")
    
    if st.button("⚡ Generate Viral Hooks"):
        if not topic.strip():
            st.warning("⚠️ Please enter a topic first.")
        else:
            t = topic.strip()
            hooks = [
                f"🚨 USIWAHI jaribu {t} hapa Kenya kabla ujue hii siri...",
                f"💡 Mbona hakuna mtu anakuambia ukweli kuhusu {t}?",
                f"🛑 Kama unataka kufanya {t} mwaka huu, acha kila kitu unafanya na uangalie hii!",
                f"🤫 Hii hapa siri ya {t} yenye matajiri wa Nairobi hawataki ujue.",
                f"🔥 Umechoka kuhustle na {t} na haupati matokeo? Hapa ndio mistake unafanya..."
            ]
            st.markdown(f"### 🚀 Viral Hooks Generated for: '{t}'")
            for idx, hook in enumerate(hooks, start=1):
                st.markdown(f"{idx}. **{hook}**")

# ==========================================
# TAB 2: CAPTION KING (SUBTITLE GENERATOR)
# ==========================================
with tab2:
    st.subheader("🎬 Tool 4: Caption King")
    st.markdown("Hardcode professional, mobile-ready yellow subtitles automatically.")
    
    uploaded_file = st.file_uploader("Upload Raw Video (MP4)", type=["mp4"])
    
    if uploaded_file is not None:
        # Save the uploaded file temporarily to disk
        with open("input_video.mp4", "wb") as f:
            f.write(uploaded_file.read())
            
        if st.button("🔥 Generate Captions"):
            with st.spinner("🎬 Extracting audio and transcribing speech (This takes a moment)..."):
                # Run speech-to-text
                model = whisper.load_model("base")
                result = model.transcribe("input_video.mp4")
                
                # Write standard subtitle file
                with open("subtitles.srt", "w", encoding="utf-8") as srt:
                    for i, segment in enumerate(result['segments'], start=1):
                        start, end, text = segment['start'], segment['end'], segment['text'].strip()
                        
                        def format_time(seconds):
                            h = int(seconds // 3600)
                            m = int((seconds % 3600) // 60)
                            s = int(seconds % 60)
                            ms = int((seconds % 1) * 1000)
                            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
                            
                        srt.write(f"{i}\n{format_time(start)} --> {format_time(end)}\n{text}\n\n")
            
            with st.spinner("🔥 Burning styled subtitles directly into the video..."):
                # Run FFmpeg command safely on the hosting system
                style = "Fontsize=22,PrimaryColour=&H00FFFF,OutlineColour=&H000000,BorderStyle=1,Outline=2,Alignment=2"
                cmd = f'ffmpeg -i input_video.mp4 -vf "subtitles=subtitles.srt:force_style=\'{style}\'" -c:a copy output_captioned.mp4 -y'
                
                process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                if process.returncode == 0 and os.path.exists("output_captioned.mp4"):
                    st.success("✅ Subtitles burned perfectly!")
                    # Display the final captioned video to the user
                    with open("output_captioned.mp4", "rb") as video_file:
                        st.video(video_file.read())
                else:
                    st.error("❌ Something went wrong while saving the video frames.")
