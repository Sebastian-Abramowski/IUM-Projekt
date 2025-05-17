## Eksperyment A/B

W ramach kolejnego etapu projektu naszym zadaniem było umożliwienie przeprowadzenia eksperymentu A/B,
który pozwala porównać jakość działania dwóch modeli predykcyjnych:
modelu bazowego (`Linear Regression`) oraz modelu zaawansowanego (`Random Forest`).

Dzięki temu możliwe było sprawdzenie, jak oba modele radzą sobie w warunkach produkcyjnych
oraz który z nich generuje bardziej trafne i stabilne predykcje.

### Mikroserwis

W celu przeprowadzenia eksperymentu A/B przygotowaliśmy prosty mikroserwis,
który obsługuje proces serwowania predykcji oraz zapisywania wyników potrzebnych do analizy.

Na początku zaimplementowaliśmy endpointy do testowego serwowania predykcji
z trzech modeli (`dummy, base, advanced`), aby upewnić się,
że modele są poprawnie deserializowane i zwracają różne wartości predykcji.

Następnie rozszerzyliśmy mikroserwis o właściwe endpointy pozwalające
na przeprowadzenie eksperymentu A/B, w którym predykcja wykonywana jest losowo
jednym z dwóch modeli (`Linear Regression lub Random Forest`),
a następnie zapisywana wraz z informacją o ostatecznej decyzji cenowej.

### Jak krok po kroku przeprowadzić eksperyment A/B?

Zasymulowaliśmy przeprowadzanie eksperymentu A/B przy użyciu `Postmana` w następujący sposób:

1. Wysłanie żądania, aby uzyskać predykcję z losowo wybranego modelu, podając określone zmienne wejściowe w ciele żądania,

<img src="./figures/ab/GET_prediction.png" alt="get_prediction" width="500"/>

</br>

2. Wysłanie żądania, aby ustawić ostateczną cenę, podając identyfikator wcześniej uzyskanej predykcji,

<img src="./figures/ab/POST_set_price.png" alt="set_price" width="500"/>

</br>

3. Powrót do kroku 1, jeśli potrzebujemy zebrać więcej danych,

</br>

4. Wysłanie żądania, aby uzyskać podsumowanie eksperymentu A/B.

<img src="./figures/ab/GET_summary.png" alt="get_summary" width="500"/>

### Analiza

Poza wcześniejszym podsumowaniem przygotowaliśmy również prostą wizualizację
wyników sztucznego eksperymentu A/B - wykres boxplot,
który pokazuje rozkłady błędów predykcji dla obu modeli.

<img src="./figures/ab/ab_boxplot.png" alt="ab_boxplot" width="500"/>

W przypadku rzeczywistego eksperymentu A/B sprawdzilibyśmy dodatkowo,
czy uzyskane rozkłady błędów dla obu modeli mają charakter normalny,
a także przeprowadzilibyśmy testy statystyczne (np. test t-Studenta),
aby upewnić się, że zaobserwowane różnice w skuteczności modeli nie wynikają z przypadku.

### Przechowywanie danych eksperymentu

Dane z eksperymentu A/B przeechowywane są w dwóch tabelach `Predction` oraz `Decision`

Przykład danych:

- tabela `Predicton`

![prediction_data_example](./figures/ab/prediction_table_example.png)

- tabela `Decision`

![decision_data_example](./figures/ab/decision_table_example.png)
