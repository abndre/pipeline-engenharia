# pipeline-engenharia


Initialize the project
```
docker compose up -d
```

Access the airflow webpage:

http://localhost:8080/

airflow:airflow

Access the minins3 webpage

http://localhost:9001/

admin:password

## Airflow Con

atualize a connection do airflow: aws_default, adicione no extra

```
{
  "aws_access_key_id": "admin",
  "aws_secret_access_key": "password",
  "endpoint_url": "http://minio:9000"
}
```

## Local Stack

Com o aws cli instalado

```
export AWS_ACCESS_KEY_ID="test"
export AWS_SECRET_ACCESS_KEY="test"
export AWS_DEFAULT_REGION="us-east-1"

aws --endpoint-url=http://localhost:4566 s3 ls

#sqs
aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name sqs-dev-andre

aws --endpoint-url=http://localhost:4566 sqs send-message --queue-url http://localhost:4566/000000000000/sqs-dev-andre --message-body '{"hello":"world"}'

```