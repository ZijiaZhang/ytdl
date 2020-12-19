FROM nikolaik/python-nodejs
COPY . /app
WORKDIR /app
RUN npm install -D
RUN npx webpack
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD python ./main.py