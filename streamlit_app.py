import streamlit as st
import whisper
import os
import subprocess
import requests
import cv2
import numpy as np
import urllib.parse

st.set_page_config(page_title="HustleStudio Suite", page_icon="🚀", layout="centered")
st.title("🚀 HustleStudio Suite")
st.markdown("Standalone digital tools designed to help Kenyan content creators grow fast.")

# Create the clean product tab structure
tab1, tab2, tab3 = st.tabs(["🎨 Tool 1: AI Animation Gen", "💡 Tool 2: Viral Hooks", "🎬 Tool 3: Caption King"])

# ==========================================
# TOOL 1: CINEMATIC AI VIDEO GENERATOR
# ==========================================
with tab1:
    st.subheader("🎨 Tool 1: AI Video & Animation Generator")
    st.markdown("Type a prompt to watch the cloud generate a smooth, high-fidelity cinematic video loop.")
    
    video_prompt = st.text_input("Describe the scene you want to animate:", placeholder="e.g., A sleek sports car driving through Nairobi at night, neon lights...", key="animation_prompt_field")
    
    if st.button("🚀 Generate AI Animation"):
        if not video_prompt.strip():
            st.warning("⚠️ Please type an animation prompt first.")
        else:
            with st.spinner("🎨 Creating high-fidelity AI artwork and animating camera vectors..."):
                
                # Use a fast, highly stable public endpoint that returns immediate high-end artwork
                clean_prompt = urllib.parse.quote(video_prompt.strip())
                img_url = f"https://pollinations.ai{clean_prompt}?width=720&height=720&nologo=true&private=true"
                
                try:
                    resp = requests.get(img_url, timeout=25)
                    if resp.status_code == 200:
                        arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
                        master_img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                        
                        if master_img is not None:
                            st.text("🎬 Animating camera pan frames into video container...")
                            
                            # Video dimensions
                            orig_h, orig_w, _ = master_img.shape
                            crop_w, crop_h = 640, 640  # Output frame size
                            
                            video_name = "ai_panning_animation.mp4"
                            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                            video = cv2.VideoWriter(video_name, fourcc, 24, (crop_w, crop_h)) # 24 FPS for cinematic smoothness
                            
                            # Create a beautiful 2.5-second cinematic slow-zoom and drift loop (60 frames total)
                            for i in range(60):
                                # Calculate moving coordinates for smooth camera motion
                                offset_x = int((orig_w - crop_w) * (i / 60))
                                offset_y = int((orig_h - crop_h) * (0.5 + 0.5 * np.sin(i * 0.1)))
                                
                                # Crop frame dynamically to create motion
                                animated_frame = master_img[0:crop_h, offset_x:offset_x+crop_w]
                                
                                # Ensure frame matches sizing strictly before compiling
                                if animated_frame.shape[1] == crop_w and animated_frame.shape[0] == crop_h:
                                    video.write(animated_frame)
                                else:
                                    # Fallback resizing if borders touch
                                    resized = cv2.resize(master_img[0:crop_h, 0:orig_w], (crop_w, crop_h))
                                    video.write(resized)
                                    
                            video.release()
                            
                            # Convert via FFmpeg to stream beautifully on mobile browsers
                            final_ready_video = "final_animation.mp4"
                            os.system(f"ffmpeg -i {video_name} -vcodec libx264 -acodec aac {final_ready_video} -y")
                            
                            if os.path.exists(final_ready_video):
                                st.success("✨ Your Cinematic AI Video has been generated!")
                                with open(final_ready_video, "rb") as file:
                                    st.video(file.read())
                            else:
                                st.error("❌ Conversion frame block failed.")
                        else:
                            st.error("❌ Image matrix data corrupt. Please try hitting generate again.")
                    else:
                        st.error("⚠️ AI server response error. Try hitting generate again.")
                except Exception as e:
                    st.error("❌ The cloud server timed out under heavy load. Hit generate again to reload the connection!")

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





     
                
        
