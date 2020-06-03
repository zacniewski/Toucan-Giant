# Toucan-Giant

## Uruchomienie i obsługa projektu
  * Aktywujemy odpowiednie środowisko wirtualne condy - ```conda activate job_manager```, 
  * przechodzimy do '/home/toucan/Downloads/-TE-Tools/Toucan-Giant' i wydajemy komendę ```python manage.py runserver 0.0.0.0:8000```,
  * IP Giant'a to 20.20.1.188 i taki adres wpisany jest w pliku setting.py,
  * aby połączyć się z serwerem z innego komputera, wpisujemy w przeglądarce ```20.20.1.188:8000```,
  * pliki .wav kopiujemy do folderu ```data_dir```,
  * w sekcji 'Wave text editor' dostępna jest lista wszystkich plików .wav oraz tekstów dotyczących danego nagrania,
  * przycisk edycji dostępny jest dla tekstu przed normalizacją, po kliknięciu mamy dostęp do nagrania oraz tekstu z nim związanego,
  * gdy jesteśmy pewni, że tekst jest zgodny z nagraniem, klikamy czerwony przycisk,
  * na liście plików status powinien zostać zmieniony z 'False' na 'True'.
  
## Panel admina
  * Login i hasło to ```nvidia```,
  * ścieżka do pliku CSV dodawana jest w sekcji 'Pliki CSV',
  * na teraz najlepszą opcją jest, aby była tam dodana jedna ścieżka,
  * sekcja 'Teksty w plikach wave' zawiera informacje o poszczególnych rekordach w bazie danych,
  * gdy skończymy pracę z jednym datasetem, a chcemy zacząć z drugim:
       * usuwamy poprzednie pliki .wav i .csv z foldera 'data_dir',
       * kopiujemy do ww. foldera nowe pliki,
       * dodajemy nową śćieżkę do pliku CSV w sekcji 'Pliki CSV'.
  * w sekcji 'Pliki CSV' mamy dwa przyciski:
       * do wypełniania bazy danych SQLite danymi z pliku (stosujemy przy pustej bazie danych),
       * do generowania nowego pliku CSV, zawierającego dane z ww. bazy danych (tworzony jest nowy plik CSV z nową nazwą),
       * używać ostrożnie!   
  * w panelu (najwygodniejsza i najbezpieczniejsza opcja) możemy usunąć zarówno strtowy plik CSV jak i dane z bazy, dotyczące nagrań:
       * robimy to po zakończeniu pracy z danym datasetem.
       
## Koniec pracy
  * zatrzmujemy serwer w konsoli (Ctrl + C),
  * deaktywujemy środowisko wirtualne condy - ```conda deactivate```.
  
