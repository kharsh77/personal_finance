FROM python:3.9-slim

RUN apt-get -q -y update 
RUN apt-get install -y gcc

ENV USERNAME=pfm_user
ENV WORKING_DIR=/home/pfm_app

WORKDIR ${WORKING_DIR}

COPY app app
COPY requirements.txt .
COPY service_entrypoint.sh .

# RUN groupadd ${USERNAME} && \
#     useradd -g ${USERNAME} ${USERNAME}

# RUN chown -R ${USERNAME}:${USERNAME} ${WORKING_DIR}
# RUN chmod -R u=xxx,g=xxx ${WORKING_DIR}

# USER ${USERNAME}
# ENV PATH "$PATH:/home/${USERNAME}/.local/bin"


RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV FLASK_APP=app
RUN chmod +x service_entrypoint.sh

EXPOSE 5000

# RUN flask db init

ENTRYPOINT [ "./service_entrypoint.sh" ]