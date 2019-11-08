FROM certbot/certbot:v0.40.1

RUN pip install schedule

COPY run.py /run.py

EXPOSE 80
VOLUME ["/etc/letsencrypt"]

CMD ["/run.py"]