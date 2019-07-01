FROM python:3.7
#ARG output_file="/output.conf"
#ARG loop_forever=10
WORKDIR /nginx-dynamics-ips

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY update-ips.py .
COPY reload-docker-nginx.sh .
RUN chmod +x update-ips.py
RUN chmod +x reload-docker-nginx.sh
# RUN apt-get update && apt-get install docker -y

ENTRYPOINT ./update-ips.py /input/* -o "${OUTPUT_FILE}" -r "./reload-docker-nginx.sh" -l "${LOOP_FOREVER}"
