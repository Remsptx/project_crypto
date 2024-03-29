FROM python:3.9

WORKDIR /usr/src/app

RUN python -m pip install flask
RUN python -m pip install flask_cors
RUN python -m pip install requests
RUN python -m pip install argon2-cffi

COPY data /usr/src/app/data
COPY static /usr/src/app/static
COPY templates /usr/src/app/templates

# Copy the current directory contents into the container
COPY Server1.py .

# Expose the port the app runs on
EXPOSE 3000

# Run the application
CMD ["python", "Server1.py"]