# Use an official Python runtime as a parent image
FROM python:3.10-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Patch the django-cart package
RUN sed -i 's/ugettext_lazy/gettext_lazy/g' /usr/local/lib/python3.10/site-packages/cart/models.py

# Copy project
COPY . /app/

# Collect static files
#RUN python manage.py collectstatic --noinput

# Expose the port your app runs on
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "django_project.wsgi:application"]
