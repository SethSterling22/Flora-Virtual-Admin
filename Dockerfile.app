# Hecho por Sebastián Sterling :D
# docker build --no-cache -t mi-imagen .
# Se puede cambiar el tag dependiendo de la versión que se quiera (VERIFICAR VERSIÓN DE FUNCIONAMIENTO DE PROGRAMA), después de los dos puntos 
FROM python:3.13

# Evita la interacción durante la instalación de paquetes
ARG DEBIAN_FRONTEND=noninteractive

# Actualiza la lista de paquetes e instala las actualizaciones
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Comando por defecto (opcional)
CMD ["tail", "-f", "/dev/null"]

# Esta imagen deja el contenedor corriendo solamente sin activar la aplicación
