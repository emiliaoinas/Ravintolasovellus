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

## Sovelluksen tilanne 16.11:
Tällä hetkellä sovelluksessa on mahdollista
- Luoda käyttäjätunnus
- Kirjautua sisään ja ulos
- Tarkastella ravintoloita (eivät tosin vielä ole kartalla, vaan näkyvät listana)
- Lisätä ravintoloita (tämä on vielä avoin kaikille)
- Lukea ja lisätä arvosteluja

Sovelluksesta puuttuu vielä yllämainittuja hakuominaisuuksia, karttaominaisuus ja ylläpitäjän toiminnot. Sovellusta voi testata yllä olevien tiedostojen avulla, ja jotta kaikkia tähän mennessä lisättyjä ominaisuuksia voi käyttää, on luotava käyttäjätunnus ja kirjauduttava sisään.

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
