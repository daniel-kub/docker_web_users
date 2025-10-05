# Docker Web Users - Dokumentacja

## Wstęp

Ten repozytorium dotyczy tworzenia użytkowników z kontami FTP, użytkownikami i bazami danych MySQL oraz stronami internetowymi przy użyciu Docker i Traefik. Na podstawie README.md, założenia projektu to:

- Stworzenie użytkownika z dostępem do konta FTP, MySQL oraz hostingu strony z subdomeną (np. user.example.com).
- Stworzenie skryptu umożliwiającego szybkie i proste dodawanie użytkownika.
- Zmniejszenie ingerencji administratora (np. poprzez skrypt do łatwej zmiany hasła FTP).

Wykorzystane technologie:
- Docker do tworzenia kontenerów.
- Traefik jako reverse proxy do routingu subdomen.
- MySQL i PHPMyAdmin do zarządzania bazami danych.
- PHP do budowania stron.
- Python do skryptu tworzenia użytkownika i API.

Poniżej opisano każdy plik w repozytorium wraz z jego ścieżką i działaniem, na podstawie nazwy, lokalizacji i dostępnej zawartości.

## Pliki w katalogu głównym

### README.md
Plik zawiera opis projektu, założenia oraz listę wykorzystanych technologii. Służy jako główna dokumentacja repozytorium, wyjaśniająca cel i strukturę.

### dodaj_uzytkownika.py
Skrypt Pythonowy do dodawania nowego użytkownika. Na podstawie nazwy ("dodaj_uzytkownika" oznacza "add_user") i opisu w README, ten plik odpowiada za szybkie tworzenie użytkownika z kontem FTP, bazą MySQL i stroną internetową. Prawdopodobnie automatyzuje konfigurację Docker kontenerów i ustawień.

## Katalog: mysql

### mysql/docker-compose.yml
Plik konfiguracyjny Docker Compose dla usługi MySQL. Definiuje kontenery związane z bazą danych, takie jak serwer MySQL i prawdopodobnie PHPMyAdmin do administrowania bazami. Służy do uruchamiania i zarządzania bazami danych dla użytkowników.

## Katalog: panel

### panel/docker-compose.yml
Plik Docker Compose dla panelu administracyjnego. Konfiguruje kontenery dla API i interfejsu webowego panelu, w tym prawdopodobnie serwer PHP lub inny do obsługi zmiany haseł i zarządzania użytkownikami.

#### Podkatalog: api

### panel/api/main.py
Główny plik Pythonowy dla API. Obsługuje backend API do zarządzania użytkownikami, takie jak zmiana haseł. Na podstawie struktury, to serwer API (prawdopodobnie używający frameworka jak Flask), który przetwarza żądania od frontendu.

### panel/api/userapi.service
Plik usługi systemd (service file) dla API użytkownika. Definiuje, jak uruchomić i zarządzać usługą API jako demonem w systemie Linux, zapewniając automatyczne startowanie i restartowanie.

### panel/api/usluga.sh
Skrypt shellowy ("usluga" oznacza "service"). Prawdopodobnie pomaga w uruchamianiu lub konfiguracji usługi API, np. instalacja zależności, start serwera lub zadania pomocnicze związane z deploymentem.

#### Podkatalog: html

### panel/html/zmiana_hasla.php
Plik PHP do zmiany hasła ("zmiana_hasla" oznacza "change_password"). Zawiera formularz webowy, który pozwala użytkownikowi na zmianę hasła FTP/MySQL. Skrypt wysyła dane do API za pomocą cURL, przetwarza odpowiedź i wyświetla komunikaty sukcesu lub błędu. To interfejs frontendowy dla funkcji zmiany hasła, zmniejszający potrzebę interwencji administratora.

## Katalog: strony

### strony/Dockerfile
Plik Dockerfile do budowania obrazu Docker dla stron internetowych użytkowników. Definiuje środowisko dla hostingu stron (prawdopodobnie oparte na PHP/Apache), umożliwiając tworzenie kontenerów dla subdomen użytkowników.

## Katalog: traefik

### traefik/docker-compose.yml
Plik Docker Compose dla Traefik. Konfiguruje reverse proxy do routingu ruchu z subdomen (np. user.example.com) do odpowiednich kontenerów stron użytkowników. Obsługuje automatyczne przekierowania i zarządzanie certyfikatami SSL.



## Jak uruchomić projekt Docker Web Users

