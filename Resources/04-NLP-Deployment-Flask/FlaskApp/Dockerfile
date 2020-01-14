FROM publysher/alpine-numpy:1.14.0-python3.6-alpine3.7

# multiple pip install lines to avoid 
# pkg dependancy issues
# scipy==1.0.0 for pickle loading issues
# for pickle issues, build .pkl file wih the same sklearn version
# you will be using to load it
# ALWAYS DO PIP INSTALLS IN IMAGE `RUN`
# NOT IN CONTAINERS
RUN apk --no-cache add lapack libstdc++\
    && apk --no-cache add --virtual .builddeps g++ gcc gfortran musl-dev lapack-dev\
    && pip install cython \
    && pip install scipy==1.0.0 \
    && pip install scikit-learn==0.21.3 \
    && pip install pandas flask nltk \
    && pip install pickle5 \
    && apk del .builddeps \
    && rm -rf /root/.cache


WORKDIR /app

COPY . /app
#RUN pip3 install -r requirements.txt

EXPOSE 4000

# to use same scikit learn version
RUN python model.py

# ------------------------------------------------------
# defined for running flask
# Use this only. Don't use `wait.sh` with this
ENTRYPOINT ["python"]
CMD ["app.py"]
# ------------------------------------------------------

#CMD ["chmod", "+x", "wait.sh"]
#CMD ["sh", "wait.sh"]

# 1. Create image:
#   docker build -t flask-nlp-basic-image:v1 .
# 2. Run container based on image:
#   docker run -p 5000:4000 -d --name flask-test-container flask-nlp-basic-image:v1
# 3. make container wait so that we can enter it
#   CMD ["chmod", "+x", "wait.sh"]
#   CMD ["sh", "wait.sh"]
# 4. Enter into container:
#   docker exec -it <container-id> /bin/sh
