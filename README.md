## IUM Projekt

## Temat

(_nr. 6_) Serwis Nocarz szczyci się wysoką jakością wsparcia dla oferentów. Wydaje nam się, że przy dodawaniu nowej oferty **nasz serwis powinien sugerować wartość nocy.**

## Definicja problemu biznesowego

**Wielu wynajmujących nie wie, jaką cenę ustalić za noc.**
Ustalają ją "na oko" albo porównują się do innych ofert, ale często popełniają błędy – dają za wysoką cenę (nikt nie rezerwuje) albo za niską (tracą pieniądze).

**Celem projektu jest stworzenie mechanizmu, który inteligentnie zasugeruje sensowną cenę za noc.**

Wdrożenie takiego rozwiązania może przyczynić się do:

- skrócenia czasu potrzebnego na wystawienie oferty

- ujednolicenia poziomu cen na platformie

- zwiększenia liczby rezerwacji dzięki lepszemu dopasowaniu ceny do rynku

## Zdefiniowanie zadania modelowania i wszystkich założeń

Celem modelowania jest **zbudowanie systemu, który automatycznie zasugeruje oferentowi cenę za nocleg (w USD) na etapie dodawania nowej oferty.**

Jest to **problem regresji**, ponieważ model ma przewidywać jedną liczbę – wartość ceny – na podstawie zestawu cech opisujących ofertę.

Do trenowania modelu wykorzystamy dane z pliku `listings.csv`, zawierające _ceny bazowe (price), które staramy się przewidzieć_, oraz wybrane cechy ofert istotne dla modelowania (np. lokalizacja, typ lokalu, liczba łóżek). Nie będziemy korzystać ze wszystkich dostępnych kolumn.

W projekcie planujemy zastosować **dwa modele:**

- model bazowy: **regresja liniowa** - najprostszy możliwy model regresyjny, który nie wymaga strojenia i pozwala szybko uzyskać pierwsze predykcje

- model docelowy: **Random Forest Regressor** – nieliniowy model, który lepiej uchwyci zależności w danych i powinien zapewnić wyższą jakość predykcji

**Założenia:**

- Model ma przewidywać ogólną, startową cenę za noc – wartość, którą oferent może przyjąć jako domyślną przy dodawaniu oferty

- Cena nie dotyczy konkretnej daty – ma charakter typowy i uśredniony na podstawie podobnych ofert

- Dane treningowe pochodzą z `listings.csv`- zawierają zarówno cechy ofert, jak i ceny bazowe

- Model ma pełnić rolę wspierającą – dostarczać rozsądną sugestię, którą użytkownik może zmienić

## Kryterium sukcesu

Skuteczność modelu ocenimy na dwóch poziomach:

### Jakoś predykcji

Porównamy model bazowy (regresja liniowa) i model docelowy (Random Forest Regressor) na danych testowych, wykorzystując **RMSE (Root Mean Squared Error)** jako podstawową metrykę oceny jakości predykcji.

### Użyteczność dla użytkownika

Ponieważ model ma wspierać oferenta przy ustalaniu ceny, rzeczywistą skuteczność należy ocenić na podstawie zachowania użytkowników.

Po zamodelowaniu problemu **powinniśmy zapewnić możliwość przeprowadzenia eksperymentu A/B**, w ramach którego użytkownicy otrzymają sugestie cenowe z różnych modeli.

Celem eksperymentu będzie sprawdzenie, jak bardzo wystawiający modyfikują zaproponowaną przez system cenę, w zależności od użytego modelu (bazowego lub docelowego).

## Analiza danych z perspektywy realizacji zadań

Z otrzymanych plików interesują nas pliki `calender` i `listings`

Odnośnie pliku calender:

- Nie znamy kontekstu przechowywanych informacji, czy jest to zapis wszystkich dni dla każdego lokalu i ich dostępności tego konretnengo dnia?
- Kolumna available zawiera wartości t/f, ale nie jest jasne, czy dotyczą one dostępności konkretnego dnia (date) czy ogólnej dostępności oferty.
- Kolumna adjusted_price jest w większości pusta – nie wiadomo, czym różni się od price.
- Kolumny minimum_nights i maximum_nights są niejednoznaczne – nie wiadomo, czy odnoszą się do całej oferty czy tylko do konkretnego dnia.
- Wartość price wygląda na cenę za noc dla danego dnia (date), czy jest to prawda? Niektóre ceny są wyjątkowe wysokie (12000$ za jedną noc) nie jest to błąd?

Odnośnie pliku listings:

- Niewiemy co oznacza price, i czym się różni się od 'price' w calender
- Niewiemy co oznaczają kolumny: host_location, host_is_superhost, host_neighbourhood, hoste_acceptance_rate, host_is_superhost, accommodates review_scores_accuracy, review_scores_cleanliness, review_scores_checkin, review_scores_communication, review_scores_location, review_scores_value, license, minimum_nights, maximum_nights, minimum_minimum_nights, maximum_minimum_nights, minimum_maximum_nights, maximum_maximum_nights, minimum_nights_avg_ntm, maximum_nights_avg_ntm, calendar_updated, has_availability, availability_30, availability_60, availability_90, availability_365, license, instant_bookable

W danych są liczne braki (pojedyńcze komórki są puste).

Dane pozwalają na rozpoczęcie pracy, ale będziemy je jeszcze czyścić i przekształcać.

## Terminy

- pierwszy etap: pierwsza iteracja do 25. kwietnia
- drugi etap: do 23. maja
