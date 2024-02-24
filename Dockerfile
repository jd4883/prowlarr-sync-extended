FROM 	--platform=linux/amd64 python:latest
ENV     \
        SONARR_API
COPY    . ./
RUN     pip install --no-cache-dir -r requirements.txt
CMD     [ "python", "./main.py" ]