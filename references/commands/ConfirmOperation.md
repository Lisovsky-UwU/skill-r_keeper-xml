# ConfirmOperation

[Кассовый сервер, Касса] Подвердить выполнение операции, записать операцию в журнал операций

Схемы: `schemas/qryConfirmOperation.xsd`, `schemas/resConfirmOperation.xsd`
Влияние: изменяет данные

## Практика

- Operation - элемент справочника OPERATIONS (ищите по имени через GetRefData RefName="OPERATIONS").

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Operation> [refItem]  - Операция
  <Station> [refItem]  - Станция
  <Manager> [refItem]  - Пользователь, выполняющий операцию
  <Order>? [orderElement]  - Заказ
  <Maket>? [refItem]  - Представление документа для операции
  <Dish>? [menuItem]  - Элемент меню, связанный с операцией
    (refItem: id | code | guid)
    @quantity!: int  - Количество блюда (в тысячных долях)
  @CMD: string = "ConfirmOperation"
  @param: int (по умолчанию "0")  - Параметр операции
  @opengui: boolean (по умолчанию "0")  - Если флаг выставлен и у пользователя нет прав, то запрос перенаправляется на станцию. На станции открывается диалог для подтверждения права на операцию
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Manager>? [refItem]  - Менеджер, который подтвердил операцию
```

## Пример: ConfirmOperation

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="ConfirmOperation" param="0" opengui="0">
    <Operation id="{{operationId}}"/>
    <Station id="{{stationId}}"/>
    <Manager id="{{managerId}}"/>
  </RK7CMD>
</RK7Query>
```
