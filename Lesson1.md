# 1. Artificial Intelligence (AI)
- Trí tuệ nhân tạo: chat gpt, gemini, face recognition, autopilot,..
- Trí tuệ là khả năng:
 nhận thức -> suy luận -> lưu trữ -> áp dụng
- Ví dụ 1: dạy một em bé nhận biết con mèo
    + Ban đầu, chỉ vào nhiều bức ảnh và nói:
        . Đây là mèo.
        . Đây không phải mèo.
    + Sau một thời gian, em bé có thể tự nhận ra một con mèo mới mà chưa từng nhìn thấy
=> AI là lĩnh vực giúp máy tính có khả năng học cách suy nghĩ và đưa ra quyết định giống con người, thay vì chỉ làm đúng những gì được lập trình sẵn.
- Ví dụ 2: Khi mở điện thoại bằng Face ID
    + Điện thoại sẽ:
        . Nhìn khuôn mặt
        . So sánh với dữ liệu đã lưu
        . Nếu khớp → mở khóa
    + Không cần lập trình: "Nếu mắt cách nhau 5cm thì mở"
    + AI sẽ tự học các đặc điểm khuôn mặt
- Phân loại AI:
    + Khả năng: 
        . AI hẹp: 1 tác vụ cụ thể
        . AI rộng: nhiều lĩnh vực
    + Chức năng:
        . AI dự đoán: tìm ra xu hướng, đặc điểm chung của dữ liệu trong quá khứ để đưa ra quyết định
        . AI tạo sinh: sáng tạo văn bản, hình ảnh, âm thanh

# 2. Machine Learning
- Là 1 nhánh của AI, tự tìm quy luật từ dữ liệu 
- Ví dụ 1: Phân loại trái cây
    + Lập trình thông thường: 
        . Nếu màu đỏ -> Táo
        . Nếu màu vàng -> Chuối
    + Nhưng nếu có: táo xanh, chuối xanh, cam đỏ thì sẽ rất phức tạp.
    + Machine Learning: cho máy tính nhiều ảnh trái cây, máy sẽ tự tìm quy luật
- Ví dụ 2: Netflix gợi ý phim
    + Máy không biết bạn xem phim gì
    + Quan sát: xem phim nào, bao lâu, bỏ dở hay xem hết
    + Dự đoán phim tiếp theo

# 3. Deep Learning
- Sử dụng nhiều tầng Neural Network
- Ví dụ: Nhìn 1 chiếc xe, con người sẽ k nhận ra chiếc xe ngay lập tức mà xử lý từng bước
    + Có các đường thẳng, có các đường tròn
    + Có 4 bánh xe
    + Có cửa
    => Đây là oto
- ví dụ:FB tự gắn thẻ tên trong ảnh
    + Không tìn toàn bộ mặt
    + Nhận biết: mắt, mũi, miệng, khoảng cách các bộ phận => Kết luận

# 4. Neural Network (Artificial Neural Network)
- Mạng neuron nhân tạo: Mô phỏng hoạt động của não người
- Đơn vị nhỏ nhất của nó được gọi là Perceptron, liên kết với nhau thành từng lớp (layer)
- Mỗi nơ ron nhận tín hiệu đầu vào (input) từ nơ ron khác, tính toán và trả kết quả (output) cho các nơ ron tiếp theo.
- Một Perceptron nhận các đầu vào (Inputs), nhân chúng với các trọng số (Weights), cộng thêm một sai số (Bias), và đi qua một hàm kích hoạt (Activation Function) để cho ra kết quả (Output)
y = ax + b
- Hàm số: ánh xạ từ x đầu vào -> giá trị y
    + y = f(x)
    + Hàm tuyến tính (Linear function): 
y = ax + b
y = w1x1 + w2x2 + ... + w0
    + Hàm phi tuyến (non-linear function):
0(x) = 1 / (1 + e^(-x)) - hàm sigmoid
activation function
- Neuron: chính là các hàm số bên trên với nhiều giá trị x truyền vào
- Layer: tập hợp nhiều neuron nhận cùng x nhưng trọng số khác nhau => y khác nhau
- Artificial Neural Network: ảnh
Ví dụ: Quyết định đi xem phim với người yêu (y)
- Các yếu tố ảnh hưởng đến quyết định đi xem phim (inputs)
	+ x1: Thời tiết (1 = thời tiết đẹp, 0 = thời tiết xấu)
	+ x2: Tài chính (1 = nhiều tiền, 0 = hết tiền)
	+ x3: Sức khỏe (1 = khỏe, 0 = ốm)
	+ x4: Rạp có phim mình thích không (1 = có, 0 = không)
- Trọng số (độ quan trọng của các yếu tố) - weights:
	+ w1: 2 (Thời tiết không quá quan trọng)
	+ w2: 8	(tình hình tài chính rất quan trọng)
	+ w3: 5 (sức khỏe khá quan trọng)
	+ w4: 1 (phim không quan trọng lắm)
- Sai số (bias): số mặc định
	+ Ai cũng có 1 độ lười tự nhiên, bạn rất lười
	+ w0 = -15
- Phương trình:
	y = w1x1 + w2x2 + w3x3 + w4x4 + w0
MA: 	y = 2*0 + 8*0.5 + 5*0.5 + 1*0 - 10 = -3.5 < 0 => k đi
LK: 	y = 4*1 + 8*0.6 + 7*1 + 5*0 - 11 = 4.8 > 0 => đi 
DA: 	y = 5*1 + 10*1 + 7*1 + 5*1 - 20 = 7 > 0 => đi
TL: 	y = 1*1 + 5*1 + 8*1 + 9*1 - 10 = 13 > 0 => đi
- Giải thích:
	+ Khi y > 0: hàm kích hoạt bật đèn xanh => quyết định đi xem phim
	+ Khi y < 0: hàm kích hotaj đèn đỏ => quyết định không đi xem phim

https://playground.tensorflow.org/