## 🛠 Instalador de Servidor Web (Nginx, PHP, MariaDB, phpMyAdmin)

Este es un script automatizado para instalar, configurar y administrar un servidor web con **Nginx, PHP, MariaDB y phpMyAdmin** en sistemas basados en Debian/Ubuntu.

### 📌 **Características**
- Instalación automática de:
  - **Nginx** (servidor web)
  - **PHP** (módulos y configuración)
  - **MariaDB** (base de datos)
  - **phpMyAdmin** (gestión de bases de datos en entorno web)
- Configuración automática de Nginx y phpMyAdmin.
- Opción para desinstalar los paquetes si es necesario.
- Reinicio y verificación del estado de los servicios.

---

## 📥 **Instalación**
### 🔹 **Requisitos**
Antes de ejecutar el script, asegúrate de que tu sistema está actualizado:
```bash
sudo apt update && sudo apt upgrade -y
```
Si no esta actualizado el script lo actualizara

### 🔹 **Clonar el repositorio**
Ejecuta el siguiente comando en tu terminal para clonar el repositorio:
```bash
git clone https://github.com/Joelsitovs/Instalador.git
cd Instalador
```

### 🔹 **Ejecutar el script**
El script requiere permisos de administrador (**sudo**):
> **⚠️ Nota:** Si obtienes un error de permisos, usa:
```bash
chmod +x install.sh
```

```bash
sudo  ./install.sh
```



---

## 📌 **Opciones del Instalador**
El script tiene un menú interactivo donde puedes seleccionar qué deseas hacer:

1️⃣ **Instalar MariaDB**  
2️⃣ **Instalar Nginx**  
3️⃣ **Instalar PHP**  
4️⃣ **Instalar phpMyAdmin**  
5️⃣ **Instalar todo**  
6️⃣ **Salir**  

---

## 🚀 **Desinstalación**
Si necesitas desinstalar los servicios instalados:
```bash
sudo python3 desisv3.py
```

> Esto eliminará **Nginx, PHP, MariaDB y phpMyAdmin** del sistema, además de limpiar archivos de configuración.

---

## 🛠 **Solución de Problemas**
Si tienes problemas con los servicios, puedes reiniciarlos manualmente:
```bash
sudo systemctl restart nginx mariadb php8.3-fpm
```

Para verificar si están corriendo:
```bash
sudo systemctl status nginx
sudo systemctl status mariadb
sudo systemctl status php8.3-fpm
```

Si phpMyAdmin no carga correctamente, revisa los **logs de errores**:
```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/mysql/error.log
```

---

## 👨‍💻 **Contribuciones**
Si quieres mejorar este instalador, siéntete libre de hacer un **fork** del repositorio y enviar **pull requests**. 🚀

---

## 📜 **Licencia**
Este proyecto está bajo la licencia **MIT**, por lo que puedes usarlo y modificarlo libremente.

---

