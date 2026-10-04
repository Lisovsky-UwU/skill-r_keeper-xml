# GetSystemInfo2

[Касса, Кассовый сервер] Получить инфо о программе

Схемы: `schemas/qryGetSystemInfo2.xsd`, `schemas/resGetSystemInfo2.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  @CMD: string = "GetSystemInfo2"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<SystemInfo>
  <Cash>? [refItem]  - Касса (заполняется, если запрос вызван для кассы)
  <CashGroup> [refItem]  - Кассовый сервер
  <Restaurant> [refItem]  - Ресторан
  <Waiter>? [refItem]  - Текущий пользователь (заполняется, если запрос вызван для кассы)
  <CommonShift> [CommonShift]  - Общая смена
    @ShiftDate: dateTime  - Логическая дата смены
    @ShiftNum: int  - Номер смены
    @ShiftStartTime: dateTime  - ДатаВремя начала смены
  @ProcessID: int  - Идентификатор процесса
  @RestCode: int  - Код ресторана
  @uptime: dateTime  - Время работы программы
```

## Пример: GetSystemInfo2

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetSystemInfo2"/>
</RK7Query>
```
