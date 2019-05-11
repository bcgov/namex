FROM centos:centos7

LABEL name="e2e-image" \ 
			description="Google Chrome/Firefox Headless in a container with nodejs based on BDDStack"

ARG NODE_MAJOR_VERSION=10
ARG NODE_VERSION=v10.13.0


ENV PATH=$HOME/.local/bin/:$PATH \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8


# Fetch stock nodejs and install
RUN mkdir -p /opt && \
    pushd /opt && \
    curl -sL https://nodejs.org/dist/${NODE_VERSION}/node-${NODE_VERSION}-linux-x64.tar.xz | tar -Jx && \
    rm -f node-${NODE_VERSION}-linux-x64.tar.xz

RUN yum -y update; yum clean all
RUN yum -y install epel-release
RUN yum -y install wget nano Xvfb  xorg-x11-xauth java-1.8.0-openjdk git; yum clean all
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
RUN yum -y localinstall google-chrome-stable_current_x86_64.rpm; yum clean all
RUN rm google-chrome-stable_current_x86_64.rpm
RUN yum -y install firefox; yum clean all


# Update environment variables
ENV NODE_HOME=/opt/node-${NODE_VERSION}-linux-x64 \
    PATH=$PATH:/opt/node-${NODE_VERSION}-linux-x64/bin

# Update the version of `npm` that came with the packages above
# and install a few additional tools.
RUN npm i -g npm@latest yarn@latest nsp@latest nodemon@latest  && \
    rm -rf ~/.npm && \
    node -v && \
    npm -v

EXPOSE 8080

USER 1001
