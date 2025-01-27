

Proszę opracować schemat bazy danych dla sklepu internetowego.
Baza zawiera informacje o klientach (imię, nazwisko, adres e-mail),
 o produktach oferowanych przez sklep.
  Produkty zawarte są w kilku kategoriach.
   Zamówienie klienta zawiera informację o wybranych produktach i jego stanie realizacji ( zlecenie otrzymane, oczekiwanie na towar, w realizacji, wysłane, anulowane).
Zapytania do bazy danych:

    informacja o stanie realizacji zamówienia: według stanu realizacji, numeru zamówienia lub adresu e-mail klienta,
    informacja pełna o zamówieniu.

Poprawność przedstawionych zapytań przetestować w przykładowej bazie danych.

Należy wykonać diagram encji (wszyskie atrybuty i klucz główny) oraz przedstawić odpowiednie polecenia SQL dla powyższych zapytań do bazy danych. Zadanie będzie omawiane na pierwszych zajęciach w nowym roku.

create view sklep;

create table klient(
    id primary key,
    imie varchar(32),
    nazwisko varchar(64),
    email varchar(128)

) 	

create table produkty(
    id primary key,
    kategoria enum,
    nazwa varchar(255),
    opis varchar(1024),
    cena float


)

create tabl zamowienia(

)

create table zamowienia_klient(
    fore
)