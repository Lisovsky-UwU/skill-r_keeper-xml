# GetEmployeeInfo2

[Касса,Кассовый сервер] Получить информацию о работнике (права/привилегии)

Схемы: `schemas/qryGetEmployeeInfo2.xsd`, `schemas/resGetEmployeeInfo2.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Waiter> [refItem]  - Официант
  <Restaurant>? [refItem]  - Ресторан
  <Station>? [refItem]  - Станция
  @CMD: string = "GetEmployeeInfo2"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Waiter> [resRefItem]  - Работник
<Drawer>? [resRefItem]  - Ящик, на который зарегистрирован работник
<Operations>? [Items]  - Список операций
  <Item>*
    @id: positiveInteger  - ID элемента
    @guid: normalizedString  - GUID элемента
<ObjectRights>? [Items]  - Список прав на объекты (структура - см. выше)
<Privileges>? [Items]  - Список привилегий (структура - см. выше)
<ObjectPrivileges>? [Items]  - Список привилегий на объекты (структура - см. выше)
```

## Пример: GetEmployeeInfo2

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetEmployeeInfo2">
    <Waiter id="{{waiterId}}"/>
    <Restaurant id="{{restaurantId}}"/>
    <Station id="{{stationId}}"/>
  </RK7CMD>
</RK7Query>
```
