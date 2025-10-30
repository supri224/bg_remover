# app.py
import streamlit as st
from PIL import Image
import io
from remove_bg import remove_background
from config import *

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title=APP_TITLE,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Monk - Background Remover\nPowered by AI using U²-Net"
    }
)

# ============================================
# CUSTOM CSS STYLING
# ============================================
st.markdown(f"""
    <style>
        :root {{
            --primary-color: {PRIMARY_COLOR};
            --secondary-color: {SECONDARY_COLOR};
            --accent-color: {ACCENT_COLOR};
        }}
        
        /* Main background */
        .main {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        
        /* Header styling */
        .header-container {{
            text-align: center;
            margin-bottom: 40px;
        }}
        
        /* Logo styling */
        .logo-container {{
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }}
        
        /* Title */
        .title {{
            font-size: 48px;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 20px 0;
        }}
        
        /* Subtitle */
        .subtitle {{
            font-size: 18px;
            color: #666;
            margin-bottom: 30px;
        }}
        
        /* Card styling */
        .card {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin: 20px 0;
        }}
        
        /* Button styling */
        .stButton > button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border-radius: 10px !important;
            padding: 12px 30px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            border: none !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4) !important;
        }}
        
        /* File uploader */
        .stFileUploader {{
            border-radius: 10px !important;
        }}
        
        /* Success message */
        .success-box {{
            background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }}
        
        /* Info box */
        .info-box {{
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }}
        
        /* Spinner text */
        .stSpinner {{
            color: #667eea !important;
        }}
        
        /* Section header */
        .section-header {{
            font-size: 28px;
            font-weight: 700;
            margin: 30px 0 20px 0;
            color: #333;
        }}
    </style>
""", unsafe_allow_html=True)

# ============================================
# HEADER SECTION
# ============================================
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
        <div class="header-container">
            <div class="title">🧘 Monk</div>
            <div class="subtitle">AI-Powered Background Remover</div>
        </div>
    """, unsafe_allow_html=True)

# ============================================
# MAIN CONTENT
# ============================================
st.markdown("""
    <div class="info-box">
        <h3>✨ Welcome to Monk</h3>
        <p>Upload any image and remove its background instantly using advanced AI technology. 
        Download your transparent PNG in seconds!</p>
    </div>
""", unsafe_allow_html=True)

# ============================================
# FILE UPLOADER SECTION
# ============================================
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("<div class='section-header'>📸 Upload Image</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Choose an image",
        type=SUPPORTED_FORMATS,
        help="Supported formats: PNG, JPG, JPEG (Max 50MB)"
    )

# ============================================
# IMAGE PROCESSING
# ============================================
if uploaded_file:
    try:
        # Read and display original image
        image = Image.open(uploaded_file).convert("RGB")
        
        # Create two columns for before/after
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='section-header'>📷 Original Image</div>", unsafe_allow_html=True)
            st.image(image, use_column_width=True, caption="Your uploaded image")
        
        # Process image
        with col2:
            st.markdown("<div class='section-header'>✨ Processed Image</div>", unsafe_allow_html=True)
            
            with st.spinner("🔄 Removing background... (First time may take 1-2 minutes)"):
                result = remove_background(image)
            
            st.image(result, use_column_width=True, caption="Background removed")
        
        # ============================================
        # DOWNLOAD SECTION
        # ============================================
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Prepare download
            buf = io.BytesIO()
            result.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.markdown("""
                <div class="success-box">
                    <h3>✅ Success!</h3>
                    <p>Your background has been removed. Click below to download your transparent PNG!</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.download_button(
                label="⬇️ Download Transparent PNG",
                data=byte_im,
                file_name=f"monk_removed_bg_{uploaded_file.name.split('.')[0]}.png",
                mime="image/png",
                use_container_width=True
            )
    
    except Exception as e:
        st.error(f"❌ Error processing image: {str(e)}")
        st.info("Try uploading a different image or check if the file is corrupted.")

else:
    st.markdown("""
        <div class="info-box">
            <h3>🚀 Get Started</h3>
            <p>Click the 'Browse files' button above to upload an image. Monk will instantly remove 
            the background and create a transparent PNG file for you to download!</p>
        </div>
    """, unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
    <div style="text-align: center; margin-top: 40px; color: #666;">
        <p><strong>Monk Background Remover</strong></p>
        <p>Powered by U²-Net AI • Open Source • Free to Use</p>
        <p style="font-size: 12px;">© 2025 Monk. All rights reserved.</p>
    </div>
""", unsafe_allow_html=True)
