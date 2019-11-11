FROM certbot/certbot:v0.40.1

COPY run.py /run.py
RUN pip install schedule pyOpenSSL && chmod +x /run.py
USER root:root
ENTRYPOINT ["python","/run.py"]
