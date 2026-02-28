FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# VULNERABILITY: Hardcoded credentials in Dockerfile
ENV AZURE_OPENAI_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
ENV AZURE_OPENAI_ENDPOINT=https://contoso-openai-prod.openai.azure.com/

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
