FROM ubuntu:latest
LABEL authors="aboba"

ENTRYPOINT ["top", "-b"]