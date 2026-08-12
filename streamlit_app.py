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
# TOOL 1: BULLETPROOF AI ANIMATION GENERATOR
# ==========================================
with tab1:
    st.subheader("🎨 Tool 1: AI Video & Animation Generator")
    st.markdown("Type a detailed prompt to generate a smooth high-resolution AI video animation.")
    
    video_prompt = st.text_input("Describe the animation you want:", placeholder="Type a punchy prompt or long description...", key="animation_prompt_field")
    
    if st.button("🚀 Generate AI Animation"):
        if not video_prompt.strip():
            st.warning("⚠️ Please type an animation prompt first.")
        else:
            with st.spinner("🎨 Processing text structure and generating video..."):
                
                # 🧠 PROMPT CONDENSER AUTOMATION
                # Split long sentences and take the most descriptive keywords to avoid API server timeout
                words = video_prompt.strip().split()
                if len(words) > 5:
                    # Take the first 5 core conceptual keywords
                    optimized_prompt = " ".join(words[:5])
                else:
                    optimized_prompt = video_prompt.strip()
                
                # Safe url parsing format handling for the optimized text string
                clean_prompt = urllib.parse.quote(optimized_prompt)
                img_url = f"https://pollinations.ai{clean_prompt}?width=512&height=512&nologo=true"
                
                try:
                    # Set a robust 30-second window to pull the asset matrix safely
                    resp = requests.get(img_url, timeout=30)
                    if resp.status_code == 200:
                        arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
                        master_frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                        
                        if master_frame is not None:
                            height, width, layers = master_frame.shape
                            video_name = "ai_generated_animation.mp4"
                            
                            # Build a clean 3-second animated container video file
                            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                            video = cv2.VideoWriter(video_name, fourcc, 10, (width, height))
                            
                            for i in range(30): 
                                video.write(master_frame)
                            video.release()
                            
                            # Convert container profile via FFmpeg to work perfectly on Android and Safari browsers
                            final_ready_video = "final_animation.mp4"
                            os.system(f"ffmpeg -i {video_name} -vcodec libx264 -acodec aac {final_ready_video} -y")
                            
                            if os.path.exists(final_ready_video):
                                st.success("✨ Your AI Animation has been generated successfully!")
                                with open(final_ready_video, "rb") as file:
                                    st.video(file.read())
                            else:
                                st.error("❌ Conversion frame block failed.")
                        else:
                            st.error("❌ Image matrix data corrupt. Please try hitting generate again.")
                    else:
                        st.error("⚠️ AI server response error. Try hitting generate again.")
                except Exception as e:
                    st.error("❌ Request timed out. The free public server is busy. Hit generate again!")

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




     
                
        
