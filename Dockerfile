FROM python:3.7
#ARG output_file="/output.conf"
#ARG loop_forever=10
WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY update-ips.py .
COPY reload-nginx.sh .

# RUN apt-get update && apt-get install docker -y

ENTRYPOINT ./update-ips.py /input/* -o "${OUTPUT_FILE}" -r "./reload-nginx.sh" -l "${LOOP_FOREVER}"
