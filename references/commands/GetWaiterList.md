# GetWaiterList

[Кассовый сервер] Получить список официантов, работающих со столом

Схемы: `schemas/qryGetWaiterList.xsd`, `schemas/resGetWaiterList.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Table> [refItem]  - Стол
  @CMD: string = "GetWaiterList"
  @registeredOnly: boolean  - Флаг - вернуть всех работников (0), или только зарегистрированных в смене (1)
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Waiters>
  <waiter>*
    <Drawer>? [resRefItem]  - Ящик, на который зарегистрирован работник
    <Station>* [resRefItem]  - Текущая касса, на которой залогинен работник
    @ID: positiveInteger  - ID работника
    @Code: positiveInteger  - Код работника
```

## Пример: GetWaiterList

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetWaiterList" registeredOnly="0">
    <Table id="{{tableId}}"/>
  </RK7CMD>
</RK7Query>
```
