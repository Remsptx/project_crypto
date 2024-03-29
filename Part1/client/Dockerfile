FROM python:3.9

WORKDIR /usr/src/app

RUN python -m pip install flask
RUN python -m pip install flask_cors
RUN python -m pip install requests
RUN python -m pip install argon2-cffi

COPY credentials.json /usr/src/app/credentials.json
COPY static /usr/src/app/static
COPY templates /usr/src/app/templates

# Copy the current directory contents into the container
COPY app.py .

# Expose the port the app runs on
EXPOSE 3000

# Run the application
CMD ["python", "app.py"]