# 🎓 College AI Assistant

A simple chatbot that answers common college questions such as timetable, exams, fees, library, hostel and placements. It is built with Python and Streamlit and uses TF-IDF with cosine similarity to match a student's question to the closest FAQ.

## Features
- Chat interface built with Streamlit
- Answers questions from a custom FAQ dataset (`data/faqs.csv`)
- Shows the category of each answer
- Gives a fallback reply when no match is found
- Easy to extend by adding more rows to the CSV

## Tech Stack
- Python
- Streamlit
- Pandas, NumPy
- scikit-learn (TF-IDF, cosine similarity)

## Project Structure
```
college_ai_assistant/
├── app.py              # Streamlit UI
├── assistant.py        # answering logic
├── data/
│   └── faqs.csv        # college FAQs (question, answer, category)
└── requirements.txt    # dependencies
```

## How to Run
1. Clone or download this project
2. Install dependencies:
```
   pip install -r requirements.txt
```
3. Start the app:
```
   streamlit run app.py
```
4. Open `http://localhost:8501` in your browser

## How It Works
1. The questions in `faqs.csv` are converted into TF-IDF vectors.
2. The user's question is converted into a vector the same way.
3. Cosine similarity finds the closest FAQ.
4. If the similarity is above the threshold, its answer is shown. Otherwise a fallback message is shown.

## Sample Questions
- What is the minimum attendance required?
- What are the library timings?
- How can I pay my fees online?

## Future Improvements
- Add an LLM API for more natural answers
- Add a dashboard of the most asked question categories
- Support multiple languages

## Author
[Lasya Thallapelly] – 2nd-year B.Tech CSE (Data Science), [Mallareddy Engneering College For Women]