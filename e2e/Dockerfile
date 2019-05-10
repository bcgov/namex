FROM daggerok/e2e
  
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

RUN sudo apt-get -y install nodejs

EXPOSE 8080

USER 1001
