FROM python:3.7
ARG output_file="/output.conf"
ARG run
ARG loop_forever=10
WORKDIR /code

COPY update-ips.py .
COPY requirements.txt .
COPY reload-nginx.sh .
RUN pip install -r requirements.txt

ENTRYPOINT update-ips.py /input/* -o "${output_file}" -r "reload-nginx.sh" -l ${loop_forever}
