import json
import os
from pathlib import Path

import google.generativeai as genai
import pandas as pd
import streamlit as st
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
MEMBERS = ["Tuấn Linh", "Thu Hương", "Minh Anh", "Lâm Khánh", "Duy Anh"]
UNSUPPORTED_MESSAGE = (
    "Tôi đang không hỗ trợ chức năng này. Xin liên hệ nhân viên nhà hàng "
    "qua hotline 1900 561 252 để được trợ giúp."
)


def load_app_data() -> tuple[list[str], str, pd.DataFrame]:
    # Đọc cấu hình và menu, luôn sử dụng đường dẫn cùng thư mục với app.py.
    with (BASE_DIR / "config.json").open(encoding="utf-8") as file:
        config = json.load(file)

    features = config.get("function", [])
    if isinstance(features, str):
        features = [features]

    welcome_message = config.get(
        "initial_bot_message", "Chào bạn, tôi là CSI24_Bot. Tôi có thể giúp bạn điều gì?"
    )
    menu = pd.read_csv(BASE_DIR / "menu.csv", index_col=0).fillna("")
    return features, welcome_message, menu


def create_system_instruction(menu: pd.DataFrame, features: list[str]) -> str:
    # Tạo system instruction tập trung, để dễ mở rộng dữ liệu và chức năng của bot.
    menu_information = "\n".join(
        (
            f"- {row['name']}: {row['description']} "
            f"Nguyên liệu: {row['ingredients']}. Ghi chú: {row['notes'] or 'Không có'}."
        )
        for _, row in menu.iterrows()
    )
    feature_list = "; ".join(features) or "Giới thiệu lớp và menu"

    return f"""
Bạn là CSI24 Chatbot, trợ lý thân thiện của lớp MK-C4K-CSI24 tại cơ sở Minh Khai, Hà Nội.

CHỨC NĂNG HỖ TRỢ
- 1. Giới thiệu lớp: tên lớp, cơ sở học và mục đích của CSI24 Chatbot.
- 2. Tra cứu thành viên: liệt kê thành viên của lớp.
- 3. Xem menu: liệt kê toàn bộ món hiện có trong menu.
- 4. Tra cứu món ăn: mô tả, nguyên liệu và ghi chú phục vụ của một món cụ thể.
- 5. So sánh món ăn: đối chiếu nguyên liệu, mô tả và ghi chú của tối đa hai món có trong menu.
- 6. Gợi ý món: gợi ý theo nhu cầu đơn giản của khách, ví dụ món nước, món cơm hoặc món ăn nhẹ; giải thích dựa trên dữ liệu menu, không khẳng định về sức khỏe hay dinh dưỡng.
- 7. Hướng dẫn sử dụng: nêu các dạng câu hỏi bot có thể trả lời và đưa ví dụ câu hỏi.

NGUYÊN TẮC
- Trả lời bằng tiếng Việt, ngắn gọn, lịch sự và đúng dữ liệu bên dưới.
- Các chức năng cấu hình ban đầu: {feature_list}.
- Chỉ hỗ trợ bảy chức năng ở trên. Nếu khách nói chưa rõ, hãy hỏi lại một câu ngắn để làm rõ.
- Nếu câu hỏi không thuộc các nội dung trên, chỉ trả lời đúng câu: "{UNSUPPORTED_MESSAGE}"
- Không bịa thêm giá, khuyến mãi, thời gian hoạt động, địa chỉ chi tiết hoặc thông tin không có trong dữ liệu.

THÔNG TIN LỚP
- Tên lớp: MK-C4K-CSI24.
- Thành viên: {', '.join(MEMBERS)}.

MENU
{menu_information}

CÁCH TRẢ LỜI
- Khi được hỏi về menu chung, liệt kê tên món và mời người dùng hỏi thêm về một món.
- Khi hỏi về một món, nêu mô tả, nguyên liệu và ghi chú của đúng món đó.
- Nếu tên món không có trong menu, nói rõ món đó chưa có trong menu hiện tại.
- Khi so sánh, trình bày ngắn gọn theo từng tiêu chí; không đưa ra dữ liệu không có trong menu.
- Khi gợi ý, chỉ chọn từ menu hiện tại và giải thích lý do bằng loại món hoặc nguyên liệu có trong dữ liệu.
- Khi được hỏi bot làm được gì, hãy liệt kê 7 chức năng và 2-3 ví dụ câu hỏi.
""".strip()


@st.cache_resource(show_spinner=False)
def create_model(system_instruction: str, api_key: str):
    # Khởi tạo Gemini một lần cho mỗi cấu hình ứng dụng.
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        "gemini-3.5-flash", system_instruction=system_instruction
    )


