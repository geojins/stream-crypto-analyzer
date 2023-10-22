FROM python:3

WORKDIR app
# Install dependencies.
RUN pip install -y requirements.txt

COPY . .

# Entrypoint
CMD ["python", "main.py"]