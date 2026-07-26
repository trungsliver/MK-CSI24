import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

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

name1 = st.text_input("Họ và tên")
age1 = st.number_input("Tuổi của bạn", 1, 100)
gender1 = st.radio(
    "Giới tính",
    ["Nam", "Nữ", "Khác"]
)
course1 = st.selectbox(
    "Khóa học",
    ["Python", "Java", "AI", "Web"]
)
skills1 = st.multiselect(
    "Kỹ năng",
    ["Python","Java","HTML","CSS","JavaScript"]
)
agree1 = st.checkbox("Tôi đồng ý với điều khoản")

if st.button("Đăng ký ngay"):
    if agree1:
        st.success("Đăng ký thành công!")

        st.write("### Thông tin")

        st.write(f"Tên: {name1}")
        st.write(f"Tuổi: {age1}")
        st.write(f"Giới tính: {gender1}")
        st.write(f"Khóa học: {course1}")
        st.write(f"Kỹ năng: {skills1}")

    else:
        st.error("Bạn cần đồng ý điều khoản.")

# ==================== DASHBOARD ==========================
st.title("📊 Dashboard")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Doanh thu", "150 triệu", "+12%")
with col2:
    st.metric("Khách hàng", "540", "+25")
with col3:
    st.metric("Đơn hàng", "320", "-8")
st.divider()
data = pd.DataFrame({
    "Ngày": range(1, 11),
    "Doanh thu": np.random.randint(50, 200, 10)
})
st.line_chart(
    data.set_index("Ngày")
)
st.dataframe(data)

# ================== Upload CSV và xem dữ liệu ==================
st.title("📂 Đọc file CSV")

uploaded_file = st.file_uploader(
    "Chọn file CSV",
    type=["csv"]
)
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("Đọc dữ liệu thành công!")
    st.dataframe(df)
    st.write("Số dòng:", df.shape[0])
    st.write("Số cột:", df.shape[1])
    st.write(df.describe())

# ================= Upload ảnh =======================
st.title("Upload ảnh")

uploaded_image = st.file_uploader(
    "Chọn ảnh",
    type=["jpg", "png", "jpeg"]
)

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(
        image,
        caption="Ảnh đã upload",
        use_container_width=True
    )
    st.success("Hiển thị thành công.")

# ================= SAMPLES ===================
st.title("🎓 Student Manager")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Trang chủ",
        "Thêm sinh viên",
        "Danh sách"
    ]
)

if "students" not in st.session_state:
    st.session_state.students = []

if menu == "Trang chủ":

    st.header("Trang chủ")

    st.write(
        "Ứng dụng quản lý sinh viên bằng Streamlit."
    )

elif menu == "Thêm sinh viên":

    st.header("Thêm sinh viên")

    name = st.text_input("Tên")

    age = st.number_input(
        "Tuổi",
        1,
        100
    )

    major = st.selectbox(
        "Ngành",
        [
            "CNTT",
            "AI",
            "Data Science",
            "Cyber Security"
        ]
    )

    if st.button("Lưu"):

        st.session_state.students.append({
            "Tên": name,
            "Tuổi": age,
            "Ngành": major
        })

        st.success("Đã thêm.")

elif menu == "Danh sách":

    st.header("Danh sách sinh viên")

    if st.session_state.students:

        df = pd.DataFrame(
            st.session_state.students
        )

        st.dataframe(df)

    else:

        st.warning("Chưa có dữ liệu.")