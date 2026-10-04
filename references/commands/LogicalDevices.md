# LogicalDevices

Список загруженных драйверов на станции, запрос можно выполнять на любой санции и на любом кассовом сервере

Схемы: `schemas/qryLogicalDevices.xsd`, `schemas/resLogicalDevices.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
(одно из:)
  <RK7CMD> [LogicalDevices]
    <Station> [refItem]  - Станция, с которой надо запросить список устройств"
    @CMD: string = "LogicalDevices"
  <RK7Command>+ [LogicalDevices] (структура - см. выше)
  <RK7Command2>+ [LogicalDevices] (структура - см. выше)
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<LogicalDevices>
  <LogicalDevice>*
    (resRefItem: id | code | guid)
    @modClass: nonNegativeInteger
    @guid: normalizedString
    @driver: string
    @number: nonNegativeInteger
```

## Пример: LogicalDevices

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="LogicalDevices">
    <Station id="{{stationId}}"/>
  </RK7CMD>
</RK7Query>
```
