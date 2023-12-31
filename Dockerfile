FROM python:3.10
WORKDIR /usr/src/app/
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
COPY ./requirements.txt .

# RUN apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl
# RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

RUN pip install -r requirements.txt
COPY . .

# Add wait-for-it.sh script
ADD ./wait-for-it.sh .
# COPY ./wait-for-it.sh .
RUN chmod +x wait-for-it.sh