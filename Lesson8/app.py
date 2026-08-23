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