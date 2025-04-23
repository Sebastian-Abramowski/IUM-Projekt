## IUM Projekt

## Temat

(_nr. 6_) Serwis Nocarz szczyci się wysoką jakością wsparcia dla oferentów. Wydaje nam się, że przy dodawaniu nowej oferty **nasz serwis powinien sugerować wartość nocy.**

## Definicja problemu biznesowego

**Wielu wynajmujących nie wie, jaką cenę ustalić za noc.**
Ustalają ją "na oko" albo porównują się do innych ofert, ale często popełniają błędy - dają za wysoką cenę (nikt nie rezerwuje) albo za niską (tracą pieniądze).

**Celem projektu jest stworzenie mechanizmu, który inteligentnie zasugeruje sensowną cenę za noc.**

Wdrożenie takiego rozwiązania może przyczynić się do:

- skrócenia czasu potrzebnego na wystawienie oferty

- ujednolicenia poziomu cen na platformie

- zwiększenia liczby rezerwacji dzięki lepszemu dopasowaniu cen do rynku

## Zdefiniowanie zadania modelowania i ogólnych założeń

Celem modelowania jest **zbudowanie systemu, który automatycznie zasugeruje oferentowi cenę za nocleg (w USD) na etapie dodawania nowej oferty.**

Jest to **problem regresji**, ponieważ model ma przewidywać jedną liczbę - wartość ceny - na podstawie zestawu cech opisujących ofertę.

Do trenowania modelu wykorzystamy dane z pliku `listings.csv`, zawierające _ceny bazowe (**price**), które staramy się przewidzieć_, oraz wybrane cechy ofert istotne dla modelowania (np. lokalizacja, typ lokalu, liczba łóżek). Nie będziemy korzystać ze wszystkich dostępnych kolumn.

W projekcie planujemy zastosować **dwa modele:**

- model bazowy: **regresja liniowa** - najprostszy możliwy model regresyjny, który nie wymaga strojenia i pozwala szybko uzyskać pierwsze predykcje

- model docelowy: **Random Forest Regressor** - nieliniowy model, który lepiej uchwyci zależności w danych i powinien zapewnić wyższą jakość predykcji

**Założenia:**

- Model ma przewidywać ogólną, startową cenę za noc - wartość, którą oferent może przyjąć jako domyślną przy dodawaniu oferty

- Cena nie dotyczy konkretnej daty - ma charakter typowy i uśredniony na podstawie podobnych ofert

- Dane treningowe pochodzą z `listings.csv`- zawierają zarówno cechy ofert, jak i ceny bazowe

- Model ma pełnić rolę wspierającą - dostarczać rozsądną sugestię, którą użytkownik może zmienić

## Kryterium sukcesu

Skuteczność modelu ocenimy na dwóch poziomach:

### Jakoś predykcji

Porównamy model bazowy (regresja liniowa) i model docelowy (Random Forest Regressor) na danych testowych, wykorzystując **RMSE (Root Mean Squared Error)** jako podstawową metrykę oceny jakości predykcji.

### Użyteczność dla użytkownika

Ponieważ model ma wspierać wystawiającego przy ustalaniu ceny, **rzeczywistą skuteczność należy ocenić na podstawie zachowania użytkowników.**

Po zamodelowaniu problemu **powinniśmy zapewnić możliwość przeprowadzenia eksperymentu A/B**, w ramach którego użytkownicy otrzymają sugestie cenowe z różnych modeli.

Celem eksperymentu będzie sprawdzenie, jak bardzo wystawiający modyfikują zaproponowaną przez system cenę, w zależności od użytego modelu (bazowego lub docelowego).

**Oczekiwanym rezultatem jest, że użytkownicy rzadziej modyfikują cenę sugerowaną przez model docelowy.**

## Analiza danych z perspektywy realizacji zadań

Planujemy oprzeć modelowanie na danych z pliku `listings.csv`, który zawiera m.in. kolumnę `price`. Zakładamy, że jest to ogólna, deklarowana przez wystawiającego cena bazowa za jedną noc - czyli dokładnie to, co chcielibyśmy sugerować podczas dodawania nowej oferty.

Dla porównania, plik `calendar.csv` zawiera ceny (`price`) przypisane do konkretnych dat. Zakładamy, że jest to rzeczywista cena za noc w określonym miejscu w danym dniu, odzwierciedlająca sezonowość, dostępność i ewentualne zmiany.

Ze względu na to, jakie dane znajdują się w `calendar.csv`, plik ten raczej nie będzie przez nas wykorzystywany - choć musimy się jeszcze upewnić, czy poprawnie interpretujemy znaczenie zawartej tam ceny (`price`) (warto wspomnieć, że wartości te są bardzo zróżnicowane - od kilkudziesięciu do nawet 12 000 dolarów).

Jednym z problemów, który rzuca się w oczy podczas analizy danych, są ogólne **braki w danych** - występują we wszystkich plikach, a szczególnie w listings.csv, który jest kluczowy dla naszego zadania.

Wstępnie przeanalizowaliśmy zawartość pliku `listings.csv` i zidentyfikowaliśmy kilka kolumn, które potencjalnie weźmiemy pod uwagę w naszym modelu:

- **_price_** - cena bazowa za noc, czyli wartość, którą będziemy w przyszłości przewidywać w naszym modelu (target)

- **accommodates** - liczba osób, ktore może pomieścić lokal
- **bedrooms**, **beds** - liczba sypialni i łóżek

Zauważyliśmy, że w niektórych przypadkach dane te są nielogiczne lub niespójne - np. lokal może mieć 2 miejsca dla gości i 17 sypialni, albo 5 miejsc i 8 łóżek. Może to świadczyć o błędach wprowadzania danych lub niestandardowym sposobie ich zliczania.

