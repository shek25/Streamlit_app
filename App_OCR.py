import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
from ultralytics import YOLO
import cv2
from object_det_app import *
from Pedestrian import *
from speed_modular import *

def main_func_image(image, model, confidence):
    # Placeholder for image processing function for street name detection
    # Implement street name detection logic for images here
    # For example: process the image through the model and return detected text
    results = model(image)
    return "Detected street name"  # Replace with actual detection results

def main_func_ped_image(image, confidence, margin):
    # Placeholder for pedestrian detection on image
    # Implement pedestrian detection logic for images here
    # For example: process the image through the model and return pedestrian count
    results = model(image)
    return "Detected pedestrians"  # Replace with actual detection results

def alert_on_image(image, model, class_type, confidence):
    # Placeholder for alert logic on image
    # Implement alert logic here, such as detecting specific object classes
    results = model(image)
    for detection in results:
        if detection["class"] == class_type:  # This is a simplified example
            return f"Alert: {class_type} detected."
    return "No alerts"

im = Image.open('eye.png')

# Replace the relative path to your weight file
model_path = "best_Model_Roboflow.pt"

# Setting page layout
st.set_page_config(
    page_title="Third Eye Vision",  # Setting page title
    page_icon=im,  # Setting page icon
    # layout="wide",      # Setting layout to wide
    initial_sidebar_state="expanded"  # Expanding sidebar by default
)

# Creating sidebar
with st.sidebar:
    st.header("Image/Video Config")  # Adding header to sidebar
    # Adding file uploader to sidebar for selecting videos
    uploaded_file = st.file_uploader(Choose a video or image...", type=["mp4", "mov", "png"])
    temporary_location = None

    if uploaded_file is not None:
        #Get the file extension and construct the temporary filename accordingly
        file_extension = uploaded_file.name.split('.')[-1].lower()
        temporary_location = f"temp_file.{file_extension}"
        
        try:
            with open(temporary_location, 'wb') as out:
                out.write(uploaded_file.read())  # Read bytes into the temporary file
        except PermissionError:
            st.error("Permission denied to write the temporary file. Please check your permissions.")
        except Exception as e:
            st.error(f"Error saving uploaded file: {e}")
            
        # temporary_location = "testout_simple.mp4"
        # try:
        #     with open(temporary_location, 'wb') as out:  ## Open temporary file as bytes
        #         out.write(uploaded_file.read())  ## Read bytes into file
        # except PermissionError:
        #     st.error("Permission denied to write the temporary file. Please check your permissions.")
        # except Exception as e:
        #     st.error(f"Error saving uploaded file: {e}")

    det_type = st.radio(
        "Select Detection Type",
        ["Street_Name", "Pedestrian", "Alert"])
    
    if det_type == "Alert":
        class_type = st.radio(
            "Select Class Type",
            ['bicycle', 'car', 'motorcycle', 'bus', 'truck'])

        FPS = st.radio(
            "Select Duration of Seconds",
            [1,2,3])       


    if det_type == "Alert":

        # Model Options
        margin = float(st.slider(
            "Select Frame Margin", 0, 10, 10)) / 100
    if det_type == "Pedestrian":

        # Model Options
        margin = float(st.slider(
            "Select Frame Margin", 0, 25, 25)) / 100
        
    # Model Options
    confidence = float(st.slider(
        "Select Model Confidence", 25, 60, 35)) / 100

try:
    model = YOLO(model_path)
except Exception as ex:
    st.error(
        f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

# Creating a session state to store the uploaded video's state
if 'video_uploaded' not in st.session_state:
    st.session_state.video_uploaded = False

# Check if a new video has been uploaded
if uploaded_file is not None and not st.session_state.video_uploaded:
    st.session_state.video_uploaded = True
    st.experimental_rerun()

# Header Section
st.title("Third Eye Vision")
st.header("Upload the video or image file and click on the start detection")

selected = option_menu(
    menu_title=None,
    options=["HOME", "ABOUT", "CONTACT"],
    icons=["house", "briefcase", "person-lines-fill"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if selected == "HOME":
    st.header("Upload the video or image file and click on the start detection")

    # File processing
    if uploaded_file is not None:

        # Check file extension and process accordingly
        if file_extension in ['mov', 'mp4']:
            if st.sidebar.button('Start Detection'):
                vid_cap = cv2.VideoCapture(temporary_location)

                # Video detection based on type
                if det_type == "Street_Name":
                    detected_text = main_func(vid_cap, model, confidence)
                    st.write("Most common text:", detected_text)
                elif det_type == "Pedestrian":
                    main_func_ped(vid_cap, confidence, margin)
                elif det_type == "Alert":
                    alert_message = "Alert logic for video not yet implemented."  # Placeholder
                    st.write(alert_message)

        elif file_extension == 'png':
            if st.sidebar.button('Start Detection'):
                # If the image file is loaded, open it
                image = Image.open(temporary_location)

                # Image detection based on type
                if det_type == "Street_Name":
                    detected_text = main_func_image(image, model, confidence)
                    st.write("Detected text:", detected_text)
                elif det_type == "Pedestrian":
                    pedestrian_message = main_func_ped_image(image, confidence, margin)
                    st.write(pedestrian_message)
                elif det_type == "Alert":
                    alert_message = alert_on_image(image, model, class_type, confidence)
                    st.write(alert_message)

if selected == "ABOUT":

    st.header("🚀 Elevate Independence")
    st.write("""
        "Third Eye" leverages groundbreaking computer vision technology to empower blind and low-vision individuals. Navigate your surroundings with newfound confidence as "Third Eye" interprets the world in real-time.
        """)

    st.header("🌟 Features")
    st.markdown("""
    - **Object Recognition:** Instantly identify obstacles, signage, and objects.
    - **Text-to-Speech:** Hear descriptions of your surroundings, making navigation intuitive.
    - **Navigation Support:** Get real-time assistance to move around safely and efficiently.
    """)

    st.header("💡 How It Works")
    st.write("""
    By analyzing live video feeds, "Third Eye" detects and vocalizes the presence of obstacles and signage, converting visual information into audible guidance. This real-time support system is designed to promote greater inclusivity and accessibility, enhancing the daily lives of visually impaired individuals.
    """)

    # Interactive demo or more information about the technology could go here

    st.header("🌐 Join Our Community")
    st.write("""
    Become a part of the "Third Eye" community and contribute to a world where technology bridges the gap towards a more inclusive society. Share your experiences, suggest improvements, and help us make "Third Eye" better for everyone.
    """)

if selected == "CONTACT":
    # Add a Contact Us section
    st.header("📬 Contact Us")
    st.write(
        "We'd love to hear from you! Whether you have a question, feedback, or just want to say hello, please don't hesitate to reach out. Fill out the form below or email us directly at contact-thirdeye@gmail.com.")

    with st.form("contact_form"):
        name = st.text_input("Name", placeholder="Your Name")
        email = st.text_input("Email", placeholder="Your Email Address")
        message = st.text_area("Message", placeholder="Your Message Here")

        submit_button = st.form_submit_button("Send Message")

        if submit_button:
            # Here you would include the logic to handle the form data, such as sending an email
            # This is a placeholder to simulate form submission
            st.success(f"Thank you, {name}, for reaching out! We'll get back to you soon.")
