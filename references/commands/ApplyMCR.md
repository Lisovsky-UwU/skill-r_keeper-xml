# ApplyMCR

[Касса] Применение MCR-алгоритмов к кассе (эмуляция прокатывания карты)

Схемы: `schemas/qryApplyMCR.xsd`, `schemas/resApplyMCR.xsd`
Влияние: изменяет данные

## Практика

- Выполняется XML-интерфейсом самой кассы: кассовый сервер отвечает "Unknown command ApplyMCR".

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  @CMD: string = "ApplyMCR"
  @data!: normalizedString  - Строка с данными
  @devicetype!: deviceType {MagneticCard | Keyboard | Dallas | BarCode | NoTouche}  - Тип устройства
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
  @Processed: boolean  - Результат обработки алгоритма (1 - обработан, 0 - не обработан)
```

## Пример: ApplyMCR

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="ApplyMCR" data="{{cardCode}}" devicetype="Keyboard" deviceid="0"/>
</RK7Query>
```
