# CloseCashShift

[Кассовый сервер] Закрыть кассовую смену

Схемы: `schemas/qryCloseCashShift.xsd`, `schemas/resCloseCashShift.xsd`
Влияние: **опасно** - необратимые или массовые изменения, блокировка кассы

## Практика

- Закрывает кассовую смену станции и печатает сменный отчет.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Station> [refItem]  - Станция
  <Manager> [refItem]  - Менеджер
  <Maket>? [refItem]  - Макет сменного отчета
  @CMD: string = "CloseCashShift"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
@CommonShiftNum!: positiveInteger  - Номер смены
@CommonShiftDate!: dateTime  - Логическая дата смены
```

## Пример: CloseCashShift

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="CloseCashShift">
    <Station id="{{stationId}}"/>
    <Manager id="{{managerId}}"/>
  </RK7CMD>
</RK7Query>
```
