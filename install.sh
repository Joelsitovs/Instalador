#!/bin/bash

# Configurar colores para mensajes
GREEN="\e[32m"
RED="\e[31m"
YELLOW="\e[33m"
RESET="\e[0m"

# Detener el script si un comando falla
set -e

# Verificar si el usuario es root
if [ "$(id -u)" -ne 0 ]; then
    echo -e "${RED}❌ Este script debe ejecutarse como root.${RESET}" 1>&2
    exit 1
fi

# Actualizar sistema
apt update && apt upgrade -y
echo -e "${GREEN}✅ Sistema actualizado.${RESET}"

# Obtener el home del usuario que ejecuta el script con sudo
user_home=$(eval echo ~$SUDO_USER)
repo_dir="$user_home/instalador-servidor-web"

# Verificar si Python3 está instalado
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 no está instalado. Instalando...${RESET}"
    apt update && apt install -y python3
else
    echo -e "${GREEN}✅ Python3 ya está instalado.${RESET}"
fi

# Verificar si psmisc está instalado
if ! dpkg -l | grep -q psmisc; then
    echo -e "${RED}❌ psmisc no está instalado. Instalando...${RESET}"
    apt update && apt install -y psmisc
else
    echo -e "${GREEN}✅ psmisc ya está instalado.${RESET}"
fi

# Instrucciones para ejecutar el script
sudo python3 $repo_dir/v2.py
