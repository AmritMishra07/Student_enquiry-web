import streamlit as st
from fpdf import FPDF
import time
import uuid
from datetime import date

st.set_page_config(page_title="Student Enquiry Form", page_icon="📄", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = 1

def next_page():
    st.session_state.page += 1

def prev_page():
    st.session_state.page -= 1

if st.session_state.page == 1:
    st.title("Student Enquiry Form")
    st.subheader("Step 1 — Personal Details")

    name = st.text_input("Full Name")
    if name == "":
        st.error("Full name cannot be empty")

    dob = st.date_input("Date of Birth", min_value=date(1800, 1, 1), max_value=date.today())


    gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"])
    if gender == "Select":
        st.error("Please select a valid gender")

    mobile = st.text_input("Mobile Number")
    if mobile and (not mobile.isdigit() or len(mobile) != 10):
        st.error("Mobile number must be 10 digits")

    email = st.text_input("Email Address")
    if email and "@gmail.com" not in email:
        st.error("Email must contain @gmail.com")

    st.subheader("Address Details")

    address = st.text_area("Full Address")
    if address == "":
        st.error("Address cannot be empty")

    city = st.text_input("City")
    if city == "":
        st.error("City cannot be empty")

    state = st.text_input("State")
    if state == "":
        st.error("State cannot be empty")

    pincode = st.text_input("Pincode")
    if pincode and (not pincode.isdigit() or len(pincode) != 6):
        st.error("Pincode must be 6 digits")

    if st.button("Next"):
        if (name == "" or gender == "Select" or mobile == "" or len(mobile) != 10 or
            email == "" or "@gmail.com" not in email or address == "" or
            city == "" or state == "" or pincode == "" or len(pincode) != 6):
            st.error("Please correct errors before continuing")
        else:
            st.session_state.update({
                "name": name,
                "dob": dob,
                "gender": gender,
                "mobile": mobile,
                "email": email,
                "address": address,
                "city": city,
                "state": state,
                "pincode": pincode
            })
            next_page()

elif st.session_state.page == 2:
    st.title("Academic and Course Info")
    st.subheader("Step 2 — Academic Details")

    qualification = st.selectbox("Qualification",
                                ["Select", "9", "10", "11", "12", "Graduate", "Post Graduate"])

    school = st.text_input("School or College Name")
    percentage = st.text_input("Marks or Percentage")

    st.subheader("Course Interest")

    course = st.selectbox("Interested Course",
                          ["Select", "BCA", "MCA", "Web Development", "Data Science", "Python Programming", "Other"])

    mode = st.selectbox("Mode of Study", ["Select", "Online", "Offline"])
    timing = st.selectbox("Batch Timing", ["Select", "Morning", "Afternoon", "Evening"])
    reason = st.text_area("Reason for Joining")

    col1, col2 = st.columns(2)

    if col1.button("Back"):
        prev_page()

    if col2.button("Preview"):
        if (qualification == "Select" or course == "Select" or timing == "Select" or
            school == "" or percentage == "" or mode == "Select" or reason == ""):
            st.error("Please fill all required fields properly")
        else:
            st.session_state.update({
                "qualification": qualification,
                "school": school,
                "percentage": percentage,
                "course": course,
                "mode": mode,
                "timing": timing,
                "reason": reason,
                "enquiry_id": "ENQ-" + str(uuid.uuid4())[:8].upper()
            })
            next_page()

elif st.session_state.page == 3:
    st.title("Final Preview")
    st.write("Please check all details before submitting.")

    st.subheader(f"Enquiry ID: {st.session_state.enquiry_id}")

    st.write("### Personal Details")
    st.write(f"Name: {st.session_state.name}")
    st.write(f"DOB: {st.session_state.dob}")
    st.write(f"Gender: {st.session_state.gender}")
    st.write(f"Mobile: {st.session_state.mobile}")
    st.write(f"Email: {st.session_state.email}")

    st.write("### Address")
    st.write(f"{st.session_state.address}, {st.session_state.city}, {st.session_state.state} - {st.session_state.pincode}")

    st.write("### Academic Details")
    st.write(f"Qualification: {st.session_state.qualification}")
    st.write(f"School/College: {st.session_state.school}")
    st.write(f"Percentage: {st.session_state.percentage}")

    st.write("### Course Information")
    st.write(f"Course: {st.session_state.course}")
    st.write(f"Mode: {st.session_state.mode}")
    st.write(f"Batch Timing: {st.session_state.timing}")
    st.write(f"Reason: {st.session_state.reason}")

    col1, col2 = st.columns(2)

    if col1.button("Back"):
        prev_page()

    if col2.button("Submit & Download PDF"):

        with st.spinner("Generating PDF..."):
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)

        file_name = f"Enquiry_{st.session_state.enquiry_id}.pdf"

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt=f"Enquiry ID: {st.session_state.enquiry_id}", ln=True)

        data = [
            ("Full Name", st.session_state.name),
            ("Date of Birth", str(st.session_state.dob)),
            ("Gender", st.session_state.gender),
            ("Mobile", st.session_state.mobile),
            ("Email", st.session_state.email),
            ("Address", st.session_state.address),
            ("City", st.session_state.city),
            ("State", st.session_state.state),
            ("Pincode", st.session_state.pincode),
            ("Qualification", st.session_state.qualification),
            ("School/College", st.session_state.school),
            ("Percentage", st.session_state.percentage),
            ("Course Interested", st.session_state.course),
            ("Mode", st.session_state.mode),
            ("Batch Timing", st.session_state.timing),
            ("Reason", st.session_state.reason),
        ]

        for label, value in data:
            pdf.cell(0, 8, txt=f"{label}: {value}", ln=True)

        pdf.output(file_name)

        with open(file_name, "rb") as f:
            st.download_button("Download PDF", f, file_name, mime="application/pdf")

