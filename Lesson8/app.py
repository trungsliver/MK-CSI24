import os, json
import pandas as pd

import google.generativeai as genai 
from dotenv import load_dotenv
import streamlit as st

# Set up AI
    # Load key API từ file .env
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=google_api_key)

# Load config bạn đầu của LLM
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
    functions = config.get("function", "Giới thiệu về lớp MK-CSI24")
    initial_bot_message = config.get("initial_bot_message", "Chào bạn, tôi là CSI24_Bot. Tôi có thể giúp bạn điều gì?")

# Load data từ file CSV
menu_df = pd.read_csv("menu.csv", index_col=[0])

# Tạo LLM 
model = genai.GenerativeModel("gemini-3.5-flash",
                               system_instruction= f"""Bạn tên là CSI24 Chatbot, bạn có nhiệm vụ giải đáp thông tin cho học sinh.
                               Các chức năng bạn hỗ trợ:
                               1. Giới thiệu lớp CSI24: Tên đầy đủ là MK-C4K-CSI24, tại cơ sở Minh Khai - Hà Nội
                               2. Liệt kê thành viên trong lớp: Tuấn Linh, Thu Hương, Minh Anh, Lâm Khánh, Duy Anh
                               3. Giới thiệu menu đồ ăn của lớp, gồm các món: {', '.join(menu_df['name'].to_list())}.
                               Ngoài các chức năng trên, bạn không hỗ trợ chức năng nào khác. Đối với các câu hỏi ngoài chức năng mà bạn hỗ trợ,
                               trả lời bằng 'Tôi đang không hỗ trợ chức năng này. Xin liên hệ nhân viên nhà hàng qua hotline 1900 561 252 để được trợ giúp.'
                               Hãy có thái độ thân thiện và lịch sự khi nói chuyện với khách hàng, vì khách hàng là thượng đế""")

# Hàm trò chuyện của chatbot
def csi24_chatbot():
    st.title("CSI24 Chatbot")
     # tin nhắn mặc định
    st.write(initial_bot_message)
    # Tin nhắn gợi ý chức năng
    st.write("""Các chức năng bạn có thể hỏi tôi:
    1. Giới thiệu về lớp MK-CSI24
    2. Giới thiệu menu của lớp
    """)

    # Nếu chưa có lịch sử trò chuyện
    if 'conversation_log' not in st.session_state:
        st.session_state.conversation_log = [
            {"role": "assistant", "content": initial_bot_message}
        ]

     # Nếu đã có lịch sử trò chuyện, hiển thị lịch sử ra màn hình
    for message in st.session_state.conversation_log:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.write(message["content"])

    # Khi người dùng nhập prompt
    if prompt := st.chat_input("Nhập yêu cầu của bạn tại đây..."):
        # Hiển thị prompt của người dùng ra màn hình
        with st.chat_message("user"):
            st.write(prompt)
        # Thêm vào log
        st.session_state.conversation_log.append({"role": "user", "content": prompt})

        # LLM tạo câu trả lời
        response = model.generate_content(prompt)
        bot_reply = response.text

        # Kiểm tra xem prompt có đề cập menu không
        if "menu" in prompt.lower() or "món" in prompt.lower():
            bot_reply = '\n\n'.join([f"**{row['name']}**: {row['description']}" for idx, row in menu_df.iterrows()])
        else:
            response = model.generate_content(prompt)
            bot_reply = response.text

        # Hiển thị câu trả lời từ LLM
        with st.chat_message("assistant"):
            st.write(bot_reply)
        # và thêm vào log
        st.session_state.conversation_log.append({"role": "assistant", "content": bot_reply})

    #### Chạy chương trình ###
if __name__ == "__main__":
    csi24_chatbot()

# Câu lệnh chạy: streamlit run app.py