Na podstawie analizy repozytorium (https://github.com/daniel-kub/docker_web_users), README.md nie zawiera szczegółowych instrukcji uruchomienia. Projekt wydaje się być w fazie rozwoju, a pliki konfiguracyjne (jak docker-compose.yml) nie zostały w pełni udokumentowane lub ich zawartość nie jest dostępna w surowej formie. Dlatego opisuję kroki na podstawie standardowych praktyk dla projektów opartych na Docker, Traefik, MySQL i Python, uwzględniając strukturę repozytorium. Zakładam, że masz zainstalowanego Dockera, Docker Compose oraz Pythona (wersja 3.x).

### Wymagania wstępne
- **System operacyjny**: Linux (zalecany, ze względu na skrypty shellowe jak usluga.sh), Windows lub macOS z Docker Desktop.
- **Oprogramowanie**:
  - Docker i Docker Compose (wersja 2+).
  - Python 3 z bibliotekami potrzebnymi do skryptu (np. jeśli skrypt używa modułów jak subprocess, requests – zainstaluj je via `pip install -r requirements.txt`, jeśli plik istnieje; w przeciwnym razie załóż standardowe biblioteki).
  - Domena z DNS skonfigurowanym do wildcard subdomen (np. *.example.com指向ujący na IP serwera) dla Traefik.
- **Konfiguracja środowiska**:
  - Ustaw zmienne środowiskowe, jeśli wymagane (np. dla MySQL: root password; dla Traefik: certyfikaty Let's Encrypt).
  - Upewnij się, że porty 80, 443 (dla Traefik) i inne (np. 3306 dla MySQL) są otwarte.

### Krok 1: Sklonuj repozytorium
Otwórz terminal i wykonaj:
```
git clone https://github.com/daniel-kub/docker_web_users.git
cd docker_web_users
```

### Krok 2: Uruchom Traefik (reverse proxy)
Traefik jest odpowiedzialny za routing subdomen do kontenerów stron użytkowników.
- Przejdź do katalogu: `cd traefik`
- Edytuj `docker-compose.yml` jeśli potrzeba (np. dodaj email dla Let's Encrypt, ustaw domain).
- Uruchom: 
  ```
  docker-compose up -d
  ```
- Sprawdź logi: `docker-compose logs -f` (powinien wystartować na portach 80/443).

### Krok 3: Uruchom MySQL i PHPMyAdmin
MySQL obsługuje bazy danych dla użytkowników, a PHPMyAdmin to interfejs webowy.
- Przejdź do katalogu: `cd ../mysql` (lub z głównego: `cd mysql`)
- Edytuj `docker-compose.yml` (ustaw hasło roota MySQL, np. poprzez environment variables).
- Uruchom:
  ```
  docker-compose up -d
  ```
- Dostęp do PHPMyAdmin: zazwyczaj pod adresem `http://localhost:8080` lub skonfigurowaną subdomeną (zależnie od Traefik).

### Krok 4: Uruchom panel administracyjny
Panel zawiera API (Python) i frontend (PHP) do zarządzania, np. zmiany haseł.
- Przejdź do katalogu: `cd ../panel` (lub z głównego: `cd panel`)
- W podkatalogu `api`:
  - Uruchom skrypt usługi: `./api/usluga.sh` (prawdopodobnie instaluje lub startuje API jako usługę; jeśli to systemd, użyj `sudo systemctl start userapi` po konfiguracji).
  - Dodaj mu brakujące pakiety poprzez sudo pip install -r requirements.txt --break-system-packages
  - API jest w `api/main.py` – prawdopodobnie uruchamiane jako serwer (np. Flask/Uvicorn). Jeśli nie startuje automatycznie, wykonaj: `python api/main.py`.
- Edytuj `docker-compose.yml` jeśli potrzeba (np. volumes dla danych).
- Uruchom:
  ```
  docker-compose up -d
  ```
- Frontend (zmiana_hasla.php): Dostępny pod subdomeną panelu, pozwala na zmianę hasła via formularz, który wysyła żądanie do API.

### Krok 5: Dodaj użytkownika
Skrypt `dodaj_uzytkownika.py` automatyzuje tworzenie użytkownika z FTP, MySQL i stroną.
- Z głównego katalogu: `python dodaj_uzytkownika.py [argumenty]`
  - Argumenty: Prawdopodobnie nazwa użytkownika, hasło, subdomena (np. `python dodaj_uzytkownika.py --user nowyuser --password haslo123 --domain example.com`).
  - Skrypt tworzy kontener strony (używając `strony/Dockerfile`), dodaje użytkownika do MySQL i konfiguruje FTP.
- Jeśli skrypt wymaga edycji, sprawdź kod dla komentarzy.

### Krok 6: Testowanie i zarządzanie
- Strony użytkowników: Dostępne pod subdomenami (np. http://user.example.com).
- Zmiana hasła: Użyj panelu HTML (`html/zmiana_hasla.php`) – formularz wysyła dane do API, które aktualizuje hasło FTP/MySQL.
- Monitorowanie: Użyj `docker ps` do sprawdzenia kontenerów, `docker logs [container_name]` dla logów.
- Zatrzymanie: W każdym katalogu `docker-compose down`.

### Uwagi
- Projekt zmniejsza rolę admina, więc po uruchomieniu użytkownicy mogą sami zmieniać hasła via panel.
- Jeśli napotkasz błędy, sprawdź konfiguracje (np. volumes dla persistencji danych w MySQL).
- Brak pełnych instrukcji w repo sugeruje, że to projekt edukacyjny lub WIP – rozważ kontakt z autorem (daniel-kub) na GitHub.
- Bezpieczeństwo: Ustaw silne hasła, użyj HTTPS via Traefik.

Jeśli potrzebujesz więcej szczegółów, podaj dodatkowe informacje lub sprawdź aktualizacje repozytorium.