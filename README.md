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
