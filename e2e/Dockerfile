FROM registry.access.redhat.com/openshift3/jenkins-slave-base-rhel7
  
ARG NODE_MAJOR_VERSION=10
ARG NODE_VERSION=v10.13.0

ENV SUMMARY="Jenkins slave with stock nodejs ${NODE_VERSION}"  \
    DESCRIPTION="Jenkins pipeline slave with stock nodejs ${NODE_VERSION}"

LABEL summary="$SUMMARY" \
      description="$DESCRIPTION" \
      io.k8s.description="$DESCRIPTION" \
      io.k8s.display-name="jenkins-pipeline-nodejs${NODE_MAJOR_VERSION}" \
      io.openshift.expose-services="8080:http" \
      io.openshift.tags="builder,jenkins-jnlp-nodejs,jenkins-jnlp-nodejs${NODE_MAJOR_VERSION},jenkins-jnlp" \
      release="1"

ENV PATH=$HOME/.local/bin/:$PATH \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8


# Fetch stock nodejs and install
RUN mkdir -p /opt && \
    pushd /opt && \
    curl -sL https://nodejs.org/dist/${NODE_VERSION}/node-${NODE_VERSION}-linux-x64.tar.xz | tar -Jx && \
    rm -f node-${NODE_VERSION}-linux-x64.tar.xz \
    wget --no-verbose --output-document /tmp/firefox-65.0.tar.bz2 https://ftp.mozilla.org/pub/firefox/releases/65.0/linux-x86_64/en-US/firefox-65.0.tar.bz2 && \
    tar -xjf /tmp/firefox-65.0.tar.bz2 && \
    mv firefox /opt/firefox65 && \
    ln -s /opt/firefox65/firefox-bin /usr/bin/firefox

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
