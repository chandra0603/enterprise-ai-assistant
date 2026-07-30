FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

# Install CPU-only PyTorch
RUN pip install --no-cache-dir \
    torch==2.13.0 \
    --index-url https://download.pytorch.org/whl/cpu

# Install remaining packages
RUN grep -v "^torch==" requirements.txt > requirements_no_torch.txt && \
    pip install --no-cache-dir -r requirements_no_torch.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]