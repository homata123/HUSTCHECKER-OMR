from omr_main import result
import cv2
import streamlit  as st
import PIL.Image
import numpy as np
from PIL import Image

correct_answer = ["a", "b", "b", "c", "a", "b", "a", "b", "a", "c", "b", "c", "a", "b", "d", "d", "d", "a", "b", "c"
                  ]

# st.markdown('<style>body{background-color:coral;}</style>',unsafe_allow_html=True)

st.markdown('<center><h1>Phần mềm chấm điểm tự động HUSTGRADE <h1></center>', unsafe_allow_html=True)

ch = st.selectbox(
    "Choice",
    [
        "Home",
        "HUSTGRADE CHECKER",
    ],
    key="main_select",
)

if ch == "Home":
    st.markdown('<center><h3>HOME<h3></center>', unsafe_allow_html=True)

    a = '<p style="text-align: justify;font-size:20px;">HUSTGRADE Checker APP is an APP that will help the teachers get the results of'
    a += 'answer sheet of the students. This will help the teacher to grade the students faster and provide faster results.'
    a += ' </p><br>'
    st.markdown(a, unsafe_allow_html=True)

    st.markdown('<center><h3>FEATURES<h3></center>', unsafe_allow_html=True)
    a = "<p style='text-align: justify;font-size:20px;'><ul><li style='text-align: justify;font-size:20px;'>Interactive Dashboard to Generate HUSTGRADE Scores Easily</li>"
    a += "<li style='text-align: justify;font-size:20px;'>The images should be in jpeg,png or jpeg format</li>"
    a += "<li style='text-align: justify;font-size:20px;'>The HUSTGRADE Layout is restricted to the Sample displayed</li><br>"
    st.markdown(a, unsafe_allow_html=True)

    st.markdown('<center><h3>SAMPLE IMAGES<h3></center>', unsafe_allow_html=True)
    image = Image.open('data/test1.jpeg')
    st.image(image, use_column_width=True)

elif ch == "HUSTGRADE CHECKER":
    st.markdown('<center><h3>HUST-CHECKER<h3></center>', unsafe_allow_html=True)
    uploaded_image = st.file_uploader("Upload an OMR Sheet", type=["png", "jpeg", "jpg"])

    if uploaded_image is not None:
        image = PIL.Image.open(uploaded_image).convert("RGB")
        img_array = np.array(image)
        enrollment_no,test_id,answer_list = result(img_array)
        right = 0
        wrong = 0
        unattempted = 0
        for i in range(20):
            if answer_list[i] == correct_answer[i]:
                right += 1
            elif answer_list[i] == " ":
                unattempted += 1
            else:
                wrong += 1

        st.success("Correctly Marked  : " + str(right))
        st.error("Wrongly Marked  : " + str(wrong))
        st.warning("Not Marked  : " + str(unattempted))

