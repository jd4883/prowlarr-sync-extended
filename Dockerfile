FROM 	--platform=linux/amd64 python:latest
ENV     \
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

COPY    . ./
RUN     pip install --no-cache-dir -r requirements.txt
CMD     [ "python", "./main.py" ]