- **room_type**, **property_type** - typ lokalu i rodzaj obiektu

Na pierwszy rzut oka kolumny te niosą niemal identyczną informację, jednak dane w nich nie zawsze są spójne - zdarzają się przypadki, w których jedna z nich jest pusta, a druga wypełniona. Wymaga to doprecyzowania, czym dokładnie różnią się te pola i skąd wynika ta niespójność.

- **bathrooms** - liczba łazienek

Zauważyliśmy, że w danych pojawiają się wartości niecałkowite, np. 1.5 czy 2.5, których znaczenie nie jest dla nas do końca jasne - może to sugerować niejednoznaczne zasady liczenia łazienek i wymaga doprecyzowania.

- ~~amenities~~ - lista udogodnień dostępnych w ofercie

Choć wydaje się, że kolumna ta mogłaby być przydatna, trudno sensownie z niej skorzystać, ponieważ te same rzeczy są zapisywane na wiele różnych sposobów - np. telewizor może być opisany jako "TV", "50 inch HDTV with standard cable", "HDTV with Netflix, Amazon Prime Video", czy "TV with Apple TV, Disney+, Netflix". Dodatkowo wiele wpisów dotyczy mało istotnych elementów, takich jak "Hangers" czy "Shower gel", co sprawia, że nawet liczba udogodnień nie jest dobrą miarą. Z tego względu kolumna amenities średnio nadaje się do bezpośredniego wykorzystania przy modelowaniu, choć być może warto będzie jeszcze rozważyć jej użycie na późniejszym etapie.

- **minimum_nights**, **maximum_nights** - minimalna i maksymalna liczba nocy możliwa do zarezerwowania

Mogą wskazywać na typ wynajmu (krótkoterminowy vs długoterminowy), choć w danych pojawiają się skrajne wartości (np. minimalna liczba nocy równa 1000), które mogą budzić pewne wątpliwości co do jakości lub interpretacji tych pól.

- ~~number_of_reviews~~, ~~review_scores_rating~~ - liczba opinii oraz ogólna ocena oferty (od 1 do 5)

Atrybuty te mogą mieć sens przy opisie istniejących ofert, ale nie możemy ich wykorzystać w naszym przypadku, ponieważ przy dodawaniu nowej oferty takie informacje jeszcze nie istnieją.

- ~~neighbourhood_cleansed~~ - dzielnica, w której znajduje się lokal. Rozważaliśmy użycie tej kolumny jako wskaźnika lokalizacji, ale ze względu na dużą liczbę unikalnych, niespójnych nazw i brak struktury przestrzennej raczej nie nadaje się do wykorzystania w naszym modelu. Może też powodować problemy, gdy pojawi się nowa dzielnica, której model wcześniej nie widział.
  Kolumny latitude i longitude zawierają współrzędne geograficzne, ale nie dają wprost informacji o jakości lokalizacji - nie wiadomo na ich podstawie, czy lokal znajduje się w centrum, w dzielnicy turystycznej, czy na jego obrzeżach. Uznajemy, że nawet po przetworzeniu trudno byłoby sensownie wykorzystać te dane w naszym modelu, dlatego nie planujemy ich używać.

Po głębszej analizie zauważyliśmy, że wartości w kolumnie **neighbourhood_cleansed** odpowiadają nazwom dzielnic Stambułu. Jeśli faktycznie wszystkie oferty w zbiorze znajdują się w tym mieście, możemy wziąć lokalizację pod uwagę (wtedy możemy je pogrupować do kilku kategorii, np. centrum, dzielnice standardowe, obrzeża). **Żeby to zrobić, potrzebujemy jednak jednoznacznego potwierdzenia, że dane obejmują wyłącznie oferty ze Stambułu.**

Jeśli tak jest, kolumna **neighbourhood_cleansed** może okazać się bardzo wartościową cechą wspierającą nasze modelowanie.

## Ocena wykonalności

Zadanie wydaje się wykonalne, ale przed budową modelu potrzebujemy dokładniej zrozumieć **źródła braków, niespójności i nietypowych wartości w danych**. Konieczne jest również uzyskanie odpowiedzi na kilka **niejasności** oraz potwierdzenie, że przyjęte przez nas **założenia** co do znaczenia wybranych atrybutów są poprawne.

## Implementacja i udostępnienie predykcji

W ramach etapu drugiego planujemy przygotowanie **mikroserwisu**, który będzie wykorzystywany do **serwowania predykcji modelu.**

Mikroserwis będzie przyjmował dane nowej oferty w **formacie JSON** i na ich podstawie zwracał sugerowaną cenę za noc.

Rozwiązanie to umożliwi najpierw porównanie modeli w ramach eksperymentu A/B, a następnie pełne wdrożenie systemu w środowisku produkcyjnym.

## Potencjalne problemy

Dane w `listings.csv` są aktualne (`koniec 2024`), ale z czasem mogą się zdezaktualizować. Model może wymagać ponownego trenowania lub douczenia na nowszych danych, aby utrzymać trafność predykcji.

Dodatkowo, użytkownik powinien być jasno poinformowany, że **sugerowana cena to wstępna propozycja oparta na analizie podobnych ofert**, która nie uwzględnia sezonowości, specjalnych wydarzeń ani dostępności. Brak takiej informacji może prowadzić do niepewności co do sensowności sugerowanej ceny i zniechęcać do jej wykorzystania.

## Terminy

- pierwszy etap: pierwsza iteracja do 25. kwietnia
- drugi etap: do 23. maja
