FROM python
WORKDIR /demoapp
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
CMD ["python","./app.py"]
EXPOSE 5000