FROM python:3.8.6-buster

ARG BUILD_DATE
ARG VCS_REF

LABEL build_date=$BUILD_DATE
LABEL vcs_ref=$VCS_REF

USER root

# Create working directory
RUN mkdir /opt/app-root && chmod 755 /opt/app-root
WORKDIR /opt/app-root

# Install the requirements
COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install .

USER 1001

# Set Python path
ENV PYTHONPATH=/opt/app-root/src

EXPOSE 8080

CMD ["hypercorn", "--bind", "0.0.0.0:8080", "wsgi:app"]
