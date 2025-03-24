FROM apache/airflow:2.10.5

# Instala Java (OpenJDK 11)
USER root

RUN apt-get update && \
    apt-get install -y default-jdk && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

#ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
#ENV PATH="${JAVA_HOME}/bin:${PATH}"


# Copiar o Spark para dentro da imagem
#COPY spark-3.5.5-bin-hadoop3 /opt/spark
RUN curl -fsSL https://dlcdn.apache.org/spark/spark-3.5.5/spark-3.5.5-bin-hadoop3.tgz \
    | tar -xz -C /opt/ \
    && mv /opt/spark-3.5.5-bin-hadoop3 /opt/spark
# Definir variáveis de ambiente do Spark
ENV SPARK_HOME=/opt/spark
ENV PATH="$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH"

# Configurar permissões
RUN chown -R $(id -u airflow):$(id -g airflow) /opt/spark

ENV SPARK_MAJOR_VERSION=3.5
ENV ICEBERG_VERSION=1.8.1

# Download iceberg spark runtime
RUN curl https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-${SPARK_MAJOR_VERSION}_2.12/${ICEBERG_VERSION}/iceberg-spark-runtime-${SPARK_MAJOR_VERSION}_2.12-${ICEBERG_VERSION}.jar -Lo /opt/spark/jars/iceberg-spark-runtime-${SPARK_MAJOR_VERSION}_2.12-${ICEBERG_VERSION}.jar

# Download AWS bundle
RUN curl -s https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-aws-bundle/${ICEBERG_VERSION}/iceberg-aws-bundle-${ICEBERG_VERSION}.jar -Lo /opt/spark/jars/iceberg-aws-bundle-${ICEBERG_VERSION}.jar

# Download GCP bundle
#RUN curl -s https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-gcp-bundle/${ICEBERG_VERSION}/iceberg-gcp-bundle-${ICEBERG_VERSION}.jar -Lo /opt/spark/jars/iceberg-gcp-bundle-${ICEBERG_VERSION}.jar

# Download Azure bundle
#RUN curl -s https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-azure-bundle/${ICEBERG_VERSION}/iceberg-azure-bundle-${ICEBERG_VERSION}.jar -Lo /opt/spark/jars/iceberg-azure-bundle-${ICEBERG_VERSION}.jar


USER airflow

ADD requirements.txt .
RUN pip install apache-airflow==2.10.5 -r requirements.txt