FROM certbot/certbot:v0.40.1

RUN apk add --no-cache gcc musl-dev && \
    pip install schedule pyOpenSSL pyjks &&\
    apk del gcc musl-dev    
COPY run.py /run.py
RUN chmod a+x /run.py && mkdir -p /etc/letsencrypt/live && chown -Rv daemon:root /etc/letsencrypt/ && chmod -Rv 0700 /etc/letsencrypt/
ENTRYPOINT ["python","/run.py"]
