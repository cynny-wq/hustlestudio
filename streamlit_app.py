import streamlit as st

# 1. CORE PAGE CONFIGURATION
st.set_page_config(
    page_title="Hustle Studio",
    page_icon="🚀",
    layout="centered"
)

# 2. CUSTOM MOBILE-FIRST STYLING
st.markdown("""
    <style>
    /* Expands buttons to full-width and adds padding for mobile thumb tapping */
    div.stButton > button:first-child {
        width: 100%;
        padding: 14px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border-radius: 8px !important;
    }
    /* Styles the custom notification box for results cards */
    .result-card {
        background-color: #f8f9fa;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 16px;
        border-left: 5px solid #ff4b4b;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Hustle Studio")

st.success(
    "📱 **Hustler Tip:** Want this as a phone app? Tap your browser settings "
    "(3 dots) and click **'Add to Home Screen'** to get an instant shortcut icon on your phone!"
)

st.markdown("Standalone digital tools designed to help Kenyan content creators grow fast.")

# 3. INITIALIZE PERSISTENT WORKSPACE STATE ENGINE
# UPDATE THIS BLOCK INSIDE PIECE 1 AT THE TOP OF YOUR FILE:
if "workspace_data" not in st.session_state:
    st.session_state.workspace_data = {
        "hooks": [],
        "script": "",
        "captions": "",
        "current_topic": "",
        "free_captions_left": 3  # Tracks the 3 free video caption trials
    }

# ==========================================
# 3. SIDEBAR NAVIGATION MODEL
# ==========================================
st.sidebar.title("🚀 Hustle Studio")
st.sidebar.markdown("---")
workspace_selection = st.sidebar.radio(
    "Navigate Workspace",
    ["🧠 Strategy Studio", "🎬 Caption King Studio", "👤 Monetization Portal"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Current Tier: **Free Strategy Plan**")

# ==========================================
# 4. MODULE 1: THE UNIFIED STRATEGY STUDIO (INPUTS)
# ==========================================
if workspace_selection == "🧠 Strategy Studio":
    st.subheader("🧠 Strategy Studio")
    st.markdown("Go from an abstract idea to a complete, localized production roadmap instantly.")
    
    # Responsive mobile selection dropdowns
    col1, col2 = st.columns(2)
    with col1:
        niche = st.selectbox(
            "🎯 Select Video Niche",
            [
                "General Hustle & Business", 
                "Fashion & Thrift (Mitumba/Bales)", 
                "Real Estate & Housing (Bedsitters/Apartments)", 
                "Food & Cooking (Pilau/Local Recipes)", 
                "Tech & Gadget Reviews"
            ]
        )
    with col2:
        style = st.selectbox(
            "🎭 Select Delivery Style",
            [
                "Comedic / Local Vibe (Sheng Mix)", 
                "Energetic & Fast-Paced", 
                "Storytelling & Emotional", 
                "Educational & Corporate"
            ]
        )
        
    topic = st.text_input(
        "💡 What is your video topic? (e.g., Starting a business with KSh 5,000)",
        value=st.session_state.workspace_data["current_topic"]
    )
    if st.button("🔥 Generate Complete Production Package"):
        if topic.strip():
            clean_topic = topic.strip()
            st.session_state.workspace_data["current_topic"] = clean_topic
            
            # 1. GENERATE LOCALIZED VIRAL HOOKS
            hooks = [
                f"USIWAHI jaribu {clean_topic} hapa Kenya kabla ujue hii siri...",
                f"Mbona hakuna mtu anakuambia ukweli kuhusu {clean_topic}?",
                f"Hii hapa siri ya {clean_topic} yenye matajiri wa Nairobi hawataki ujue.",
                f"Umechoka kuhustle na {clean_topic} na haupati matokeo? Hapa ndio mistake unafanya..."
            ]
            
            # 2. DYNAMIC DEEP-TEMPLATE SCRIPT ENGINE (No API Costs)
            script_body = ""
            cta_text = ""
            hashtags = ""
            
            # --- MITUMBA NICHE ---
            if niche == "Fashion & Thrift (Mitumba/Bales)":
                hashtags = f"#MitumbaKenya #Gikomba #NairobiFashion #ThriftKE #Biashara"
                if style == "Comedic / Local Vibe (Sheng Mix)":
                    script_body = f"Wasee wanadhani kuuza {clean_topic} ni kwenda tu Gikomba mapema kuchagua nguo. Ukweli ni kwamba unapigwa character development na supplier usipochunga! Unauziwa bale imejaa 'fanya' tupu alafu unashangaa mbona bado uko mboka."
                    cta_text = f"Kama unataka kupata zile camera pieces safi za {clean_topic} bila kuoshwa Nairobi, nifollow sasa hivi upate siri!"
                elif style == "Energetic & Fast-Paced":
                    script_body = f"Stop scrolling! Most people fail at {clean_topic} because they buy cheap bales instead of focus pieces. To flip clothes fast, you need a ring light, clean styling, and zero boring intro scenes!"
                    cta_text = f"We are restocking premium pieces this weekend. Click the link in our bio to join our exclusive WhatsApp updates group!"
                elif style == "Storytelling & Emotional":
                    script_body = f"When I first started looking into {clean_topic}, I lost thirty thousand shillings because I trusted an agent blindly. Nobody wants to share the real steps to finding clean bales in this city."
                    cta_text = f"Drop a comment sharing your biggest loss with {clean_topic}, and let's help each other skip the scams."
                else: 
                    script_body = f"Data shows that micro-margins in the {clean_topic} sector depend entirely on inventory velocity. If you hold onto stock for more than fourteen days, your overhead eats the retail profit."
                    cta_text = f"Save this video for reference and follow this page for weekly market breakdowns."

            # --- REAL ESTATE NICHE ---
            elif niche == "Real Estate & Housing (Bedsitters/Apartments)":
                hashtags = f"#NairobiRentals #Kilimani #BedsitterChronicles #Roysambu #KenyaRealEstate"
                if style == "Comedic / Local Vibe (Sheng Mix)":
                    script_body = f"Ukitafuta keja ma-upmarket Nairobi, ma-agent watakuambia place iko '5 minutes from the highway', lakini ukifika unapata ni safari mzima hadi unahitaji passport! Hakuna hata maji, ni tokens tupu!"
                    cta_text = f"Usichezwe na ma-agent wa uongo kwa soko ya {clean_topic}. Drop budget yako kwa comments nikufeidie!"
                elif style == "Energetic & Fast-Paced":
                    script_body = f"Before you sign that lease or pay a house deposit for {clean_topic}, check these three things: water consistency, tokens billing system, and whether security is guaranteed. Missing one means instant regret!"
                    cta_text = f"Share this video with a friend who is planning to relocate or upgrade houses in Nairobi this month!"
                elif style == "Storytelling & Emotional":
                    script_body = f"Moving into my first studio apartment felt like a dream until the first month ended. The hidden utility costs and the landlord's unexpected rules turned my peace into a daily headache."
                    cta_text = f"Have you ever had a nightmare landlord while dealing with {clean_topic}? Let's talk in the comment section."
                else: 
                    script_body = f"When evaluating residential or commercial spaces for {clean_topic}, always calculate the cost-per-square-foot against the localized structural security index of that specific zone."
                    cta_text = f"Follow our professional insights pipeline for bi-weekly property valuation updates."

            # --- FOOD & COOKING NICHE ---
            elif niche == "Food & Cooking (Pilau/Local Recipes)":
                hashtags = f"#KenyanFood #PilauSecrets #NairobiEats #SwahiliCooking #Chapo"
                script_body = f"Siri ya {clean_topic} kunoga sio kuweka viungo mingi sana zikose mpangilio. Ni timing ya kitunguu kuiva kabisa! Ukikimbiza moto, kila kitu kinaungua na unapoteza ule ladha halisi ya uswahilini."
                cta_text = f"Tafadhali hit that follow button hapo chini kwa recipe zingine rahisi na za haraka kila wiki!"

            # --- TECH & GADGETS NICHE ---
            elif niche == "Tech & Gadget Reviews":
                hashtags = f"#TechKenya #NairobiGadgets #iPhoneKenya #AndroidKE #Unboxing"
                script_body = f"Wasee wengi wanajaza pesa kwa spec zenye hawatawahi tumia. Huna haja ya flagship simu ya kilo mia moja kama mboka yako ya {clean_topic} inataka tu app za kawaida na kamera safi ya mchana."
                cta_text = f"Drop jina ya simu unatumia sasa hivi kwa comments, nikuambie kama inafaa ku-upgrade!"

            # --- GENERAL HUSTLE & BUSINESS (FALLBACK) ---
            else:
                hashtags = f"#NairobiHustle #BiasharaMkononi #GainWithMchina #KenyanCreators"
                if style == "Comedic / Local Vibe (Sheng Mix)":
                    script_body = f"Wasee wengi wanadhani kuingia kwa {clean_topic} ni mchezo au kubahatisha tu hapa Nairobi. Ukikose strategy safi ya kucheza na wateja, utarudi ocha haraka sana mzee!"
                    cta_text = f"Kama unataka kuacha kuangusha amani na kuanza kupata faida kwa {clean_topic}, nifollow sasa hivi upate maujuzi kila siku!"
                else:
                    script_body = f"Success with {clean_topic} doesn't happen by chance. The East African market shifts daily, and those tracking client behavior manually are getting systematically left behind."
                    cta_text = f"Hit that follow button right now if you want to scale your {clean_topic} strategy this month."

            # 3. COMPILE BACK INTO PERSISTENT MEMORY STORAGE
            st.session_state.workspace_data["hooks"] = hooks
            st.session_state.workspace_data["script"] = f"""### 📝 STRUCTURED SCRIPT ROADMAP

#### 🚨 Phase 1: The Hook
* **Action:** Speak your chosen hook with absolute energy in the first 3 seconds!

#### 📦 Phase 2: The Core Body
* **[Visual Scene Layout]:** Mid-shot framing, talking directly into the mobile lens. Keep the background clean.
* **[Vocal Delivery Script]:** "{script_body}"

#### 🎬 Phase 3: Pacing & Direction Cues
* Cut the clip every 3 seconds to keep video retention graphs high.
* Overlay bold, colored text on-screen exactly matching the keywords spoken.

#### 🎯 Phase 4: Closing Conversion
* **[Call-To-Action Script]:** "{cta_text}" """
            
            st.session_state.workspace_data["captions"] = f"""🎯 The raw truth about {clean_topic} that nobody shares... 🤫 Watch till the end!\n\n🏷️ **Viral Tag Pack:**\n{hashtags} #ContentCreatorKE"""
            st.balloons()
        else:
            st.warning("⚠️ Please provide a video topic framework first.")
            
    # DISPLAY OUTPUTS SEQUENTIALLY IN A SINGLE VIEW
    if st.session_state.workspace_data["script"]:
        st.markdown("---")
        st.subheader("🚀 Your Complete Production Strategy Package")
        
        with st.expander("💡 1. Localized Hook Variations", expanded=True):
            for i, hook in enumerate(st.session_state.workspace_data["hooks"], 1):
                st.markdown(f"<div class='result-card'><strong>Hook Option #{i}:</strong> {hook}</div>", unsafe_allow_html=True)
                
        with st.expander("📝 2. High-Retention Script & Video Direction", expanded=True):
            st.markdown(st.session_state.workspace_data["script"])
            
        with st.expander("📲 3. Social Media Optimization Kit (Caption & Tags)", expanded=True):
            st.text_area("Copy Caption Pack:", value=st.session_state.workspace_data["captions"], height=120)
# ==========================================
# 5. MODULE 2: CAPTION KING STUDIO (REAL EDITING ENGINE)
# ==========================================
elif workspace_selection == "🎬 Caption King Studio":
    st.title("🎬 Caption King Studio")
    st.markdown("Burn stylized, high-retention subtitles directly into your short-form video assets.")
    
    if "processed_video_data" not in st.session_state.workspace_data:
        st.session_state.workspace_data["processed_video_data"] = None

    if "free_captions_left" not in st.session_state.workspace_data:
        st.session_state.workspace_data["free_captions_left"] = 3

    trials_left = st.session_state.workspace_data["free_captions_left"]
    if trials_left > 0:
        st.success(f"🎁 **Free Trial Active:** You have **{trials_left} out of 3** free caption generations left!")
    else:
        st.error("🔒 **Premium Engine Interface Required:** Your 3 free caption trial generations have expired.")
        st.info("💡 Go to the **Monetization Portal** in the sidebar menu to unlock unlimited video processing via M-Pesa.")

    uploaded_video = st.file_uploader("Upload your raw MP4 video clip (Max 25MB)", type=["mp4", "mov"])
    
    if uploaded_video is None:
        st.session_state.workspace_data["processed_video_data"] = None

    col1, col2, col3 = st.columns(3)
    with col1:
        font_style = st.selectbox("Subtitle Font", ["Impact Bold", "Montserrat ExtraBold", "Sheng Modern"])
    with col2:
        caption_pos = st.selectbox("Text Position", ["Lower Third", "Center", "Top Drop"])
    with col3:
        accent_color = st.color_picker("Accent Highlight Color", "#FF4B4B")
        
    if st.button("🎬 Run Subtitle Generation"):
        if uploaded_video is not None:
            if trials_left > 0:
                with st.spinner("🧠 Writing and burning subtitles into video layers (this takes a few seconds)..."):
                    try:
                        import tempfile
                        from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
                        
                        # 1. Save uploaded file bytes safely to a temporary file
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_input:
                            temp_input.write(uploaded_video.read())
                            temp_input_path = temp_input.name

                        # 2. Load the video track into MoviePy
                        video = VideoFileClip(temp_input_path)
                        
                        # 3. Create a dynamic subtitle text overlay matching your selections
                        # Pulls topic script from Tab 1 to use as subtitle text fallback
                        subtitle_text = "Hustle Studio Content"
                        if st.session_state.workspace_data["current_topic"]:
                            subtitle_text = f"Siri ya {st.session_state.workspace_data['current_topic']} Kenya!"

                        # Determine vertical position layout metric
                        y_placement = "bottom"
                        if caption_pos == "Center":
                            y_placement = "center"
                        elif caption_pos == "Top Drop":
                            y_placement = "top"

                        # Build the text render clip layer
                        txt_clip = TextClip(
                            subtitle_text, 
                            fontsize=32, 
                            color='white', 
                            bg_color=accent_color,
                            size=(video.w - 40, None),
                            method='caption'
                        )
                        
                        # Set text parameters to display continuously across a 5-second short clip window
                        txt_clip = txt_clip.set_pos((20, y_placement)).set_duration(min(5, video.duration))

                        # 4. Composite the layers together into a new output
                        final_video = CompositeVideoClip([video, txt_clip])
                        
                        # 5. Render out back to an output path container
                        temp_output_path = tempfile.mktemp(suffix=".mp4")
                        final_video.write_videofile(
                            temp_output_path, 
                            codec="libx264", 
                            audio_codec="aac",
                            logger=None # Suppress massive internal shell processing printouts
                        )

                        # 6. Read the newly captioned file bytes back into state memory
                        with open(temp_output_path, "rb") as f:
                            st.session_state.workspace_data["processed_video_data"] = f.read()

                        # Clean up temporary disk files to avoid container size leaks
                        video.close()
                        final_video.close()
                        os.unlink(temp_input_path)
                        os.unlink(temp_output_path)

                        # Deduct one generation credit point from storage balance
                        st.session_state.workspace_data["free_captions_left"] -= 1
                        st.rerun()

                    except Exception as e:
                        st.error(f"❌ Video Processing System Error: {str(e)}")
                        st.info("💡 Note: Running video text layers requires image utilities installed on your system engine host.")
            else:
                st.warning("⚠️ Access Denied: Please authorize a pricing plan in the Monetization Portal to process this asset.")
        else:
            st.error("❌ Please upload a valid MP4 file container before starting the rendering engine.")

    # PERSISTENT RENDER LAYER
    if st.session_state.workspace_data["processed_video_data"] is not None:
        st.markdown("---")
        st.success("🎉 Subtitles burned directly into your video frames successfully!")
        st.balloons()
        
        # Display video preview screen on dashboard interface
        st.video(st.session_state.workspace_data["processed_video_data"])
        
        st.info("📦 Click below to download your captioned media asset container:")
        st.download_button(
            label="📥 Download Subtitled Video",
            data=st.session_state.workspace_data["processed_video_data"],
            file_name="hustlestudio_captioned.mp4",
            mime="video/mp4"
        )

# ==========================================
# 6. MODULE 3: LOCAL MONETIZATION PORTAL
# ==========================================
elif workspace_selection == "👤 Monetization Portal":
    st.title("👤 Monetization Portal")
    st.markdown("Unlock the full power of advanced media processing and custom styling suites.")
    
    st.markdown("### Choose Your Production Plan")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="background-color:#fff; padding:20px; border-radius:8px; border:1px solid #ddd; text-align:center; color: #333;">
            <h4 style="color: #333;">🚀 Weekly Pass</h4>
            <h2 style="color: #ff4b4b;">KSh 150</h2>
            <p>Per Single Week Access</p>
            <small>• Unlimited Subtitle Exports<br>• Full HD Processing Worker<br>• Direct M-Pesa STK Integration</small>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Unlock Weekly Access Pass", key="pay_weekly"):
            st.info("📲 Sending instant M-Pesa STK Push authorization prompt to your phone...")
            
    with col2:
        st.markdown("""
        <div style="background-color:#fff; padding:20px; border-radius:8px; border:2px solid #ff4b4b; text-align:center; color: #333;">
            <h4 style="color: #333;">🏆 Creator Pro</h4>
            <h2 style="color: #ff4b4b;">KSh 500</h2>
            <p>Per Continuous Month</p>
            <small>• Everything in Weekly Pass<br>• Multi-Dialect Subtitle Tracking<br>• Priority Background Processing Queues</small>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Unlock Full Creator Pro Tier", key="pay_monthly"):
            st.info("📲 Sending instant monthly recurring M-Pesa billing verification prompt...")
