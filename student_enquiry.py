import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import time
import uuid

st.set_page_config(page_title="Student Enquiry Form", page_icon="📄", layout="centered")

# -------------------- SESSION STATE --------------------
if "page" not in st.session_state:
    st.session_state.page = 1

# Buttons
def next_page():
    st.session_state.page += 1

def prev_page():
    st.session_state.page -= 1


# ============ CUSTOM CSS for Clean UI =============
st.markdown("""
<style>
    .card {
        padding: 20px;
        background: #FFFFFF;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)


# -------------------- PAGE 1 --------------------
if st.session_state.page == 1:
    st.title("📄 Student Enquiry Form")
    st.subheader("Step 1 — Personal Details")

    name = st.text_input("Full Name *")
    dob = st.date_input("Date of Birth *")
    gender = st.selectbox("Gender *", ["Select", "Male", "Female", "Other"])
    mobile = st.text_input("Mobile Number *")
    email = st.text_input("Email Address *")

    st.subheader("Address Details")
    address = st.text_area("Full Address *")
    city = st.text_input("City *")
    state = st.text_input("State *")
    pincode = st.text_input("Pincode *")

    # ---------- Next Button with Validation ----------
    if st.button("Next ➡️"):
        if (not name or gender == "Select" or not mobile or not email or
            not address or not city or not state or not pincode):
            st.error("⚠️ Please fill all * required fields")
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



# -------------------- PAGE 2 --------------------
elif st.session_state.page == 2:
    st.title("📘 Academic & Course Info")
    st.subheader("Step 2 — Academic Details")

    qualification = st.selectbox("Qualification *",
                                 ["Select", "9", "10", "11", "12", "Graduate", "Post Graduate"])
    school = st.text_input("School / College Name *")
    percentage = st.text_input("Marks / Percentage *")

    st.subheader("Course Interest")
    course = st.selectbox("Interested Course *",
                          ["Select", "BCA", "MCA", "Web Development", "Data Science", "Python Programming", "Other"])
    mode = st.selectbox("Mode of Study *", ["Select", "Online", "Offline"])
    timing = st.selectbox("Batch Timing *", ["Select", "Morning", "Afternoon", "Evening"])
    reason = st.text_area("Reason for Joining *")

    col1, col2 = st.columns(2)

    if col1.button("⬅️ Back"):
        prev_page()

    if col2.button("Preview ➡️"):
        if (qualification == "Select" or course == "Select" or timing == "Select"
            or not school or not percentage or mode == "Select" or not reason):
            st.error("⚠️ Please fill all * required fields")
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



# -------------------- PAGE 3 (PREVIEW) --------------------
elif st.session_state.page == 3:
    st.title("🧾 Final Preview")
    st.write("Your enquiry details are ready to submit!")

    # ---------- PREVIEW CARD ----------
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader(f"Enquiry ID: 🆔 {st.session_state.enquiry_id}")

    st.write("### Personal Details")
    st.write(f"**Name:** {st.session_state.name}")
    st.write(f"**DOB:** {st.session_state.dob}")
    st.write(f"**Gender:** {st.session_state.gender}")
    st.write(f"**Mobile:** {st.session_state.mobile}")
    st.write(f"**Email:** {st.session_state.email}")

    st.write("### Address")
    st.write(f"{st.session_state.address}, {st.session_state.city}, "
             f"{st.session_state.state} - {st.session_state.pincode}")

    st.write("### Academic Details")
    st.write(f"**Qualification:** {st.session_state.qualification}")
    st.write(f"**School/College:** {st.session_state.school}")
    st.write(f"**Percentage:** {st.session_state.percentage}")

    st.write("### Course Information")
    st.write(f"**Course Interested:** {st.session_state.course}")
    st.write(f"**Mode:** {st.session_state.mode}")
    st.write(f"**Timing:** {st.session_state.timing}")
    st.write(f"**Reason:** {st.session_state.reason}")

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("---")

    # ---------- Buttons ----------
    col1, col2 = st.columns(2)

    if col1.button("⬅️ Back"):
        prev_page()

    # ---------- PDF GENERATION ----------
    if col2.button("Submit & Download PDF"):
        with st.spinner("Submitting..."):
            bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                bar.progress(i + 1)

        file_name = f"Enquiry_{st.session_state.enquiry_id}.pdf"

        # Create PDF
        c = canvas.Canvas(file_name, pagesize=letter)
        c.setFont("Helvetica", 12)

        y = 750
        c.drawString(50, y, f"Enquiry ID: {st.session_state.enquiry_id}")
        y -= 30

        info = [
            ("Full Name", st.session_state.name),
            ("DOB", str(st.session_state.dob)),
            ("Gender", st.session_state.gender),
            ("Mobile", st.session_state.mobile),
            ("Email", st.session_state.email),
            ("Address", st.session_state.address),
            ("City", st.session_state.city),
            ("State", st.session_state.state),
            ("Pincode", st.session_state.pincode),
            ("Qualification", st.session_state.qualification),
            ("School", st.session_state.school),
            ("Percentage", st.session_state.percentage),
            ("Course Interested", st.session_state.course),
            ("Mode of Study", st.session_state.mode),
            ("Batch Timing", st.session_state.timing),
            ("Reason", st.session_state.reason),
        ]

        for label, value in info:
            c.drawString(50, y, f"{label}: {value}")
            y -= 20

        c.save()

        with open(file_name, "rb") as f:
            st.download_button("⬇️ Download PDF", f, file_name, mime="application/pdf")

