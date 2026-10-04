# CloseCommonShift

[Кассовый сервер] Закрыть общую смену

Схемы: `schemas/qryCloseCommonShift.xsd`, `schemas/resCloseCommonShift.xsd`
Влияние: **опасно** - необратимые или массовые изменения, блокировка кассы

## Практика

- Закрывает общую смену ресторана. CloseAnyCase="1" - закрыть, даже если смена не открыта.
- Пока смена закрывается, любые запросы получают Query Parse Error "UCSERR(2172): В данный момент закрывается общая смена" - повторите позже.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Manager>? [refItem]  - Менеджер
  <Station>? [refItem]  - Станция
  @CMD: string = "CloseCommonShift"
  @CloseAnyCase: boolean (по умолчанию "false")  - Нужно ли закрывать смену, если она не была открыта. Если 1, то смена будет закрыта, если 0 то будет выдана ошибка 'Нельзя закрыть смену, смена не была открыта'
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Warnings> [normalizedString]  - Предупреждения (некритичные ошибки), которые были при закрытии смены
@CommonShiftNum!: positiveInteger  - Номер смены
@CommonShiftDate!: dateTime  - Логическая дата смены
```

## Пример: CloseCommonShift

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="CloseCommonShift" CloseAnyCase="0">
    <Manager id="{{managerId}}"/>
    <Station id="{{stationId}}"/>
  </RK7CMD>
</RK7Query>
```
