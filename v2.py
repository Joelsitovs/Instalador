import subprocess
import os
import sys
import time
import getpass

#Colores
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


#Check si el script se ejecuta con privilegios de root
def check_root():
    if os.geteuid() != 0:
        print(f"{bcolors.FAIL}Este script debe ejecutarse con privilegios de root (sudo).{bcolors.ENDC}")
        sys.exit(1)
        
#Actualiza el sistema operativo
def update_system():
    try:
        print(f"{bcolors.OKBLUE} Actualizando lista de paquetes...{bcolors.ENDC}")
        subprocess.run(["apt", "update"], check=True)
        time.sleep(2)
        print(f"{bcolors.OKBLUE}Actualizando paquetes...")
        subprocess.run(["apt", "upgrade", "-y"], check=True)
        print(f"{bcolors.OKGREEN} Actualización completada.{bcolors.ENDC}")
        time.sleep(2)
        #Verificar si nano esta instalado
        try:
            print(f"{bcolors.WARNING}Verificando si nano esta instalado...{bcolors.ENDC}")
            time.sleep(1)
            subprocess.run(["nano", "--version"], check=True)
            print(f"{bcolors.OKGREEN}✅ Nano está instalado.{bcolors.ENDC}")
            time.sleep(2)
        except subprocess.CalledProcessError:
            print(f"{bcolors.FAIL} Nano no está instalado. Instalando...{bcolors.ENDC}")
            time.sleep(1)
            subprocess.run(["apt", "install", "nano", "-y"], check=True)
            print(f"{bcolors.OKGREEN}Instalación de nano completada. {bcolors.ENDC}")
            time.sleep(2)
            
        print(f"{bcolors.OKGREEN}Continuando.......{bcolors.ENDC}")
    except subprocess.CalledProcessError:
        print("❌ Error al actualizar el sistema.")
        time.sleep(2)
        
def menu():
    #Mostrar el menu de opciones
    print(f"{bcolors.OKBLUE}\n=== Instalador de Servidor Web ==={bcolors.ENDC}")
    print(f"{bcolors.BOLD}1. Instalar MariaDB{bcolors.ENDC}")
    print(f"{bcolors.BOLD}2. Instalar Nginx{bcolors.ENDC}")
    print(f"{bcolors.BOLD}3. Instalar PHP{bcolors.ENDC}")
    print(f"{bcolors.BOLD}4. Instalar phpMyAdmin{bcolors.ENDC}")
    print(f"{bcolors.BOLD}5. Instalar todo{bcolors.ENDC}")
    print(f"{bcolors.BOLD}6. Salir{bcolors.ENDC}")
    
    choice = input(f"{bcolors.OKBLUE}Seleccione una opción: {bcolors.ENDC}")
    return choice
    
            
def instalar_paquetes(paquetes, iniciar_servicio=None):
    try:
        print(f"{bcolors.OKBLUE}Instalando {', '.join(paquetes)}...{bcolors.ENDC}")
        subprocess.run(["apt", "install", "-y"] + paquetes, check=True)
        print(f"{bcolors.OKGREEN}✅ Instalación de {', '.join(paquetes)} completada.{bcolors.ENDC}")
        
        if iniciar_servicio:
            print(f"{bcolors.OKBLUE}Verificando si el servicio esta habilitado...{bcolors.ENDC}")
            try:
                subprocess.run(
                  ["sudo", "service", iniciar_servicio, "status"], check=True
                )
                print(f"{bcolors.OKGREEN}✅ Servicio {iniciar_servicio} está corriendo.{bcolors.ENDC}")
            except subprocess.CalledProcessError:
                print(f"{bcolors.FAIL}Servicio {iniciar_servicio} no está corriendo. Iniciando...{bcolors.ENDC}")
                try:
                    subprocess.run(
                        ["sudo", "service", iniciar_servicio, "start"], check=True
                    )
                    print(f"{bcolors.OKGREEN}✅ Servicio {iniciar_servicio} iniciado correctamente.{bcolors.ENDC}")
                except subprocess.CalledProcessError:
                    print(f"{bcolors.FAIL}❌ Error al iniciar el servicio {iniciar_servicio}{bcolors.ENDC}")
                    try:
                        subprocess.run(
                            ["sudo", "service", iniciar_servicio, "restart"], check=True
                        )
                        print(f"{bcolors.OKGREEN}✅ Servicio {iniciar_servicio} reiniciado correctamente.{bcolors.ENDC}")
                    except subprocess.CalledProcessError:
                        print(f"{bcolors.FAIL}❌ Error al reiniciar el servicio {iniciar_servicio}{bcolors.ENDC}")
                        try:
                            print(f"{bcolors.OKBLUE} Forzar el reinicio del servicio {iniciar_servicio}...{bcolors.ENDC}")
                            print(f"{bcolors.OKBLUE}Parando los servicios...{bcolors.ENDC}") 
                            subprocess.run(
                                ["sudo", "killall","-9", "mariadbd"], check=True
                            )
                            subprocess.run(
                                ["sudo", "killall","-9", "mysqld_safe"], check=True
                            )
                            print(f"{bcolors.OKGREEN}✅ Servicio {iniciar_servicio} detenido.{bcolors.ENDC}")
                            print(f"{bcolors.OKBLUE}Iniciando el servicio...{bcolors.ENDC}")
                            subprocess.run(
                                ["sudo", "service", iniciar_servicio, "start"], check=True
                            )
                            print(f"{bcolors.OKGREEN}✅ Servicio {iniciar_servicio} iniciado correctamente.{bcolors.ENDC}")
                        except subprocess.CalledProcessError:
                            print(f"{bcolors.FAIL}❌ Error al reiniciar el servicio {iniciar_servicio}{bcolors.ENDC}")
                        
        
    except subprocess.CalledProcessError:
        print(f"{bcolors.FAIL}❌ Error al instalar los paquetes{bcolors.ENDC}")
        
        
    
