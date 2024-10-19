FROM python:3.10-slim

WORKDIR /nba-project

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "nba.py"]