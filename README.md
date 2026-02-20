# Pokémon-kort kombineringsapp

En enkel app som kombinerer bilder av fremside og bakside av kort side om side.

Du kan velge mellom:
- start fra slutten: siste + nest siste, tredje siste + fjerde siste
- start fra starten: 1 + 2, 3 + 4, 5 + 6

Output lagres lokalt som `.jpg`.

## Installering

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Bruk (GUI)

Start appen:

```bash
python app.py
```

1. Klikk **Velg bilder (flere)**.
2. Velg lagringsmappe.
3. Velg om appen skal starte fra slutten eller starten av listen.
4. Klikk **Kombiner og lagre .jpg**.

## Bruk (kommandolinje)

Hvis du allerede har alle bildene i én mappe, kan du kjøre uten GUI:

```bash
python app.py --input-dir ./bilder --output-dir ./ferdige --quality 95
```

- Filene i input-mappen sorteres alfabetisk.
- Standard er å starte fra slutten av listen.
- Bruk `--start-from-start` for å starte fra begynnelsen (1+2, 3+4, ...).
- Antall bilder må være et partall.

## Navn på output-filer

Output får navn som:

- `kort_0001.jpg`
- `kort_0002.jpg`
- ...
