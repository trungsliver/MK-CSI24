# Import thư viện xử lý ảnh từ Pillow
from PIL import Image
# Import thư viện tính toán ma trận và mảng
import numpy as np
# Import thư viện Streamlit để tạo giao diện web
import streamlit as st
# Import hàm load_model từ TensorFlow/Keras để tải mô hình
from tensorflow.keras.saving import load_model
# Import các hàm xử lý ảnh từ TensorFlow/Keras
from tensorflow.keras.preprocessing import image

# Danh sách nhãn chữ cái và các ký hiệu đặc biệt trong hệ thống ASL
labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
          'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
          'U', 'V', 'W', 'X', 'Y', 'Z', 'nothing', 'space', 'del']


# Hàm tiền xử lý ảnh trước khi đưa vào mô hình
def preprocess_PIL(pil_img, input_size=(128, 128)):
    # Chuyển ảnh sang định dạng RGB để đảm bảo tương thích
    pil_img = pil_img.convert("RGB")

    # Thay đổi kích thước ảnh về đúng kích thước mà mô hình yêu cầu
    img = pil_img.resize(input_size)

    # Chuyển ảnh thành mảng số để mô hình có thể xử lý
    img_array = image.img_to_array(img)

    # Thêm một chiều batch để tạo thành dạng [1, height, width, channels]
    img_array = np.expand_dims(img_array, axis=0)  # Thêm n = 1 để batch_size = 1

    # Tạo trình sinh dữ liệu ảnh với các phép tiền xử lý tương tự như lúc huấn luyện
    test_datagen = image.ImageDataGenerator(  # Bắt buộc áp các phương pháp tiền xử lý như tập train
        samplewise_center=True,
        samplewise_std_normalization=True
    )

    # Chuyển mảng ảnh thành generator để mô hình đọc được
    img_generator = test_datagen.flow(img_array, batch_size=1)

    # Trả về generator đã được tiền xử lý
    return img_generator


# Hàm chính chạy ứng dụng
def main():
    # Tải mô hình một lần và cache lại để tăng tốc
    @st.cache_resource
    def load_asl_model(model_path='model.keras'):
        try:
            # Tải mô hình từ file .keras
            model = load_model(model_path)
            return model
        except Exception as e:
            # Hiển thị thông báo lỗi nếu không tải được mô hình
            st.error("Error loading model")
            return None

    # Gọi hàm tải mô hình với file mô hình đã cho
    model = load_asl_model("model_epoch_04.keras")

    # Hiển thị tiêu đề ứng dụng
    st.title("American ASL Classifiaction App")

    # Cho người dùng chọn cách nhập dữ liệu
    option = st.selectbox("Choose input type", ("Upload Image", "Use Webcam"))

    # Nếu người dùng chọn tải ảnh từ máy
    if option == "Upload Image":
        # Tạo nút chọn file ảnh
        uloaded_file = st.file_uploader("Choose an image ...", type=["jpg", "jpeg", "png"])

        # Nếu người dùng đã chọn ảnh
        if uloaded_file is not None:
            # Mở ảnh từ file đã upload
            image = Image.open(uloaded_file)

            # Hiển thị ảnh lên giao diện
            st.image(image, caption="Uploaded Image", use_column_width=True)

            # Khi người dùng nhấn nút phân loại
            if st.button("Classify"):
                # Tiền xử lý ảnh trước khi dự đoán
                img_gen = preprocess_PIL(image)

                # Dự đoán nhãn bằng mô hình
                predictions = model.predict(next(img_gen))

                # Lấy chỉ số nhãn có xác suất cao nhất
                prediction_idx = np.argmax(predictions)

                # Chuyển chỉ số thành nhãn tương ứng
                predicted_label = labels[prediction_idx]

                # Lấy độ tin cậy của dự đoán
                confidence = np.max(predictions)

                # Hiển thị kết quả dự đoán lên giao diện
                st.write(f"**Prediction:** {predicted_label} with {confidence * 100:.2f}% confidence.")

    # Nếu người dùng chọn dùng webcam
    elif option == "Use Webcam":
        # Hiển thị thông báo cho chế độ webcam
        st.write("Realtime ASL detected using Webcam")


# Chạy hàm main khi file được thực thi trực tiếp
if __name__ == "__main__":
    main()


