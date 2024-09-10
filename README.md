# Moja štednja

Moja štednja je web aplikacija namijenjena privatnim korisnicima za evidenciju osobne štednje. Aplikacija služi kao fiktivni podračun, omogućujući korisnicima da organiziraju svoju štednju, bilo da se ona nalazi na bankovnom računu ili u gotovini, tako što mogu pratiti namjenu za koju je novac ušteđen ili potrošen.
Korisnici imaju mogućnost unosa, pregleda, uređivanja, brisanja, filtriranja i sortiranja transakcija (uplata i isplata). Aplikacija također prikazuje trenutačni iznos ušteđenog novca, kao i ukupne iznose uplata i isplata.
Podaci o uplatama, isplatama i trenutnoj štednji po namjeni su vizualizirani u obliku tortnih grafova radi boljeg razumijevanja stanja štednje. 

## Funkcionalnosti

### Osnovne funkcionalnosti 
1. Unos transakcija
2. Pregled transakcija
3. Uređivanje transakcija
4. Brisanje transakcija

### Dodatne funkcionalnosti
1. Pregled ukupnog iznosa uplata
2. Pregled ukupnog iznosa isplata
3. Pregled iznosa trenutne štednje
4. Filtriranje transakcija po namjeni
5. Filtriranje transakcija po vrsti transakcije
6. Sortiranje transakcija po iznosu
7. Sortiranje transakcija po datumu
8. Vizualizacija uplata po namjeni
9. Vizualizacija isplata po namjeni
10. Vizualizacija trenutne štednje po namjeni

## Use case dijagram

![Use case diagram](https://github.com/user-attachments/assets/b395b246-97b7-4d47-b137-9bb65d6991df)

## Pokretanje

1. Preuzeti projekt putem terminala naredbom *git clone https://github.com/Calico-san/Moja_stednja.git*
2. Navigirati do direktorija projekta naredbom *cd*
3. Napraviti Docker image naredbom *docker build -t moja_stednja:1.0 .*
4. Pokrenuti Docker container naredbom *docker run -p 5001:8080 moja_stednja:1.0* (**Napomena**: Možete koristiti bilo koji slobodan port na vašem računalu umjesto 5001)
5. Pokrenuti aplikaciju putem Docker Desktop-a ili unosom *localhost:5001* u web preglednik
