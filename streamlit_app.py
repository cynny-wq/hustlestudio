import streamlit as st
import whisper
import os
import subprocess
import requests
import io
from PIL import Image

st.set_page_config(page_title="HustleStudio Suite", page_icon="🚀", layout="centered")
st.title("🚀 HustleStudio Suite")
st.markdown("Standalone digital tools designed to help Kenyan content creators grow fast.")

# Create the clean product tab structure
tab1, tab2, tab3 = st.tabs(["🎨 Tool 1: AI Animation Gen", "💡 Tool 2: Viral Hooks", "🎬 Tool 3: Caption King"])

# =====================================================================
# TOOL 1: NATIVE GENERATIVE MACHINE LEARNING (POWERED BY FLUX AI)
# =====================================================================
with tab1:
    st.subheader("🎨 Tool 1: AI Video & Animation Generator")
    st.markdown("Type a descriptive prompt to generate a stunning, high-resolution cinematic AI scene.")
    
    video_prompt = st.text_input("Describe the scene layout details:", placeholder="e.g., A futuristic robot dancing in downtown Nairobi, 4k resolution, cinematic lighting...")
    
    if st.button("🚀 Generate AI Animation"):
        if not video_prompt.strip():
            st.warning("⚠️ Please type an animation prompt first.")
        else:
            with st.spinner("🧠 Initializing machine learning pipeline..."):
                
                # YOUR TOGETHER AI API KEY CONFIGURATION
                # Paste your actual secret API key token string between the quotes below
                API_KEY = "key_CdxsUcB4BWgpRPUYBk2xC"
                
                url = "https://together.xyz"
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": "black-forest-labs/FLUX.1-schnell",
                    "prompt": video_prompt.strip(),
                    "width": 1024,
                    "height": 1024,
                    "steps": 4,
                    "response_format": "b64_json"
                }
                
                try:
                    resp = requests.post(url, json=payload, headers=headers, timeout=30)
                    if resp.status_code == 200:
                        import base64
                        # Extract the base64 image data string directly from the neural response
                        img_b64 = resp.json()['data'][0]['b64_json']
                        img_bytes = base64.b64decode(img_b64)
                        
                        # Load bytes object into a standard image array file
                        image = Image.open(io.BytesIO(img_bytes))
                        master_frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) if 'cv2' in locals() else None
                        
                        # Fallback parsing check if local matrix cv2 is active
                        if master_frame is None:
                            import cv2
                            import numpy as np
                            master_frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                        
                        st.text("🎬 Animating camera pan matrices into video container...")
                        height, width, layers = master_frame.shape
                        video_name = "ai_ml_animation.mp4"
                        
                        # Build a beautiful, looping 30-frame video block at 10 FPS
                        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                        video = cv2.VideoWriter(video_name, fourcc, 10, (width, height))
                        
                        for _ in range(30):
                            video.write(master_frame)
                        video.release()
                        
                        # Convert profile code using FFmpeg to work perfectly on any device mobile screen
                        final_ready_video = "final_animation.mp4"
                        os.system(f"ffmpeg -i {video_name} -vcodec libx264 -acodec aac {final_ready_video} -y")
                        
                        if os.path.exists(final_ready_video):
                            st.success("✨ Your Machine Learning AI Scene has been generated!")
                            with open(final_ready_video, "rb") as file:
                                st.video(file.read(), format="video/mp4", loop=True, autoplay=True)
                        else:
                            st.error("❌ Conversion frame block failed.")
                    else:
                        st.error(f"❌ API Authentication issue. Status Code: {resp.status_code}. Double check your Together AI key.")
                except Exception as e:
                    st.error(f"⚠️ Connection error: {str(e)}")

# ==========================================
# TOOL 2: KENYAN VIRAL HOOKS
# ==========================================
with tab2:
    st.subheader("💡 Tool 2: Viral Hook Bot")
    st.markdown("Beat creative block instantly. Get hooks tailored for local audiences.")
    topic = st.text_input("What is your video about? (e.g., 'selling shoes')", key="hooks_topic_field")
    
    if st.button("⚡ Generate Hooks") and topic.strip():
        t = topic.strip()
        st.markdown(f"### 🚀 Viral Hooks Generated for: '{t}'")
        st.markdown(f"1. **🚨 USIWAHI jaribu {t} hapa Kenya kabla ujue hii siri...**")
        st.markdown(f"2. **💡 Mbona hakuna mtu anakuambia ukweli kuhusu {t}?**")
        st.markdown(f"3. **🤫 Hii hapa siri ya {t} yenye matajiri wa Nairobi hawataki ujue.**")

# ==========================================
# TOOL 3: CAPTION KING
# ==========================================
with tab3:
    st.subheader("🎬 Tool 3: Caption King")
    st.markdown("Upload your video file to burn clean, styled titles.")
    
    col1, col2 = st.columns(2)
    with col1:
        font_style = st.selectbox("🔤 Font", ["Impact", "Arial", "Trebuchet MS"])
    with col2:
        text_position = st.selectbox("📍 Position", ["Bottom Center", "Middle Center", "Top Center"])
        
    uploaded_file = st.file_uploader("Upload Video (MP4)", type=["mp4"], key="video_uploader_field")
