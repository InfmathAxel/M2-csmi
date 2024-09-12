FROM ubuntu:24.04

RUN apt update

RUN apt install -y python3 python3-pip python3-ipykernel

RUN apt install -y python3-sklearn