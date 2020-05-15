FROM certbot/certbot:v0.40.1

COPY run.py /run.py
RUN apk add --no-cache gcc musl-dev && \
    pip install schedule pyOpenSSL pyjks &&\
    apk del gcc musl-dev &&\
    chmod +x /run.py
USER root:root
ENTRYPOINT ["python","/run.py"]
