# GetDrawerBalance

[Кассовый сервер] Получить остатки денег в ящике

Схемы: `schemas/qryGetDrawerBalance.xsd`, `schemas/resGetDrawerBalance.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Station>? [refItem]  - Станция. Если не задана, то выводятся остатки по всем станциям
  <Drawer>? [refItem]  - Кассовый ящик. Если не задан, то выводятся остатки по всем ящикам
  @CMD: string = "GetDrawerBalance"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Item>* [DrawerRestItem]  - Остатки
  <Station>? [resRefItem]  - Станция, на которую зарегистрирован ящик
  <Drawer>? [resRefItem]  - Ящик
  <Currency> [resRefItem]  - Валюта
  <Printer> [resRefItem]  - Принтер
  @amount: int  - Остаток (в копейках)
```

## Пример: GetDrawerBalance

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetDrawerBalance"/>
</RK7Query>
```
