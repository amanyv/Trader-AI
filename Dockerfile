FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt /app/
RUN pip install -r /app/requirements.txt

RUN pip install \
    fastapi \
    uvicorn \
    httpx \
    qdrant-client \
    yfinance \
    pandas


EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
