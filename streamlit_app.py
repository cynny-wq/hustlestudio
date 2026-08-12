import streamlit as st
import whisper
import os
import subprocess
import cv2
import numpy as np

st.set_page_config(page_title="HustleStudio Suite", page_icon="🚀", layout="centered")
st.title("🚀 HustleStudio Suite")
st.markdown("Standalone digital tools designed to help Kenyan content creators grow fast.")

# Create the clean product tab structure
tab1, tab2, tab3 = st.tabs(["🎨 Tool 1: AI Animation Gen", "💡 Tool 2: Viral Hooks", "🎬 Tool 3: Caption King"])

# ==========================================
# TOOL 1: 100% LOCAL STANDALONE GENERATOR
# ==========================================
with tab1:
    st.subheader("🎨 Tool 1: AI Video & Animation Generator")
    st.markdown("Type any prompt. The engine creates an automated mathematical visual loop locally.")
    
    video_prompt = st.text_input("Describe the animation layout details:", placeholder="Type a prompt to initialize the visual seed...", key="animation_prompt_field")
    
    if st.button("🚀 Generate AI Animation"):
        if not video_prompt.strip():
            st.warning("⚠️ Please type an animation prompt first.")
        else:
            with st.spinner("🎨 Compiling independent pixel layers into video container..."):
                
                # Generate a unique color configuration palette matrix using the user's prompt text length
                seed_value = sum(ord(char) for char in video_prompt.strip()) % 256
                
                # Build an array containing 24 fluid animated frame matrices
                width, height = 512, 512
                frames = []
                
                for f in range(24):
                    # Compile a base background canvas layout pattern
                    frame = np.zeros((height, width, 3), dtype=np.uint8)
                    
                    # Compute fluid dynamic wave patterns across individual pixel fields
                    for r in range(0, height, 4):
                        dynamic_wave = int(128 + 127 * np.sin((r + f * 10) * 0.05))
                        color_mix = (dynamic_wave, (seed_value * 2) % 256, (dynamic_wave + seed_value) % 256)
                        cv2.line(frame, (0, r), (width, r), color_mix, 4)
                        
                    # Inject a central orbital shape structure layer to track visual motion pacing
                    center_x = int(width / 2 + 50 * np.cos(f * 0.2))
                    center_y = int(height / 2 + 50 * np.sin(f * 0.2))
                    cv2.circle(frame, (center_x, center_y), 60, ((seed_value + 100) % 256, 255, 255), -1)
                    
                    frames.append(frame)
                
                # Save data array objects natively into a streamable MP4 format container
                video_name = "local_matrix_animation.mp4"
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                video = cv2.VideoWriter(video_name, fourcc, 12, (width, height)) # 12 frames per second
                
                for frame in frames:
                    video.write(frame)
                video.release()
                
                # Convert profile code using FFmpeg to work perfectly on any device mobile screen
                final_ready_video = "final_animation.mp4"
                os.system(f"ffmpeg -i {video_name} -vcodec libx264 -acodec aac {final_ready_video} -y")
                
                if os.path.exists(final_ready_video):
                    st.success("✨ Your standalone visual loop animation has been generated successfully!")
                    with open(final_ready_video, "rb") as file:
                        st.video(file.read())
                else:
                    st.error("❌ Conversion frame block failed.")

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




     
                
        
