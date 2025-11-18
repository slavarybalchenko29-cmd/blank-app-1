import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader  # ВИПРАВЛЕНО ТУТ

# Налаштування сторінки
st.set_page_config(page_title="AI Тендерний Аналітик", page_icon="⚖️")

st.title("🏛️ AI Тендерний Аналітик (Prozorro)")
st.write("Завантажте тендерну документацію (PDF), щоб перевірити ризики та підібрати ноутбуки.")

# Сайдбар
with st.sidebar:
    st.header("Налаштування")
    api_key = st.text_input("Введіть Google Gemini API Key", type="password")
    st.markdown("[Отримати ключ безкоштовно](https://aistudio.google.com/app/apikey)")

# Логіка
if api_key:
    try:
        genai.configure(api_key=api_key)
        
        uploaded_file = st.file_uploader("Завантажте ТЗ (PDF)", type=["pdf"])
        
        if uploaded_file is not None:
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
                
            st.info(f"Документ завантажено! Кількість сторінок: {len(reader.pages)}")
            
            if st.button("🔍 Аналізувати Тендер"):
                with st.spinner("AI аналізує документ..."):
                    # Використовуємо flash модель, вона швидка і безкоштовна
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    prompt = f"""
                    Ти - експерт із закупівель. Проаналізуй цей текст тендеру на ноутбуки.
                    
                    Текст документа:
                    {text[:30000]}
                    
                    Завдання:
                    1. Випиши основні технічні вимоги (Процесор, RAM, SSD).
                    2. Знайди приховані ризики або дискримінаційні вимоги.
                    3. Порівняй з моїм ноутбуком: "Latitude 4200" (i7, 16GB RAM, 512GB SSD). Чи він проходить?
                    """
                    
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    
    except Exception as e:
        st.error(f"Виникла помилка: {e}")
else:
    st.warning("⬅️ Введіть API ключ у меню зліва, щоб почати.")
