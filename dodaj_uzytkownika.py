#!/usr/bin/env python3
import subprocess
import sys
import pymysql
from string import Template
import os

# --- Konfiguracja domyślna ---
DEFAULT_PASSWORD = "1234"
MYSQL_ROOT_PASSWORD = "daniel25"  # <- zmień na swoje hasło roota MySQL
OUTPUT_DIR = "/home/userwww/strony"  # katalog na strony / FTP
DOMAIN = "techrabka.eu"  # domena główna


def ensure_shell_in_etc_shells(shell_path: str):
    """Dopisuje powłokę do /etc/shells jeśli jej tam nie ma (wymagane przez vsftpd/su itp.)."""
    try:
        with open("/etc/shells", "r+") as f:
            shells = f.read()
            if shell_path not in shells:
                if not shells.endswith("\n"):
                    f.write("\n")
                f.write(f"{shell_path}\n")
                print(f"[OK] Dodano {shell_path} do /etc/shells")
    except Exception as e:
        print(f"[WARN] Nie udało się zapisać do /etc/shells: {e} (upewnij się ręcznie)")


def create_linux_user(username, password=DEFAULT_PASSWORD, shell="/bin/bash"):
    """
    Tworzy użytkownika systemowego.
    Domyślnie używa /bin/bash jako powłoki, ale możesz podać inny shell (np. /bin/false).
    """
    home_dir = os.path.join(OUTPUT_DIR, username)
    try:
        # Utwórz katalog dla strony, jeśli nie istnieje
        os.makedirs(home_dir, exist_ok=True)

        # Dopilnuj żeby powłoka istniała w /etc/shells (potrzebne dla vsftpd/su)
        ensure_shell_in_etc_shells(shell)

        # Utwórz użytkownika z zadanym katalogiem domowym i powłoką
        # -m tworzy katalog domowy jeśli nie istnieje
        subprocess.run(
            ["sudo", "useradd", "-m", "-d", home_dir, "-s", shell, username],
            check=True
        )

        # Ustaw hasło
        subprocess.run(
            ["sudo", "chpasswd"],
            input=f"{username}:{password}".encode(),
            check=True
        )

        # Ustaw właściciela katalogu i prawa
        subprocess.run(
            ["sudo", "chown", "-R", f"{username}:{username}", home_dir],
            check=True
        )
        subprocess.run(["sudo", "chmod", "755", home_dir], check=True)
        # upewnij się, że katalogi nadrzędne mają execute bit
        subprocess.run(["sudo", "chmod", "755", "/home"], check=False)
        subprocess.run(["sudo", "mkdir", "-p", "/home/userwww"], check=False)
        subprocess.run(["sudo", "chmod", "755", "/home/userwww"], check=False)
        subprocess.run(["sudo", "mkdir", "-p", "/home/userwww/strony"], check=False)
        subprocess.run(["sudo", "chmod", "755", "/home/userwww/strony"], check=False)

        print(f"[OK] Utworzono użytkownika Linux: {username} (shell: {shell}) katalog: {home_dir} hasło: {password}")

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Błąd przy tworzeniu użytkownika Linux: {e}")
        sys.exit(1)


def create_mysql_user_and_db(username, password=DEFAULT_PASSWORD):
    """Tworzy użytkownika MySQL i jego bazę."""
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password=MYSQL_ROOT_PASSWORD,
            autocommit=True
        )
        cursor = conn.cursor()

        db_name = f"{username}"

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
        cursor.execute(f"CREATE USER IF NOT EXISTS '{username}'@'%' IDENTIFIED BY '{password}'")
        cursor.execute(f"GRANT ALL PRIVILEGES ON `{db_name}`.* TO '{username}'@'%'")
        cursor.execute("FLUSH PRIVILEGES")

        cursor.close()
        conn.close()

        print(f"[OK] Utworzono użytkownika MySQL: {username}@'%', bazę: {db_name}, hasło: {password}")

    except Exception as err:
        print(f"[ERROR] Błąd MySQL: {err}")
        sys.exit(1)



def generate_docker_compose(username):
    """Tworzy plik docker-compose.yml dla użytkownika, używając wspólnego Dockerfile i bez DB"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, f"{username}-compose.yml")

    szablon = Template("""version: '3.8'
name: ${user}-projekt

services:
  php:
    build:
      context: /home/userwww/strony  # katalog z Dockerfile
      dockerfile: /home/userwww/strony/../Dockerfile
    image: php-global:8.2
    container_name: ${user}-strona
    volumes:
      - /home/userwww/strony/${user}:/var/www/html
    networks:
      - web
    restart: unless-stopped
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.${user}-router.rule=Host(`${user}.${domain}`)"
      - "traefik.http.routers.${user}-router.entrypoints=web"

networks:
  web:
    external: true
""")

    tekst = szablon.substitute(
        user=username,
        domain=DOMAIN
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(tekst)

    print(f"[OK] Wygenerowano plik docker-compose: {path}")
    return path




def run_docker_compose(compose_file, username):
    """Uruchamia docker compose z unikalnym projektem"""
    try:
        subprocess.run(
            ["docker", "compose", "-f", compose_file, "-p", username, "up", "-d"],
            check=True
        )
        print(f"[OK] Uruchomiono docker compose dla {compose_file} (projekt: {username})")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Nie udało się uruchomić docker compose: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Użycie: python3 {sys.argv[0]} nazwa_uzytkownika [shell]")
        print("Przykład: python3 dodaj_uzytkownika.py daniel /bin/bash")
        sys.exit(1)

    username = sys.argv[1]
    shell_arg = sys.argv[2] if len(sys.argv) >= 3 else "/bin/bash"

    create_linux_user(username, shell=shell_arg)
    create_mysql_user_and_db(username)
    compose_path = generate_docker_compose(username)
    run_docker_compose(compose_path, username)
