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

# Tietokanta
Postgres tietokanta käynnistetään docker säiliössä komennolla:<br>
`docker run --name my-postgres -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydatabase -p 5432:5432 -d postgis/postgis`<br>
Korvaa my- alkuiset syötteet omillasi.

Luodun ympäristön voi tuhota näin:<br>
1. `docker stop my-postgres`
2. `docker rm my-postgres`<br>
3. Jos tallensit dataa volumeen, saat sen poistettua komennolla:<br>
`docker volume prune`<br>
Tämä poistaa kaikki volumet, joilla ei ole assosiaatiota käynnissä olevaan tai pysäytettyyn docker säiliöön.

Tietokannan terminaaliin pääsee käsiksi näin:<br>
`docker exec -it my-postgres psql -U myuser -d mydatabase`<br>
my- alkuiset syötteet korvaat omillasi.
