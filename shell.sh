#!/bin/bash
# arquivo: reset_airflow.sh

set -e  # para o script se algum comando falhar

echo "🛑 Parando e removendo containers, volumes e imagens antigas..."
docker compose down -v --rmi all

#echo "🔹 Construindo imagens do Docker Compose..."
docker compose build

echo "🔹 Rodando o airflow-cli para listar configuração..."
docker compose run --rm airflow-cli airflow config list

echo "🔹 Inicializando o Airflow..."
docker compose up airflow-init

echo "🔹 Subindo o Airflow em background..."
docker compose up -d

echo "✅ Airflow resetado e pronto!"

