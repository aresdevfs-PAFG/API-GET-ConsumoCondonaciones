# Usar imagen oficial de Python 3.11 slim
FROM python:3.11-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar primero solo requirements.txt para aprovechar la caché de Docker
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la aplicación
COPY . .

# Exponer el puerto que Cloud Run usará (variable de entorno PORT)
ENV PORT=8080

# Comando para ejecutar la aplicación
# Cloud Run usa la variable de entorno PORT
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT}
