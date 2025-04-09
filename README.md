# Startup

## Docker compose

All parts of the project can be started with docker compose. Compose starts the Client, server and database.

```bash
docker-compose up
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
py *Insert script name*
```

# Visio

Verkkosovellus, joka näyttää kartalla lämpötilojen muutoksen paikkakohtaisesti. Omien antureiden lisäksi tietoja haetaan läheisiltä sääasemilta. Näiltä sääasemilta haetaan myös säätiedot, kuten pilvisyys ja ilmankosteus. Datan analysointiin voidaan luoda haluttuja työkaluja, asiakkaan toiveiden mukaan. Tiedot tallennetaan Google Cloudissa olevaan PostgreSQL tietokantaan.

Sovellus rakennetaan käyttäen Next.js ohjelmistokehystä. Sovelluksen laadun ja toiminnallisuuden takaamiseksi luodaan testit, jotka ajetaan automaattisesti ennen jokaisen uuden version julkaisemista. Asiakkaan toiveen mukaan sovellus voidaan julkaista käyttäen Verceliä tai Google Runia.

## Toiminnallisuudet

- Sää-datan tallennus Google Cloudiin
- Lämpötilan ja sen muutoksen visualisointi kartalle (Websovellus)
- Lämpötilakartan ajankohdan dynaaminen liukusäädin
- Versionhallinta (Github)

## Back-end

- PostgreSQL tietokanta
- API tietojen hakemiseen
- Testaus ja CI/CD (GitHub Actions / joku muu)

## Front-end

- Next.js
- Lämpötilan visualisointi kartan päälle
- Eri sääasemien datan näyttämistä

## Analysointi

- Analysointi selviää tavoitteiden määrittämisen jälkeen.
- Knime tai joku muu soveltuva teknologia