def should_show_menu_locally(prompt: str) -> bool:
    # Chỉ hiển thị dữ liệu cục bộ cho câu hỏi tra cứu menu đơn giản.
    keywords = ("menu", "món", "đồ ăn", "nguyên liệu", "gỏi", "phở", "cơm", "bún", "khoai")
    advanced_requests = ("so sánh", "khác nhau", "gợi ý", "đề xuất", "nên ăn", "phù hợp")
    normalized_prompt = prompt.lower()
    return any(keyword in normalized_prompt for keyword in keywords) and not any(
        request in normalized_prompt for request in advanced_requests
    )


def format_menu(menu: pd.DataFrame, selected_dish: str | None = None) -> str:
    # Định dạng menu chung hoặc thông tin chi tiết của một món.
    dishes = menu[menu["name"].str.casefold() == selected_dish.casefold()] if selected_dish else menu
    if dishes.empty:
        return "Món này chưa có trong menu hiện tại."

    details = []
    for _, dish in dishes.iterrows():
        item = f"**{dish['name']}**\n\n{dish['description']}\n\n**Nguyên liệu:** {dish['ingredients']}"
        if dish["notes"]:
            item += f"\n\n**Ghi chú:** {dish['notes']}"
        details.append(item)
    return "\n\n---\n\n".join(details)


def build_conversation_context(messages: list[dict]) -> str:
    # Giữ ngữ cảnh ngắn gọn cho các lượt chat trước đó.
    recent_messages = messages[-8:]
    return "\n".join(
        f"{'Khách' if message['role'] == 'user' else 'CSI24 Bot'}: {message['content']}"
        for message in recent_messages
    )


def get_bot_reply(prompt: str, model, menu: pd.DataFrame) -> str:
    if should_show_menu_locally(prompt):
        matched_dish = next(
            (name for name in menu["name"] if name.casefold() in prompt.casefold()), None
        )
        return format_menu(menu, matched_dish)

    context = build_conversation_context(st.session_state.conversation_log)
    response = model.generate_content(
        f"LỊCH SỬ TRÒ CHUYỆN:\n{context}\n\nCÂU HỎI MỚI CỦA KHÁCH: {prompt}"
    )
    return response.text.strip() if response.text else "Xin lỗi, tôi chưa thể tạo câu trả lời lúc này."


def reset_conversation(welcome_message: str) -> None:
    st.session_state.conversation_log = [{"role": "assistant", "content": welcome_message}]


def csi24_chatbot() -> None:
    st.set_page_config(page_title="CSI24 Chatbot", page_icon="🤖")
    features, welcome_message, menu = load_app_data()
    load_dotenv(BASE_DIR / ".env")
    api_key = os.getenv("GOOGLE_API_KEY")

    if "conversation_log" not in st.session_state:
        reset_conversation(welcome_message)

    with st.sidebar:
        st.header("CSI24 Chatbot")
        st.caption("Hỏi về lớp, thành viên hoặc menu đồ ăn.")
        if st.button("🗑️ Xóa lịch sử", use_container_width=True):
            reset_conversation(welcome_message)
            st.rerun()
        history_json = json.dumps(st.session_state.conversation_log, ensure_ascii=False, indent=2)
        st.download_button(
            "⬇️ Tải lịch sử", history_json, "csi24-chat-history.json", "application/json",
            use_container_width=True,
        )
        st.divider()
        selected_dish = st.selectbox("Xem nhanh thông tin món", ["-- Chọn món --", *menu["name"].tolist()])
        if selected_dish != "-- Chọn món --":
            st.markdown(format_menu(menu, selected_dish))

    st.title("🤖 CSI24 Chatbot")
    st.caption("Bạn có thể hỏi về lớp MK-CSI24, thành viên và menu đồ ăn.")

    quick_questions = [
        "Giới thiệu về lớp MK-CSI24",
        "Lớp có những thành viên nào?",
        "Gợi ý cho tôi một món ăn nhẹ",
    ]
    columns = st.columns(len(quick_questions))
    for column, question in zip(columns, quick_questions):
        if column.button(question, use_container_width=True):
            st.session_state.pending_prompt = question

    for message in st.session_state.conversation_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    typed_prompt = st.chat_input("Nhập yêu cầu của bạn tại đây...")
    prompt = typed_prompt or st.session_state.pop("pending_prompt", None)
    if not prompt:
        return

    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.conversation_log.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            if not api_key:
                raise ValueError("Chưa tìm thấy GOOGLE_API_KEY trong file .env.")
            with st.spinner("CSI24 Bot đang trả lời..."):
                system_instruction = create_system_instruction(menu, features)
                bot_reply = get_bot_reply(prompt, create_model(system_instruction, api_key), menu)
            st.markdown(bot_reply)
        except Exception as error:
            bot_reply = f"Xin lỗi, chatbot đang gặp lỗi: {error}"
            st.error(bot_reply)
    st.session_state.conversation_log.append({"role": "assistant", "content": bot_reply})


if __name__ == "__main__":
    csi24_chatbot()
