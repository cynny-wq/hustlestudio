import streamlit as st
import whisper
import os
import subprocess
import requests
import cv2
import numpy as np

st.set_page_config(page_title="HustleStudio Suite", page_icon="🚀", layout="centered")
st.title("🚀 HustleStudio Suite")

# ==========================================
# NEW TOOL: STANDALONE AI ANIMATION GENERATOR
# ==========================================
tab1, tab2, tab3 = st.tabs(["🎨 Tool 1: AI Animation Gen", "💡 Tool 2: Viral Hooks", "🎬 Tool 3: Caption King"])

with tab1:
    st.subheader("🎨 Tool 1: AI Video & Animation Generator")
    st.markdown("Type a prompt to watch the cloud generate a smooth AI visual loop from scratch.")
    
    video_prompt = st.text_input("Describe the animation you want (e.g., 'cyberpunk city neon rain', 'cosmic galaxy swirling')", placeholder="Type here...")
    
    if st.button("🚀 Generate AI Animation"):
        if not video_prompt.strip():
            st.warning("⚠️ Please type an animation prompt first.")
        else:
         with st.spinner("🎨 Designing AI animation frames... This takes about 15 seconds."):
                frames = []
                
                # FIX: Use standard urllib quoting to handle long sentences properly
                import urllib.parse
                clean_prompt = urllib.parse.quote(video_prompt.strip())
                
                # We will generate 8 high-quality animation frames to prevent timeout blips
                for i in range(8):
                    img_url = f"https://pollinations.ai{clean_prompt}?width=512&height=512&seed={200 + i}&enhance=false"
                    try:
                        resp = requests.get(img_url, timeout=15)
                        if resp.status_code == 200:
                            arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
                            img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                            if img is not None:
                                frames.append(img)
                    except:
                        pass

                    try:
                        resp = requests.get(img_url, timeout=10)
                        if resp.status_code == 200:
                            arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
                            img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                            if img is not None:
                                frames.append(img)
                    except:
                        pass
                
                if len(frames) > 0:
                    st.text("🎬 Compiling frames into high-speed video... (Almost done)")
                    # Save frames into an uncompressed local container video file
                    height, width, layers = frames[0].shape
                    video_name = "ai_generated_animation.mp4"
                    
                    # Codec framework configuration for pure local encoding compatibility
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    video = cv2.VideoWriter(video_name, fourcc, 5, (width, height)) # 5 frames per second loop
                    
                    for frame in frames:
                        video.write(frame)
                    video.release()
                    
                    # Convert via FFmpeg to make it streamable on mobile phone browsers
                    final_ready_video = "final_animation.mp4"
                    os.system(f"ffmpeg -i {video_name} -vcodec libx264 -acodec aac {final_ready_video} -y")
                    
                    if os.path.exists(final_ready_video):
                        st.success("✨ Your AI Animation has been generated!")
                        with open(final_ready_video, "rb") as file:
                            st.video(file.read())
                    else:
                        st.error("❌ Conversion frame block failed.")
                else:
                    st.error("❌ Cloud server was busy. Please try hitting generate again!")

# ==========================================
# OLD TOOLS (RETAINED IN BACKGROUND)
# ==========================================
with tab2:
    st.subheader("💡 Tool 2: Viral Hook Bot")
    topic = st.text_input("What is your video about?")
    if st.button("⚡ Generate Hooks") and topic.strip():
        st.markdown(f"1. **🚨 USIWAHI jaribu {topic} hapa Kenya...**")

with tab3:
    st.subheader("🎬 Tool 3: Caption King")
    uploaded_file = st.file_uploader("Upload Video (MP4)", type=["mp4"])


     
                
        
