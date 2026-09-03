FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY . .

# Expose Streamlit and FastAPI ports
EXPOSE 8501 8000

# Start script
RUN echo "#!/bin/bash\nuvicorn src.serving.server:app --host 0.0.0.0 --port 8000" > start.sh
RUN chmod +x start.sh

CMD ["./start.sh"]
