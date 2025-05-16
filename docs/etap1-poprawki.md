# Poprawki po oddaniu etapu 1

### Trzymanie danych w repozytorium

Uwaga:

```
- dane nie powinny być trzymane w repozytrium ze względu na możliwość otrzymania ogromnych ilości danych, z czym normalne repozytorium po przekroczeniu pewnej granicy sobie nie poradzi
```

Poprawka:

- Usunęliśmy pliki danych z repozytorium

---

## Modelowanie

Uwaga:

```
- ustalone analityczne kryterium sukcesu powinno być jakoś oparte o dostępne dane

(przy wstępnym modelowaniu warto "wrzucić" dane w prosty model i zobaczyć jakie wyniki osiągamy - pozwala to na określenie sensownego baseline'u dla problemu)
```

Poprawka:

### Model naiwny

Zastosowaliśmy model naiwny, który zawsze zwraca ten sam wynik. Zwraca on medianę zmiennej celu (`price`) ze zbioru treningowego, niezależnie od zmiennych wejściowych. Służy jako punkt odniesienia dla oceny skuteczności innych modeli.

Wyniki modelu naiwnego na zbiorze testowym:

- MAE: `2138.67`
- RMSE: `4282.36`

### Model bazowy

Zastosowaliśmy model bazowy, który jest modelem regresji liniowej. Dla zmiennych kategorycznych zastosowaliśmy kodowanie one hot, a zmienne liczbowe zostały przeskalowane.

Wyniki modelu bazowego na zbiorze testowym:

- MAE: `2478.52`
- RMSE: `4071.42`

### Pierwsza wersja modelu zaawansowanego

Z ciekawości przetestowaliśmy również pierwszą wersję bardziej zaawansowanego modelu, który powinien potrafić rozpoznać nieliniowe zależności - zastosowaliśmy regresję Random Forest.

DLa zmiennych kategorycznych zastosowaliśmy kodowanie one hot, a zmienne liczbowe nie zostały przeskalowane.

Wyniki modelu zaawansowanego na zbiorze testowym:

- MAE: `1912.86`
- RMSE: `3466.67`

Wyniki modelu zaawansowanego na zbiorze testowym po lekkich transformacjach danych i dobraniu hiperparametrów:

- MAE: `1841.32`
- RMSE: `3379.44`

Wnioski:

Wydaje się, że trudno będzie z dostępnych danych zbudować dobrą i użyteczną predykcję. Albo dane są niewystarczające, żeby uzyskać model wyraźnie lepszy od modelu naiwnego, albo my jesteśmy bezużyteczni w naszych próbach.

---

### Wątpliwości co do zmiennej celu `price`

Początkowo uznaliśmy, że `price` z pliku `listings.txt` to cena za noc ustalana przez wystawiającego ofertę — pasuje to do kontekstu zadania. Jednak po zastosowaniu pierwszych modeli i późniejszej analizie danych zauważyliśmy, że wartości tej zmiennej są bardzo wysokie. Budzi to nasze wątpliwości: może to cena za kilka nocy, może dane są błędne, a może mamy do czynienia z bardzo luksusowymi ofertami.

Na tym etapie, z braku lepszej opcji, zakładamy roboczo, że `price` to cena za jedną noc.

---

Uwaga:

```
- ustalone kryteria sukcesu - piszecie Państwo o dwóch kryteriach sukcesu, ale nie wiadomo co to za kryteria
- jak porównuje się zaproponowane kryterium sukcesu do modelu naiwnego (zwracającego zawsze taki sam wynik)?
- jakie jest biznesowe kryterium sukcesu?
- jakie jest analityczne kryterium sukcesu?
- jaka jest akceptowalna wartość proponowanej metryki w analitycznym kryterium sukcesu?
```

Poprawka:

#### Analityczne kryterium sukcesu

Jako metrykę oceny jakości predykcji przyjmujemy RMSE (Root Mean Squared Error),
mierzy ona średni błąd predykcji i kładzie większy nacisk na duże odchylenia.

