FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

WORKDIR /app

COPY requirements.txt .
RUN pip install python-multipart
RUN pip install --no-cache-dir -r requirements.txt

# Copy model creation script and generate the model file
COPY ./model ./model
RUN python model/create_model.py

COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]