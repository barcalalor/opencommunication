WORKDIR /django_app
COPY requirements.txt /django_app/
RUN pip install -r requirements.txt
COPY . /django_app/
EXPOSE 8000
#RUN coverage run -m unittest discover -s app/tests -p '*_test.py'
#RUN coverage xml


