import subprocess
import os
import sys
import getpass
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def check_root():
    """Verifica si el script se ejecuta con privilegios de root"""
    if os.geteuid() != 0:
        print("❌ Este script debe ejecutarse con privilegios de root (sudo).")
        sys.exit(1)


def desistalar():
    #Desinstala phpMyAdmin y maneja errores correctamente
    print(f"{bcolors.OKBLUE} Desinstalando paquetes...{bcolors.ENDC}")
    time.sleep(1)
    subprocess.run(
        "sudo dpkg --purge phpmyadmin",
        shell=True, check=True
    )
    print(f"{bcolors.OKGREEN} Paquete phpMyAdmin desinstalado correctamente.{bcolors.ENDC}")
    
    print(f"{bcolors.OKBLUE}Comprobando si el paquete phpMyAdmin ha sido desinstalado...{bcolors.ENDC}")
    time.sleep(1)
    try:
        subprocess.run(
            "dpkg -l | grep phpmyadmin",
            shell=True, check=True
        )
        print(f"{bcolors.WARNING} El paquete phpMyAdmin no ha sido desinstalado correctamente.{bcolors.ENDC}")
        subprocess.run(
            "sudo apt remove --purge -y phpmyadmin",
            shell=True, check=True
        )
        print(f"{bcolors.OKGREEN} Paquete phpMyAdmin desinstalado correctamente.{bcolors.ENDC}")
        print(f"{bcolors.OKBLUE} Limpiando archivos temporales...{bcolors.ENDC}")
        time.sleep(1)
        limpiar()
    except subprocess.CalledProcessError:
        print(f"{bcolors.OKGREEN} Paquete phpMyAdmin desinstalado correctamente.{bcolors.ENDC}")
        try: 
            print(f"{bcolors.OKBLUE} Borrando configuración de phpMyAdmin...{bcolors.ENDC}")
            time.sleep(1)
            subprocess.run(
                "sudo rm -rf /etc/phpmyadmin /var/lib/phpmyadmin /var/www/html/phpmyadmin",
                shell=True, check=True
            )
            print(f"{bcolors.OKGREEN} Configuración de phpMyAdmin eliminada correctamente.{bcolors.ENDC}")
            print(f"{bcolors.OKBLUE} Limpiando archivos temporales...{bcolors.ENDC}")
            time.sleep(1)
            limpiar()
        except subprocess.CalledProcessError:
            print(f"{bcolors.WARNING} Error al eliminar la configuración de phpMyAdmin.{bcolors.ENDC}")
   

    #Desinstala MariaDB y maneja errores correctamente
    try:
        print(f"Verificando paqutes de MariaDB...")
        time.sleep(1)
        try:
            subprocess.run(
                "dpkg -l | grep mariadb",
                shell=True, check=True
            )
            print(f"{bcolors.OKGREEN} Paquetes de MariaDB encontrados.{bcolors.ENDC}")
            try:
                subprocess.run(
                "sudo dpkg --purge $(dpkg -l | grep -i 'mariadb' | awk '{print $2}')",
                shell=True, check=True
                )
                print(f"{bcolors.OKGREEN} Paquetes de MariaDB desinstalados correctamente.{bcolors.ENDC}")
            except subprocess.CalledProcessError:
                print(f"{bcolors.WARNING} Error al desinstalar paquetes de MariaDB.{bcolors.ENDC}")
                try:
                    subprocess.run(
                        "sudo apt remove --purge -y mariadb-server mariadb-client mariadb-common",
                        shell=True, check=True
                    )
                    print(f"{bcolors.OKGREEN} Paquetes de MariaDB desinstalados correctamente.{bcolors.ENDC}")
                except subprocess.CalledProcessError:
                    print(f"{bcolors.WARNING} Error al desinstalar paquetes de MariaDB.{bcolors.ENDC}")
        except subprocess.CalledProcessError:
            print(f"{bcolors.WARNING} Paquetes de MariaDB no encontrados.{bcolors.ENDC}")
        
        try:
            print(f"{bcolors.OKBLUE} Eliminando archivos de configuración de MariaDB...{bcolors.ENDC}")
            time.sleep(1)
            directorios = ["/etc/mysql", "/var/lib/mysql", "/var/log/mysql*"] #"/var/run/mysql"
            for directorio in directorios:
                subprocess.run(f"sudo rm -rf {directorio}", shell=True, check=True)
            print(f"{bcolors.OKGREEN} Archivos de configuración de MariaDB eliminados correctamente.{bcolors.ENDC}")
        except subprocess.CalledProcessError:
            print(f"{bcolors.WARNING} Error al eliminar archivos de configuración de MariaDB.{bcolors.ENDC}")
            
        limpiar()
    except subprocess.CalledProcessError:
        print(f"{bcolors.WARNING} Error al verificar paquetes de MariaDB.{bcolors.ENDC}")
    

        
    
    
