# CloseCardValShift

[Кассовый сервер] Закрытие смены на банковском терминале

Схемы: `schemas/qryCloseCardValShift.xsd`, `schemas/resCloseCardValShift.xsd`
Влияние: **опасно** - необратимые или массовые изменения, блокировка кассы

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  (одно из:)
    <Station> [refItem]  - Станция. Если указана, то смена закрывается на всех терминалах данной станции
    <Device> [refItem]  - Терминал кредитных карт. Если указан, то смена закрывается только на этом терминале
  <Manager> [refItem]  - Менеджер, от имени которого выполняется операция
  @CMD: string = "CloseCardValShift"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Device>* [refItem]  - Терминал кредитных карт, на котором была закрыта смена
```

## Пример: CloseCardValShift

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="CloseCardValShift">
    <Station id="{{stationId}}"/>
    <Manager id="{{managerId}}"/>
  </RK7CMD>
</RK7Query>
```
