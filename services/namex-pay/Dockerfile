FROM python:3.8.5-buster
USER root

ARG VCS_REF="missing"
ARG BUILD_DATE="missing"

ENV VCS_REF=${VCS_REF}
ENV BUILD_DATE=${BUILD_DATE}

LABEL org.label-schema.vcs-ref=${VCS_REF} \
    org.label-schema.build-date=${BUILD_DATE}

USER root

# Installing Oracle instant client
WORKDIR    /opt/oracle
RUN        apt-get update && apt-get install -y libaio1 wget unzip \
    # && wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip \
    # && wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-sqlplus-linuxx64.zip \
    # && unzip instantclient-basiclite-linuxx64.zip \
    # && rm -f instantclient-basiclite-linuxx64.zip \
    # && unzip instantclient-sqlplus-linuxx64.zip \
    # && rm -f instantclient-sqlplus-linuxx64.zip \
    && wget https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-basiclite-linux.x64-21.1.0.0.0.zip \
    && wget https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-sqlplus-linux.x64-21.1.0.0.0.zip \
    && unzip instantclient-basiclite-linux.x64-21.1.0.0.0.zip \
    && rm -f instantclient-basiclite-linux.x64-21.1.0.0.0.zip \
    && unzip instantclient-sqlplus-linux.x64-21.1.0.0.0.zip \
    && rm -f instantclient-sqlplus-linux.x64-21.1.0.0.0.zip \
    && cd /opt/oracle/instantclient* \
    && rm -f *jdbc* *occi* *mysql* *README *jar uidrvci genezi adrci \
    && echo /opt/oracle/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf \
    && ldconfig

# Create working directory
RUN mkdir /opt/app-root && chmod 755 /opt/app-root
WORKDIR /opt/app-root

# Install the requirements
COPY ./requirements.txt .

#RUN pip install --upgrade pip
RUN pip install pip==20.1.1
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install .

USER 1001

# Set Python path
ENV PYTHONPATH=/opt/app-root/src

#EXPOSE 8080

CMD [ "python", "/opt/app-root/run.py" ]
