FROM solr:9.10.1
USER root

ARG SOLR_VERSION="9.10.1"
ARG VCS_REF="missing"
ARG BUILD_DATE="missing"
ARG CORE="name_request"
ARG FOLLOWER_CORE="name_request_follower"
ARG LEADER_CORE="name_request"
ARG SOLR_OPTS_VAR='$SOLR_OPTS'
ARG JVM_MEM="1g"

ENV VCS_REF=${VCS_REF}
ENV BUILD_DATE=${BUILD_DATE}
ENV CORE=${CORE}
ENV FOLLOWER_CORE=${FOLLOWER_CORE}
ENV LEADER_CORE=${LEADER_CORE}
ENV JVM_MEM=${JVM_MEM}

LABEL org.label-schema.vcs-ref=${VCS_REF} \
    org.label-schema.build-date=${BUILD_DATE}

# copy files into leader / follower configsets
COPY ./solr/${CORE}/conf /opt/solr-${SOLR_VERSION}/server/solr/configsets/${CORE}/conf
COPY ./solr/${LEADER_CORE}/conf /opt/solr-${SOLR_VERSION}/server/solr/configsets/${FOLLOWER_CORE}/conf
# copy follower specific config into configset
COPY ./solr/${FOLLOWER_CORE}/conf/solrconfig.xml /opt/solr-${SOLR_VERSION}/server/solr/configsets/${FOLLOWER_CORE}/conf/solrconfig.xml
# copy in starting core
COPY ./solr/${LEADER_CORE}/conf /var/solr/data/${CORE}/conf
# copy core specific config into starting core
COPY ./solr/${CORE}/core.properties /var/solr/data/${CORE}/core.properties
COPY ./solr/${CORE}/conf/solrconfig.xml /var/solr/data/${CORE}/conf/solrconfig.xml
# copy solr.xml (will be used by both leader and followers)
COPY ./solr/solr.xml /opt/solr-${SOLR_VERSION}/server/solr/solr.xml
# solr env overrides
RUN echo "" >> /etc/default/solr.in.sh
RUN echo SOLR_OPTS=\"$SOLR_OPTS_VAR -Dsolr.disable.allowUrls=true\" >> /etc/default/solr.in.sh
# NB: OPs flow is to set these afterwards so the same image can be tagged across dev/test/prod
# RUN echo SOLR_OPTS=\"$SOLR_OPTS_VAR -Dsolr.environment=$ENVIRONMENT\" >> /etc/default/solr.in.sh
# RUN echo SOLR_OPTS=\"$SOLR_OPTS_VAR -Dsolr.leaderUrl=$LEADER_URL\" >> /etc/default/solr.in.sh

# jvm memory
RUN echo SOLR_JAVA_MEM=\"-Xms$JVM_MEM -Xmx$JVM_MEM\" >> /etc/default/solr.in.sh

RUN chmod -R 777 /var/solr/data
RUN chmod -R 777 /opt/solr-${SOLR_VERSION}

USER 1001

EXPOSE 8983
