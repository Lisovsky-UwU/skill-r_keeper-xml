# OpenBottle

[Кассовый сервер] Открыть бутылку в системе учёта алкоголя (например SH5) с 7.7.0.347

Схемы: `schemas/qryOpenBottle.xsd`, `schemas/resOpenBottle.xsd`
Влияние: изменяет данные

## Практика

- Нужен настроенный сервис учета алкоголя (например StoreHouse); без него - "Сервис учёта алкоголя не доступен" (RK7ErrorN 8007).

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
(одно из:)
  <RK7CMD> [OpenBottleCommand]
    <Order>? [orderElement]  - Заказ, используется только для нужд внутреннего контроля лицензирования, заказ не обязан существовать
    <OrderCategory>? [refItem]  - Категория заказа, не обязательная
    <Station> [refItem]  - Станция
    <Mark> [base64Binary]  - марка в формате base64
    @CMD: string = "OpenBottle"
    @gtin!: gtinString  - ГТИН бутылки
    @volume: nonNegativeInteger  - объём в ранее открытой бутылке, в миллилитрах
    @isOld: boolean  - признак, что бутылка вскрыта до 1.7.2024
    @* - допускаются любые другие атрибуты
  <RK7Command>+ [OpenBottleCommand] (структура - см. выше)
  <RK7Command2>+ [OpenBottleCommand] (структура - см. выше)
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Bottle>?
  @name: normalizedString  - наименование бутылки (из ЕГАИС)
  @bottleVolume: nonNegativeInteger  - объём бутылки в миллилитрах
```

## Пример: OpenBottle

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="OpenBottle" gtin="{{gtin}}">
    <Station id="{{stationId}}"/>
    <Mark>{{markingData}}</Mark>
  </RK7CMD>
</RK7Query>
```
