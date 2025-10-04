<h1>Docker Web Users</h1>
<h2>Założenia projektu</h2>
<ol>
        <li>Stworzenie użytkownika który będzie miał dostęp do konta FTP, MySQL oraz hostingu strony z subdomeną (np. user.example.com)</li>
        <li>Stworzenie skryptu który umożliwi szybkie i proste stworzenie użytkownika</li>
        <li>Zmniejszenie ingerencji administratora (poprzez skrypt który umożliwia łatwą zmiane hasła dla FTP)</li>
</ol>
<h2>Wykorzystane przeze mnie technologie</h2>
<ol>
        <li>Docker</li>
        Umożliwia on bardzo łatwo tworzyć różne kontenery jednym plikiem
        <li>Traefik</li>
        Jest to narzędzie znane jako reverse proxy i przekierowuje ruch z subdomeny (np. user.example.com) do odpowiedniego kontenera
        <li>MySQL i PHPmyAdmin</li>
        Jest to znane narzędzie do tworzenia i administrowania bazami danych z interfejsem webowym
        <li>PHP</li>
        Jest to język interpretowany który umożliwia na podstawie tego budowanie strony
        <li>Python</li>
        Ten język interpretowany jest wykorzystywany w tym projekcie do skryptu tworzącego użytkownika oraz API
</ol>
