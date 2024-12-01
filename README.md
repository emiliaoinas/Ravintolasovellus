# Ravintolasovellus

Tämä on harjoitustyö kurssille Tietokannat ja web-ohjelmointi. Sovelluksessa on kartta, jossa näkyy alueen ravintolat, joita käyttäjä voi klikata ja lukea tietoa ja arvosteluja niistä.

Sovellukseen kuuluvia perustoimintoja:
- Tunnuksen luominen
- Sisään- sekä uloskirjautuminen
- Ravintoloiden näkyminen kartalla ja klikatessa tiedon saaminen
- Mahdollisuus arvostella ravintoloita ja lukea muiden arvosteluja
- Ravintoloiden etsiminen tietyn hakusanan avulla
- Mahdollisuus nähdä ravintolat listattuna niiden arvioiden mukaan
  
Tämän lisäksi ylläpitäjät voivat: 
- Lisätä ja poistaa ravintoloita
- Valita mitä tietoja näytetään
- Poistaa annettuja arviointeja
- Luoda erilaisia ryhmiä, joihin ravintolat on luokiteltu

## Sovelluksen tilanne 1.12.
Tällä hetkellä sovelluksessa on mahdollista
- Luoda käyttäjätunnus
- Kirjautua sisään ja ulos
- Tarkastella ravintoloita kartalla ja päästä linkin kautta ravintolan sivuille klikkaamalla kohdetta kartalla
- Lukea ja lisätä arvosteluja
- Hakea ylläpitäjäksi

Ylläpitäjät voivat myös
- Lisätä ravintoloita
- Poistaa arviointeja

Sovelluksesta puuttuu vielä
- Ravintoloiden poistaminen ja haluttujen tietojen piilottaminen
- Ravintoloiden etsiminen hakusanan avulla ja mahdollisuus nähdä ravintolat listattuna
- Ryhmät, joihin ravintolat on luokiteltu

Myös sivujen ulkoasu on kesken, ja se on vielä yksinkertaisessa muodossa.

## Sovelluksen käyttöohjeet
1. Kloonaa repositorio koneellesi ja luo samaan kansioon .env-tiedosto, joka sisältää nämä:
   ```
   DATABASE_URL=<tietokannan-paikallinen-osoite>
   SECRET_KEY=<salainen-avain>
   ```
2. Lataa Python3, jonka jälkeen aktivoi virtuaaliympäristö näillä komennoilla:
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Asenna riippuvuudet komennolla `pip install -r ./requirements.txt`
4. Luo PostgreSQL-tietokanta ja määritä skeema komennolla `psql < schema.sql`
5. Käynnistä sovellus komennolla `flask run`
6. Luo käyttäjätunnus tai kirjaudu sisään.
7. Lähetä ylläpitäjähakemus voidaksesi lisätä uusia ravintoloita ja voidaksesi testata kaikkia toiminnallisuuksia.
