# RegisterEmployee

[Кассовый сервер] Зарегистрировать сотрудника

Схемы: `schemas/qryRegisterEmployee.xsd`, `schemas/resRegisterEmployee.xsd`
Влияние: изменяет данные

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Waiter> [refItem]  - Официант
  <Manager>? [refItem]  - Менеджер, от имени которого выполняется регистрация
  <Station> [refItem]  - Станция
  <Position>* [refItem]  - Позиция обслуживания
  @iscashstation: boolean (по умолчанию "true")  - Флаг "Использовать станцию как кассовую станцию". Используется, если параметр КассоваяСтанция = 'Спрашивать'
  @CMD: string = "RegisterEmployee"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Waiter> [resEmployeeItem]  - Зарегистрированный работыник
  (resRefItem: id | code | guid)
  <Role>? [resRefItem]  - Роль работника
<Drawer>? [resRefItem]  - Ящик, на который зарегистрирован работник
```

## Пример: RegisterEmployee

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="RegisterEmployee">
    <Waiter id="{{waiterId}}"/>
    <Manager id="{{managerId}}"/>
    <Station id="{{stationId}}"/>
  </RK7CMD>
</RK7Query>
```
