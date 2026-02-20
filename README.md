# Pokémon-kort kombineringsapp

En enkel app som kombinerer bilder av fremside og bakside av kort side om side:

- siste + nest siste
- tredje siste + fjerde siste
- osv. (N+N-1, N-2+N-3, ...)

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

1. Klikk **Velg bilder (flere)** (rekkefølgen beholdes, men appen starter fra siste valgte bilde).
2. Velg lagringsmappe.
3. Klikk **Kombiner og lagre .jpg**.

## Bruk (kommandolinje)

Hvis du allerede har alle bildene i én mappe, kan du kjøre uten GUI:

```bash
python app.py --input-dir ./bilder --output-dir ./ferdige --quality 95
```

- Filene i input-mappen sorteres alfabetisk, men behandling starter fra siste fil i listen.
- Antall bilder må være et partall.

## Navn på output-filer

Output får navn som:

- `kort_0001.jpg`
- `kort_0002.jpg`
- ...
