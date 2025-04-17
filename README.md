## IUM Projekt

Temat: 6. Serwis Nocarz szczyci się wysoką jakością wsparcia dla oferentów. Wydaje nam się, że
przy dodawaniu nowej oferty nasz serwis powinien sugerować wartość nocy.

## Definicja problemu biznesowego
Wielu oferentów, czyli osób wynajmujących lokale, nie wie, jaką cenę ustalić za noc.
Ustalają ją "na oko" albo porównują się do innych ofert, ale często popełniają błędy – dają za wysoką cenę (nikt nie rezerwuje) albo za niską (tracą pieniądze).
Naszym celem jest zbudowanie mechanizmu, który pomoże im ustalić sensowną cenę, poprzez inteligentne sugerowanie ceny za noc.
Wprowadzenie takiej funkcjonalności może:
skrócić czas wystawiania ofert,
ujednolicić poziom cen na platformie,
i sprawić, by więcej osób przeglądających ofertę faktycznie ją rezerwowało

## Zdefiniowanie zadania/zadań modelowania i wszystkich założeń
Zadanie traktujemy jako problem regresji, czyli przewidywania liczby - w tym przypadku ceny za jedną noc.
Model ma na wejściu informacje o ofercie (np. typ pokoju, liczba osób, lokalizacja, termin) i zwraca sugerowaną cenę.

Założenia:
Cena, którą przewidujemy, dotyczy jednej nocy dla konkretnego dnia.
Model ma uczyć się na danych historycznych (oferty + kalendarz z cenami).

Głównym celem modelowania jest stworzenie systemu, który na podstawie danych z nowej oferty (takich jak lokalizacja, liczba miejsc, udogodnienia, standard, typ obiektu itd.)
będzie automatycznie sugerować proponowaną cenę za noc.

## Kryterium sukcesu
Za sukces uznajemy to, że model dobrze przewiduje ceny – czyli jego błąd (np. średni błąd bezwzględny, MAE) jest mały.
Na początek zbudujemy model bazowy – np. taki, który przewiduje średnią cenę dla danego typu pokoju i lokalizacji.
Potem zbudujemy model docelowy – bardziej zaawansowany (np. XGBoost, las losowy), który powinien dawać lepsze wyniki. Sukcesem będzie, jeśli ten drugi model będzie wyraźnie lepszy niż bazowy.
### Biznesowe:
Minimum 75% oferentów akceptuje sugerowaną cenę bez modyfikacji.
Wyższa konwersja rezerwacji dla ofert korzystających z sugerowanej ceny.

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

- pierwszy etap: do 25. kwietnia
- drugi etap: do 23. maja
