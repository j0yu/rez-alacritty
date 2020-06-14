ARG IMAGE=centos:7
FROM $IMAGE

ARG NAME=alacritty
ARG SRC_PATH=/usr/local/src/$NAME
ARG VERSION=0.4.3
WORKDIR $SRC_PATH
RUN curl -L --progress-bar \
    "https://github.com/alacritty/alacritty/archive/v$VERSION.tar.gz" \
    | tar -xz --strip-components=1

COPY install-dependencies entrypoint /bin/
RUN chmod +x /bin/install-dependencies /bin/entrypoint

ENTRYPOINT entrypoint
RUN install-dependencies
