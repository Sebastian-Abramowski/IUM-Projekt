# Przewidywanie ceny noclegu (IUM 2025L)

Celem było przewidywanie sugerowanej ceny za noc w serwisie rezerwacji noclegów.  

Praca miała formę **symulowanego zlecenia komercyjnego** – prowadzący wcielał się w rolę klienta, z którym nawiązywaliśmy regularny kontakt w celu uzyskania danych, zgłaszania problemów oraz konsultowania postępów.  

Zakres prac obejmował analizę problemu i dostępnych danych, ich czyszczenie i wstępne przetwarzanie, ekstrakcję i inżynierię cech, budowę oraz ocenę modeli ML w Pythonie z wykorzystaniem **scikit-learn**, a następnie implementację mikroserwisu w **FastAPI** do serwowania predykcji. Mikroserwis umożliwia przeprowadzanie eksperymentów A/B.  

## Struktura repozytorium

- **`docs/`** – `etap1.md` zawiera analizę problemu i danych, `etap1-poprawki.md` opisuje poprawki po otrzymaniu feedbacku, a pozostałe pliki obejmują analizę nowych danych oraz raport ze sztucznego eksperymentu A/B  
- **`microservice/`** – kod mikroserwisu FastAPI obsługującego predykcje oraz eksperymenty A/B  
- **`notebooks/`** – notebooki z analizą danych, przygotowaniem cech oraz trenowaniem modeli ML  
