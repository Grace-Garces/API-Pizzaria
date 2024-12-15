FROM python:3.10-slim

# Etapa 1: Definir o diretório de trabalho
WORKDIR /app

# Etapa 2: Instalar dependências do sistema (se necessário)
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean

# Etapa 3: Copiar o requirements.txt para o contêiner
COPY requirements.txt /app/  

# Etapa 4: Atualizar pip e instalar as dependências do Python
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt  # Apontando para o local exato do arquivo

# Etapa 5: Copiar o código-fonte para o contêiner
COPY . /app/  

# Etapa 6: Definir o comando padrão
CMD ["python", "app/script.py"]
