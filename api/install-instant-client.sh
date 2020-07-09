#!/bin/bash
# To run ODPI-C applications with Oracle Instant Client zip files:
# Download the 11.2 or 12.1 “Basic” or “Basic Light” zip file from here. Choose either a 64-bit or 32-bit package, matching your application architecture. Most applications use 64-bit.
# Unzip the package into a single directory that is accessible to your application. For example:
# https://www.oracle.com/ca-en/database/technologies/instant-client/macos-intel-x86-downloads.html

export PKG=https://download.oracle.com/otn_software/mac/instantclient/193000/instantclient-basic-macos.x64-19.3.0.0.0dbru.zip

mkdir -p ~/opt/oracle
curl -vo ~/opt/oracle/instantclient-basic-macos.x64.zip ${PKG}

unzip ~/opt/oracle/instantclient-basic-macos.x64.zip -d ~/opt/oracle/instantclient
# Add links to $HOME/lib to enable applications to find the library. For example:
# mkdir ~/lib
# -- ln -s /opt/oracle/instantclient_12_1/libclntsh.dylib.12.1 ~/lib/
# ln -s ~/opt/oracle/instantclient/instantclient_19_3/libclntsh.dylib.12.1 ~/lib/
# ln -s ~/opt/oracle/instantclient/instantclient_19_3/libocci.dylib.18.1 ~/lib/
# ln -s ~/opt/oracle/instantclient/instantclient_19_3/libocci.dylib.19.1 ~/lib/

# Just add dir to PATH when done
# export PATH=$PATH:~/opt/oracle/instantclient/instantclient_19_3

# Or
# ln -s ~/opt/oracle/instantclient/instantclient_19_3/libclntsh.dylib /usr/local/lib/