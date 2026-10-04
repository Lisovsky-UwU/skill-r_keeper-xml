# GetEmployeeInfo

[Кассовый сервер] Получить информацию о работнике (права, список обслуживаемых столов)

Схемы: `schemas/qryGetEmployeeInfo.xsd`, `schemas/resGetEmployeeInfo.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Waiter> [refItem]  - Официант
  <Station>? [refItem]  - Станция
  @CMD: string = "GetEmployeeInfo"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Drawer>? [resRefItem]  - Ящик, на который зарегистрирован работник
<OpRights>?  - Список прав на операции
  <oper>*
    @id: positiveInteger  - ID операции
<ObjRights>?  - Список прав на объекты
  <right>*
    @id: positiveInteger  - ID права
<Tables>?  - Список доступных столов
  <table>*
    @id: positiveInteger  - ID стола
<Orders>?  - Список доступных столов
  <Order>*
    @orderIdent!: positiveInteger
    @own_order: boolean  - Флаг "Свой заказ"
```

## Пример: GetEmployeeInfo

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetEmployeeInfo">
    <Waiter id="{{waiterId}}"/>
    <Station id="{{stationId}}"/>
  </RK7CMD>
</RK7Query>
```
