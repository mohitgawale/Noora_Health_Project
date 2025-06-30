FROM python:3.10-slim

# Install Java, wget, curl
RUN apt-get update && \
    apt-get install -y default-jdk wget curl && \
    apt-get clean

# Dynamically get JAVA_HOME
RUN JAVA_PATH=$(dirname $(dirname $(readlink -f $(which java)))) && \
    echo "export JAVA_HOME=$JAVA_PATH" >> /etc/profile && \
    echo "export PATH=\$JAVA_HOME/bin:\$PATH" >> /etc/profile && \
    echo "JAVA_HOME=$JAVA_PATH" >> /etc/environment && \
    echo "PATH=$JAVA_PATH/bin:\$PATH" >> /etc/environment

# Set environment variables manually too
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH="$JAVA_HOME/bin:$PATH"

# Install Spark
ENV SPARK_VERSION=3.5.1
ENV HADOOP_VERSION=3
RUN curl -fsSL https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -o spark.tgz && \
    tar -xzf spark.tgz -C /opt && \
    mv /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark && \
    rm spark.tgz

ENV SPARK_HOME=/opt/spark
ENV PATH="$PATH:$SPARK_HOME/bin"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

WORKDIR /app
