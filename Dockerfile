FROM 	--platform=linux/amd64 python:latest
ARG     \
        LIDARR_API \
        LIDARR_HOST=http://127.0.0.1:8686 \
        PROWLARR_API \
        PROWLARR_HOST=127.0.0.1:9696 \
        RADARR_API \
        RADARR_HOST=http://127.0.0.1:7878 \
        READARR_API \
        READARR_HOST=http://127.0.0.1:8787 \
        SONARR_API \
        SONARR_HOST=http://127.0.0.1:8989
ENV     \
        LIDARR_API=${LIDARR_API} \
        LIDARR_HOST=${LIDARR_HOST} \
        PROWLARR_API=${PROWLARR_API} \
        PROWLARR_HOST=${PROWLARR_HOST} \
        RADARR_API=${RADARR_API} \
        RADARR_HOST=${RADARR_HOST} \
        READARR_API=${READARR_API} \
        READARR_HOST=${READARR_HOST} \
        SONARR_API=${SONARR_API} \
        SONARR_HOST=${SONARR_HOST}

WORKDIR /config
COPY    . ./
RUN     pip install --no-cache-dir -r requirements.txt
CMD     [ "python", "./main.py" ]