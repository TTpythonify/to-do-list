FROM python:3.14

WORKDIR /app

COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set Flask environment variables
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV DATABASE_URL=postgresql://postgres:password@db:5432/todo_db

# Expose port for container access
EXPOSE 5000

# Start flask
CMD ["flask", "run"]