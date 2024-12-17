import streamlit as st
from PIL import Image, ImageFilter, ImageOps
from io import BytesIO

# Function to process the image based on user input
def process_image(image, blur, contrast, emboss, contour, flipx, flipy):
    # Apply Gaussian blur
    if blur > 0:
        image = image.filter(ImageFilter.GaussianBlur(blur))
    
    # Apply contrast (Unsharp mask)
    if contrast > 0:
        image = image.filter(ImageFilter.UnsharpMask(contrast))
    
    # Apply emboss filter
    if emboss:
        image = image.filter(ImageFilter.EMBOSS)
    
    # Apply contour filter
    if contour:
        image = image.filter(ImageFilter.CONTOUR)
    
    # Flip horizontally
    if flipx:
        image = ImageOps.mirror(image)
    
    # Flip vertically
    if flipy:
        image = ImageOps.flip(image)
    
    return image

# Streamlit UI
st.title("Image Editor")

# File uploader to upload image
uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Load the original image
    original_image = Image.open(uploaded_file)
    
    # Display the original image
    st.image(original_image, caption="Original Image", use_column_width=True)
    
    st.sidebar.header("Edit Controls")
    
    # Blur and Contrast sliders
    blur = st.sidebar.slider("Blur", 0, 10, 0)
    contrast = st.sidebar.slider("Contrast", 0, 10, 0)
    
    # Checkboxes for filters
    emboss = st.sidebar.checkbox("Emboss")
    contour = st.sidebar.checkbox("Contour")
    flipx = st.sidebar.checkbox("Flip Horizontally")
    flipy = st.sidebar.checkbox("Flip Vertically")
    
    # Process the image with the user inputs
    edited_image = process_image(original_image, blur, contrast, emboss, contour, flipx, flipy)
    
    # Display the edited image
    st.image(edited_image, caption="Edited Image", use_column_width=True)
    
    # Button to download the edited image
    buf = BytesIO()
    edited_image.save(buf, format="PNG")
    st.download_button("Download Edited Image", buf.getvalue(), file_name="edited_image.png", mime="image/png")