def verficar_nginx():
    result = subprocess.run(
        "dpkg -l | grep nginx",
        shell=True, check=True
    )
    if result.returncode == 0:
        return True
    
def desistalar_nginx():
    try:
        print ("Verificando paquetes de Nginx...")
        
        if not verficar_nginx():
            print("❌ Nginx no está instalado.")
            return

        try:
            print(f"{bcolors.OKBLUE} Desinstalando Nginx...{bcolors.ENDC}")
            time.sleep(1)
            subprocess.run(
            "sudo apt remove --purge -y nginx nginx-common nginx-full",
            shell=True, check=True
            )
            print(f"{bcolors.OKGREEN} Nginx desinstalado correctamente.{bcolors.ENDC}")
            print(f"{bcolors.OKBLUE} Eliminando archivos de configuración de Nginx...{bcolors.ENDC}")
            time.sleep(1)
            directorios = ["/etc/nginx", "/var/www/html", "/var/log/nginx"]
            for directorio in directorios:
                subprocess.run(f"sudo rm -rf {directorio}", shell=True, check=True)
                print(f"{bcolors.OKGREEN} Archivos de configuración de Nginx eliminados correctamente.{bcolors.ENDC}")
            limpiar()
        except subprocess.CalledProcessError:
            print(f"{bcolors.WARNING} Error al desinstalar Nginx.{bcolors.ENDC}")
    except subprocess.CalledProcessError:
        print("❌ Error al desinstalar Nginx.")
        

def verificar_php():
    try:
        result = subprocess.run(
        "dpkg -l | grep php",
        shell=True, capture_output=True,text=True
        )
        if not result.stdout.strip():
            print("❌ PHP no está instalado.")
            return False
        print("PHP está instalado.")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error al verificar paquetes de PHP.")
        return False
    
def desinstalar_php():
    print("Verificando paquetes de PHP...")
    if not verificar_php():
        print("❌ PHP no está instalado. no hay nada que desinstalar.")
        return
    
    try:
        print(f"{bcolors.OKBLUE} Desinstalando PHP...{bcolors.ENDC}")
        time.sleep(1)
        subprocess.run(
            "sudo dpkg --purge $(dpkg -l | grep -i 'php' | awk '{print $2}')",
            shell=True, check=True
        ),
    
        
        print(f"{bcolors.OKGREEN} Paquetes de PHP desinstalados correctamente.{bcolors.ENDC}")
        try:
            subprocess.run(
                "sudo apt remove --purge -y php php-cli php8.2-fpm php-mysql php-xml php-curl php-mbstring php-zip",
                shell=True, check=True
            )
            print(f"{bcolors.OKGREEN} Paquetes de PHP desinstalados correctamente.{bcolors.ENDC}")
        except subprocess.CalledProcessError:
            print(f"{bcolors.WARNING} Error al desinstalar paquetes de PHP.{bcolors.ENDC}")
        try:
            directorios = ["/etc/php", "/var/lib/php", "/var/log/php"]
            for directorio in directorios:
                subprocess.run(f"sudo rm -rf {directorio}", shell=True, check=True)
            print(f"{bcolors.OKGREEN} Archivos de configuración de PHP eliminados correctamente.{bcolors.ENDC}")
        except subprocess.CalledProcessError:
            print(f"{bcolors.WARNING} Error al eliminar archivos de configuración de PHP.{bcolors.ENDC}")
        limpiar()
    except subprocess.CalledProcessError:
        print(f"{bcolors.WARNING} Error al desinstalar PHP.{bcolors.ENDC}")
        
    
def limpiar():
    print(f"{bcolors.OKBLUE}Limpiando archivos temporales...{bcolors.ENDC}")
    subprocess.run(
        "sudo apt autoremove -y && sudo apt autoclean",
        shell=True, check=True
    )
    print(f"{bcolors.OKGREEN}✅ Archivos temporales eliminados.{bcolors.ENDC}")
    time.sleep(2)
    
    
def main():
    check_root()
    desistalar()
    desistalar_nginx()
    desinstalar_php()
    
if __name__ == "__main__":
    main()