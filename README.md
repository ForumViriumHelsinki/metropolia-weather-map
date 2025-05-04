# Startup

## Docker compose

All parts of the project can be started with docker compose. Compose starts the Client, server and database.

First time running docker you need to first run:
```bash
docker-compose build
```
Once it's been ran once, you can start the application with:
```bash
docker-compose up
```
Populate the database with:
```bash
py .\server\src\api\sql\populate_db.py
```
## Starting components separately

### Client

Starting the client on localhost:3000

```bash
cd /client
pnpm install
pnpm run dev
```

### Server

Starting the server on localhost:8000

```bash
cd /server
pip install -r requirements.txt
py ./run.py
```

### Database

Starting the database locally

```bash
docker compose -f compose.db.yml up
```

#### Loading data to database

```bash
py scripts/load_sensors.py
py scripts/csvToDb.py
```

### Running python analysis scripts
```bash
cd server/analysis
pip install -r requirements.txt
py *Insert script name*
```

# Visio

Verkkosovellus, joka näyttää kartalla lämpötilojen muutoksen paikkakohtaisesti. Omien antureiden lisäksi tietoja haetaan läheisiltä sääasemilta. Näiltä sääasemilta haetaan myös säätiedot, kuten pilvisyys ja ilmankosteus. Datan analysointiin voidaan luoda haluttuja työkaluja, asiakkaan toiveiden mukaan. Tiedot tallennetaan Google Cloudissa olevaan PostgreSQL tietokantaan.

Sovellus rakennetaan käyttäen Next.js ohjelmistokehystä. Sovelluksen laadun ja toiminnallisuuden takaamiseksi luodaan testit, jotka ajetaan automaattisesti ennen jokaisen uuden version julkaisemista. Asiakkaan toiveen mukaan sovellus voidaan julkaista käyttäen Verceliä tai Google Runia.

## Toiminnallisuudet

- Verkkosovellus
- Sensoreiden sijainnit kartalla
- Sensoreiden Live-data
- Kaavioiden generointi

## Back-end

- PostgreSQL tietokanta
- API tietojen hakemiseen

## Front-end

- Next.js

## Analysointi

- Raaka kosteusdata
- Fast Fourier Transform
- Kausivaihtelu
- Kosteuden muutos
- Lämpötilan muutos
- Kosteuden trendit
- Lämpötilan ja kosteuden korrelaatio
- Päivittäinen lämpötilaero
- Päivittäinen keskilämpötila
- Kuukausittainen yö-lämpötila
- Kuukausittainen minimilämpötila
- Kuukausittainen yö-lämpötilaero
- Päivittäinen keski-kosteus
- Päivittäinen kosteus ero
- Päivä-yö kosteus ero
- Kuukausittainen yö-kosteus
