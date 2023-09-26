FROM python:3.11

LABEL authors="alexr"

RUN apt update && apt clean && rm -rf /var/lib/apt/lists/*


RUN mkdir "/cad_documents_app"
WORKDIR /cad_documents_app

COPY ./src ./src
COPY ./commands ./commands
COPY ./requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip && \
    pip install -r ./requirements.txt

CMD ["bash"]