def  install_mariadb():
    instalar_paquetes(["mariadb-server", "mariadb-client"], iniciar_servicio="mariadb")
    print(f"{bcolors.OKGREEN}✅ Instalación de MariaDB completada.{bcolors.ENDC}")
    time.sleep(2)
    limpiar()
    
    
    
def install_nginx():
    instalar_paquetes(["nginx"], iniciar_servicio="nginx")
    print(f"{bcolors.OKGREEN}✅ Instalación de Nginx completada.{bcolors.ENDC}")
    time.sleep(2)
    limpiar()
    
    
def install_php():
    instalar_paquetes(
        ["php", "php-cli", "php-fpm", "php-mysql", "php-xml", "php-curl", "php-mbstring", "php-zip"]
    )
    print(f"{bcolors.OKGREEN}✅ Instalación de PHP completada.{bcolors.ENDC}")
    time.sleep(2)
    limpiar()

def install_phpmyadmin():
    instalar_paquetes(["phpmyadmin"])
    print(f"{bcolors.OKGREEN}✅ Instalación de phpMyAdmin completada.{bcolors.ENDC}")
    time.sleep(2)
    limpiar()
    configuracion()
    
def install_all():
    install_mariadb()
    install_nginx()
    install_php()
    install_phpmyadmin()
    print(f"{bcolors.OKGREEN}✅ Instalación completa.{bcolors.ENDC}")
    time.sleep(2)    

def configuracion():
    #Configura el servidor web
    try:
        print(f"{bcolors.OKBLUE}Configurando Nginx...{bcolors.ENDC}")
        subprocess.run(["cp", "default", "/etc/nginx/sites-available/default"], check=True)
        try:
            subprocess.run(["sudo","ls", "/var/www/html/index.html"], check=True)
            subprocess.run(["sudo","rm","-rf","/var/www/html/index.html"], check=True)
        except subprocess.CalledProcessError:
            print(f"{bcolors.FAIL}❌ Error al eliminar el archivo index.html{bcolors.ENDC}")
            
        print(f"{bcolors.OKGREEN}✅ Configuración de Nginx completada.{bcolors.ENDC}")
        print(f"{bcolors.OKBLUE}Reinicando servicio{bcolors.ENDC}")
        subprocess.run(["service", "nginx", "restart"], check=True)
        print(f"{bcolors.OKGREEN}✅ Servicio reiniciado.{bcolors.ENDC}")
        time.sleep(2)
    except subprocess.CalledProcessError:
        print(f"{bcolors.FAIL}❌ Error al configurar Nginx.{bcolors.ENDC}")
        time.sleep(2)
    
    try:
        print(f"{bcolors.OKBLUE}Configurando phpmyadmin...{bcolors.ENDC}")
        try:
            subprocess.run(["ls", "/var/www/html/phpmyadmin"], check=True)
            print(f"{bcolors.FAIL}❌ El enlace simbolico ya existe.{bcolors.ENDC}")
        except subprocess.CalledProcessError:
            subprocess.run(["sudo","ln", "-s", "/usr/share/phpmyadmin", "/var/www/html/phpmyadmin"], check=True)
            print(f"{bcolors.OKGREEN}✅ Configuración de phpMyAdmin completada.{bcolors.ENDC}")
            time.sleep(2)
    except subprocess.CalledProcessError:
        print(f"{bcolors.FAIL}❌ Error al configurar phpMyAdmin.{bcolors.ENDC}")
        time.sleep(2)
        
    try:
        print(f"{bcolors.OKBLUE}Configurando MariaDB...{bcolors.ENDC}")
        nueva_contrasena = getpass.getpass(f"{bcolors.OKBLUE}Ingrese la nueva contraseña para el usuario root de MariaDB: {bcolors.ENDC}")
        try:
            print(f"{bcolors.OKBLUE}Conectando a MariaDB...{bcolors.ENDC}")
            consulta = f"ALTER USER 'root'@'localhost' IDENTIFIED BY '{nueva_contrasena}';FLUSH PRIVILEGES;"
            comando = f"echo \"{consulta}\" |sudo mariadb -u root -p"
            subprocess.run(comando, shell=True, check=True)
            print(f"{bcolors.OKGREEN}✅ Contraseña cambiada correctamente.{bcolors.ENDC}")
            time.sleep(2)
            subprocess.run(["sudo", "service", "php8.2-fpm", "restart"], check=True)
            print(f"{bcolors.OKGREEN}✅ Configuración de MariaDB completada.{bcolors.ENDC}")
            
        except subprocess.CalledProcessError:
            print(f"{bcolors.FAIL}❌ Error al configurar MariaDB con mysql_secure_installation.{bcolors.ENDC}")
            time.sleep(2)
    except subprocess.CalledProcessError:
        print(f"{bcolors.FAIL}❌ Error al configurar MariaDB.{bcolors.ENDC}")
        time.sleep(2)
        


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
    update_system()
    while True:
        choice = menu()
        if choice == "1":
            install_mariadb()
        elif choice == "2":
            install_nginx()
        elif choice == "3":
            install_php()
        elif choice == "4":
            install_phpmyadmin()
        elif choice == "5":
            install_all()
        elif choice == "6":
            break
        else:
            print(f"{bcolors.FAIL}❌ Opción no válida.{bcolors.ENDC}")
            

    
if __name__ == "__main__":
    main()