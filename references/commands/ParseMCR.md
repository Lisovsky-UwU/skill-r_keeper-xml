# ParseMCR

[Касса] Парсинг строки при помощи MCR-алгоритмов

Схемы: `schemas/qryParseMCR.xsd`, `schemas/resParseMCR.xsd`
Влияние: только чтение

## Практика

- Несмотря на пометку [Касса] в XSD, кассовый сервер этот запрос выполняет.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  @CMD: string = "ParseMCR"
  @base64data!: base64binary  - Строка с данными в base64 формате
  @data: normalizedString  - Строка с данными в utf-8. Используется только если не заполнен атрибут base64data
  @devicetype: devicetype (по умолчанию "MAGNETICCARD")  - Тип устройства
  @deviceid: int (по умолчанию "0")  - Номер устройства
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Item>* [ParseItem]
  <MCR> [resRefItem]  - MCR алгоритм
  <Object>? [resRefItem]  - Объект
  @cardCode: normalizedString  - Код карты
  @scope: string {Currency | Employee | Discount | Entrance card | Function Key | Interface | Menu Item | Menu Item Barcode | Dish Control | Order Type}  - Область
```

## Пример: ParseMCR

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="ParseMCR" data="{{cardCode}}" devicetype="Keyboard" deviceid="0"/>
</RK7Query>
```
