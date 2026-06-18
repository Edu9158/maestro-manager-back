# 1. Usando a imagem base do Python 3.14 (slim para ser mais leve)
FROM python:3.14-rc-slim

# 2. Define o diretório de trabalho dentro do container
WORKDIR /app

# 3. Evita que o Python gere arquivos .pyc e permite logs em tempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. Instala dependências do sistema que podem ser necessárias para pacotes Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 5. Copia apenas o requirements.txt primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# 6. Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copia todo o conteúdo do projeto para dentro do container
COPY . .

# 8. Expõe a porta que sua aplicação usa (ex: 8000, 5000 ou 8080)
EXPOSE 8000

# 9. Comando para rodar a aplicação
CMD ["python", "main.py"]