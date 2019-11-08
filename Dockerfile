FROM certbot/certbot:v0.40.1

COPY run.py /run.py
RUN pip install schedule && chmod +x /run.py

ENTRYPOINT ["python","/run.py"]
