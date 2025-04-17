import streamlit as st
import fitz  # PyMuPDF
import docx
import os

# Простейший словарь ключевых IT-навыков
SKILLS = {
    "Python", "Java", "C++", "SQL", "Git", "Linux", "Docker",
    "Kubernetes", "AWS", "Azure", "HTML", "CSS", "JavaScript",
    "React", "Node.js", "TensorFlow", "Pandas", "FastAPI", "NumPy", "Scikit-learn"
}

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_skills(text, marker):
    text = text.lower()
    start = text.find(marker.lower())
    if start == -1:
        return set()
    relevant_text = text[start:]
    found = {skill for skill in SKILLS if skill.lower() in relevant_text}
    return found

def compare_skills(candidate_skills, job_skills):
    match = candidate_skills & job_skills
    missing = job_skills - candidate_skills
    percent = int(len(match) / len(job_skills) * 100) if job_skills else 0
    return match, missing, percent

# Интерфейс
st.set_page_config(page_title="Анализ соответствия компетенций", layout="wide")
st.title("📊 Анализ соответствия компетенций IT-специалиста вакансии")

# 🔽 Блок для загрузки шаблонов
with st.expander("📁 Скачать шаблоны для корректной работы"):
    col1, col2 = st.columns(2)
    with col1:
        if os.path.exists("resume_template.docx"):
            with open("resume_template.docx", "rb") as f:
                st.download_button("📄 Скачать шаблон резюме", f, file_name="Резюме_шаблон.docx")
        else:
            st.error("Файл resume_template.docx не найден.")

    with col2:
        if os.path.exists("job_template.docx"):
            with open("job_template.docx", "rb") as f:
                st.download_button("📝 Скачать шаблон вакансии", f, file_name="Вакансия_шаблон.docx")
        else:
            st.error("Файл job_template.docx не найден.")

# 🔼 Загрузка файлов
col1, col2 = st.columns(2)

with col1:
    st.header("📄 Резюме")
    resume_file = st.file_uploader("Загрузите файл резюме (PDF/DOCX)", type=["pdf", "docx"])

with col2:
    st.header("📝 Описание вакансии")
    job_file = st.file_uploader("Загрузите файл вакансии (PDF/DOCX)", type=["pdf", "docx"])

if resume_file and job_file:
    with st.spinner("Обработка файлов..."):
        resume_text = extract_text_from_pdf(resume_file) if resume_file.name.endswith(".pdf") else extract_text_from_docx(resume_file)
        job_text = extract_text_from_pdf(job_file) if job_file.name.endswith(".pdf") else extract_text_from_docx(job_file)

        resume_skills = extract_skills(resume_text, "НАВЫКИ:")
        job_skills = extract_skills(job_text, "ТРЕБУЕМЫЕ НАВЫКИ:")

        matched, missing, percent = compare_skills(resume_skills, job_skills)

        st.subheader("🎯 Результаты анализа")
        st.metric("Процент соответствия", f"{percent}%")

        col1, col2 = st.columns(2)
        with col1:
            st.write("✅ Совпадающие навыки:")
            st.write(sorted(matched))
        with col2:
            st.write("❌ Недостающие навыки:")
            st.write(sorted(missing))

        st.subheader("📚 Рекомендации:")
        if missing:
            st.info("Рекомендуется изучить: " + ", ".join(sorted(missing)))
        else:
            st.success("Все необходимые навыки присутствуют!")
