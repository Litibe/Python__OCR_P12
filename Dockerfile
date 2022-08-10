FROM python:3.10.2
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app/
COPY . /app/
RUN python3 -m venv venv
RUN . venv/bin/activate
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python manage.py collectstatic

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]