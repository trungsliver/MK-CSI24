import streamlit as st

st.title("Lesson 4: Streamlit App")
st.write("Đây là 1 dòng text")
st.success("Đây là 1 dòng text thông báo thành công")

st.set_page_config(
    page_title = "Streamlit App",
    page_icon = "✅",
    layout="centered",
)

# ===================== FORM =============================
st.title("Giới thiệu bản thân")
st.header("Personal Information")
st.write('Name: Bui Duc Trung')
st.write('Age: 2')
st.write('Work: MindX Technology School')
st.subheader("Hobbies")
st.markdown(f"""
    - Lập trình
    - Đọc sách
    - Chơi game
    - Nghe nhạc
""")

st.image(
    "https://static.ladipage.net/5cefbc1ed062e8345a24dfe8/ava-cover-01-1-20221114071946-wu7p1.jpg",
    width=300
)

st.code("""
print("Hello World")
""", language="python")

st.info("Đây là website được xây dựng hoàn toàn bằng Streamlit.")
st.success("Thành công")
st.error("Lỗi")

# ===================================================
st.title("📋 Form đăng ký")

name = st.text_input("Họ và tên")
age = st.number_input("Tuổi", 1, 100)
gender = st.radio(
    "Giới tính",
    ["Nam", "Nữ", "Khác"]
)
course = st.selectbox(
    "Khóa học",
    ["Python", "Java", "AI", "Web"]
)
skills = st.multiselect(
    "Kỹ năng",
    ["Python","Java","HTML","CSS","JavaScript"]
)
agree = st.checkbox("Tôi đồng ý với điều khoản")

if st.button("Đăng ký"):
    if agree:
        st.success("Đăng ký thành công!")

        st.write("### Thông tin")

        st.write(f"Tên: {name}")
        st.write(f"Tuổi: {age}")
        st.write(f"Giới tính: {gender}")
        st.write(f"Khóa học: {course}")
        st.write(f"Kỹ năng: {skills}")

    else:
        st.error("Bạn cần đồng ý điều khoản.")

# ==================== DASHBOARD ==========================