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