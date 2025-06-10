# Reisi Eestis: Busside Sõiduplaanid ja Piletite Broneerimine

See projekt on Flaskil põhinev veebirakendus, mis pakub kasutajatele mugavat võimalust otsida, filtreerida ja broneerida bussipileteid Eesti-siseseks reisimiseks. Rakendus hangib bussisõiduplaani andmed välisest API-st ja salvestab need kohalikku andmebaasi, tagades nii kiire andmetöötluse kui ka vähendades välisele teenusele tehtavate päringute arvu.

---
## Andmebaas:
Rakendus sünkroniseerib andmed välise API-ga, tagades alati värskeimad sõiduplaanid ja hinnad. Andmeid säilitatakse lokaalselt SQLite andmebaasis, et vähendada API kutsete arvu ja tagada kiire reageerimine.

---
## Tehniline Ülevaade
+ Backend: Flask (Python): Kergekaaluline ja paindlik veebiraamistik.

+ Andmebaas: SQLite (vaikimisi arenduses, sobib väiksematele rakendustele ja prototüüpimisele).

+ ORM (Object-Relational Mapper): Flask-SQLAlchemy andmebaasi interaktsioonide abstraheerimiseks Pythoni objektideks.

+ Välise API Integratsioon: requests teegi abil andmete hankimiseks Novateri API-st.

+ Keskkonnamuutujad: python-dotenv konfidentsiaalsete andmete turvaliseks haldamiseks.

+ Frontend: HTML, CSS ja Jinja2 (serveripoolne renderdamine)

---
## Tehnilised raskused

Projekti arendamisel oli suurimaks väljakutseks tugeva aluskonstruktsiooni ja tarkvaraarhitektuuri loomine, mis hõlmas Flaski, SQLAlchemy ja SQLite'i integreerimist. Samuti võttis aega Novateri API andmestruktuuri mõistmine ja korrektne integreerimine, et tagada andmete täpne hankimine ja töötlemine. Oluline osa arendusajast kulus ka andmevahetuse nuputamisele frontend ja backend vahel.

---

## Edasised võimalused

+ Hetkel jäi välja ehitamata korralik frontend ning reiside filtreerimine ja broneerimine. See hõlmab reisiotsingute täpsemate filtrite (nt kellaajaline piirang, vahepeatused) lisamist ja nende tõhusat integreerimist andmete kuvamisse. Backendi poolel tähendab see Pythoni funktsioonide loomist, mis suudavad marsruudiandmeid põhjalikult analüüsida ja filtreerida vastavalt kasutaja valikutele.
+ Täieliku Broneerimissüsteemi Rakendamine: Järgmine oluline samm on täieliku piletite broneerimissüsteemi väljaarendamine. See eeldab kasutajale spetsiaalsete broneerimisvormide loomist (kas olemasoleval lehel või eraldi broneerimislehel), vajalike andmete (nt reisija nimi, kontaktandmed) kogumist ning nende turvalist salvestamist andmebaasi. Seejärel tuleks luua "Minu broneeringute" leht, kus kasutajad saaksid vaadata kõiki oma tehtud broneeringuid.
+ Kui rakendus hakkab käitlema suuremat andmemahtu või vajab suuremat jõudlust, saaks migreeruda võimsamale ja skaleeritavamale andmebaasisüsteemile, näiteks PostgreSQL-i või MySQL-i. 

## Kuidas Rakendust Käivitada
Selle projekti käivitamiseks oma kohalikus arenduskeskkonnas järgi alltoodud samme.

1.  **Süsteeminõuded**
Enne alustamist veendu, et sinu süsteemi on paigaldatud:

Python 3.8+: Rakenduse käivitamiseks vajalik Pythoni versioon.

pip: Pythoni standardne paketihaldur sõltuvuste paigaldamiseks.

Git: Versioonihaldustarkvara repositooriumi kloonimiseks.

2. **Repositooriumi Kloonimine**
Alusta projekti koodi hankimisega GitHubist. Ava oma terminal või käsurida ja sisesta:

```
git clone https://github.com/R-Kanne/-Novater-Reisi-Eestis.git
cd kloonitud_repo_kaust
```
3. **Virtuaalse Keskkonna Loomine ja Aktiveerimine**
Virtuaalne keskkond aitab hoida projekti sõltuvused isoleerituna teistest Pythoni projektidest, vältides võimalikke konflikte.

Loo virtuaalne keskkond:
```
python3 -m venv venv
```
Aktiveeri virtuaalne keskkond:

macOS / Linux:
```
source venv/bin/activate
```
Windows (Command Prompt):
```
venv\Scripts\activate
```
Windows (PowerShell):
```
.\venv\Scripts\Activate.ps1
```
4. **Sõltuvuste Paigaldamine**
Kui virtuaalne keskkond on aktiveeritud, paigalda kõik projekti jaoks vajalikud Pythoni teegid, mis on loetletud failis requirements.txt:
```
pip install -r requirements.txt
```
5. **Keskkonnamuutujate Konfigureerimine**
Rakendus vajab toimimiseks konfidentsiaalsete andmete (nt API URL, API kasutajanimi, API parool, Flaski salajane võti) jaoks keskkonnamuutujaid.

Loo projekti põhikausta uus fail nimega .env.  
Näiteks:
```
touch .env
```
Kopeeri järgmised read faili .env ja asenda sulgudes olevad väärtused oma tegelike andmetega. Eelkõige veendu, et API_USERNAME ja API_PASSWORD vastavad sinu Novateri API autentimisandmetele.

FLASK_SECRET_KEY=(sinu_unikaalne_ja_salajane_voti_siia)  
API_USERNAME=(sinu_novater_kasutajanimi)  
API_PASSWORD=(sinu_novater_parool)  
API_URL=https://assignments.novater.com/v1/bus/schedule

6. **Rakenduse Käivitamine**
Nüüd oled valmis rakendust käivitama. Veendu, et oled endiselt virtuaalses keskkonnas, ja käivita:
```
python app.py
```
Pärast rakenduse käivitamist peaksid konsoolis nägema väljundit, mis näitab, et Flaski arendusserver töötab. Tavaliselt on see aadress:
```
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
Ava oma veebibrauser ja navigeeri sellele aadressile (nt http://127.0.0.1:5000/), et rakendust näha.

7. **Andmebaasi Esmakordne Loomine**
Kui käivitad rakendust esmakordselt, loob see automaatselt bus_app.db faili ja vajalikud andmebaasitabelid (PriceSheet, Booking). Konsoolis võid näha teadet andmete hankimise kohta API-st:

No valid price list in DB or all expired. Fetching from API...
Price list [some-uuid-id] saved successfully.

See näitab, et andmed on edukalt laetud ja salvestatud.

