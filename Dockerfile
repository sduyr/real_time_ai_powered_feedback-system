# Base Image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy all files to the container
COPY . /app

# Install backend and frontend dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt
RUN pip install --no-cache-dir -r frontend/requirements.txt

# Expose ports for Flask and Streamlit
EXPOSE 5000 8501

# Start both backend and frontend
CMD ["sh", "-c", "python backend/app.py & streamlit run frontend/main.py --server.port 8501 --server.headless true"]