Za sukces analityczny uznajemy sytuację, w której model osiąga RMSE mniejsze niż model naiwny (4282.36) oraz model bazowy (4071.42).

#### Biznesowe kryterium sukcesu

Biznesowe kryterium sukcesu opieramy na wyniku eksperymentu A/B, w którym użytkownicy będą losowo otrzymywać sugerowaną cenę z modelu bazowego lub modelu zaawansowanego.

Za sukces uznajemy sytuację, w której średnia zmiana ceny wprowadzana przez użytkowników po otrzymaniu sugestii z modelu zaawansowanego jest mniejsza niż w przypadku modelu bazowego, a także gdy średnia modyfikacja ceny nie przekracza 20% względem wartości zaproponowanej przez model zaawansowany.

---

Uwaga:

```
- jakie (wstępnie) będą dane wejściowe?
```

Poprawka:

Dane, które planujemy wykorzystać jako zeminne wejściowe (features) dla naszego modelu to:

- accommodates - liczba osób, które może pomieścić lokal

- bedrooms, beds - liczba sypialni i łóżek

- room_type, property_type - typ lokalu i rodzaj obiektu

- bathrooms - liczba łazienek

- minumum_nights - minimalna liczba nocy do zarezerwowania

- neighbourhood_cleaned - dzielnica Stambułu, w której znajduje się lokal

---

## Analiza dostarczonych danych

### Rozkłady kluczowych atrybutów

Uwaga:

```
- jak wyglądają rozkłady kluczowych do realizacji projektu atrybutów?

(dla atrybutów dyskretnych można zrobić wykresy słupkowe z liczbą wystąpień, a dla ciągłych wykresy estymowanego rozkładu; w szczególności w drugim przypadku pozwala to na lepsze zrozumienie wartości danych, które pojawiają się w zbiorze)
```

Poprawka:

### Ilość braków

Uwaga:

```
- nie pojawiają się konkretne informacje o ilości braków
```

Poprawka:

### Zależność między zmiennymi wejściowymi a zmienną celu

Uwaga:

```
- czy jesteście Państwo pewni, że zmienne wejściowe niosą jakąś informację o zmiennej celu?
```

Poprawka:

---

### Raczej tu będzie po prostu analiza danych, nie problemów


### Dodatkowe zbadanie naszych wcześniej zauważonych błędów z danymi

Poniżej analizujemy problemy, które zauważyliśmy już w poprzednim etapie, ale wtedy nie potwierdziliśmy w żaden sposób naszych obserwacji za pomocą wykresów.

#### Zależność liczby sypialni a łóżkami

Tak jak na oko udało nam się zauważyć, jest pewna niekonsekwencja w danych. Szczególnie to widać w przypadku jak mamy mniej łóżek niż sypialni.



#### Zależność między liczbą łóżek a liczbą osób, które może pomieścić mieszkanie

Wykres, które sporządziliśmy, także potwierdza problem, który zauważliśmy. Dane nie do końca są spójne. Liczba łóżek i liczba osób powinna być bardzo podobna, przynajmniej się tak wydaje.

#### Jaki wartości ma zmienna bathrooms

Tak jak to wcześniej zauważyliśmy, jest dużo wartóści, które nie wydają się być sensowne. Część danych ma liczbę łazienek jako liczbę niecałkowitą, co nie ma sensu.


#### Kolumna amenties

Potwierdziliśmy, że jest bardzo dużo unikalnych wartości 2057. Trzy najczęstsze udogodnienia to: Wifi, Kitchen, Hair dryer. Tak jak ustaliliśmy, trzeba byłoby włożyć dużo pracy aby te dane jakoś znormalizować, ponieważ są one w różnej formie oraz różne rzeczy ludzie wpisują w udogodnienia.

#### Kolumna neighbourhood_cleaned

Tak jak wcześniej zauważyliśmy, dane przedstawiają wszystkie dzielnice Stambułu (39).
Dla bardziej popularnych dzielnic jest bardzo dużo danych. Dane wydają się być bardzo sensowne.























