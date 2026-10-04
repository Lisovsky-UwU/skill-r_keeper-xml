# GetUsageValue

[Касса, Кассовый сервер] Получить значение использования

Схемы: `schemas/qryGetUsageValue.xsd`, `schemas/resGetUsageValue.xsd`
Влияние: только чтение

## Практика

- Значения name содержат пробелы: "Order Category", "Price Type" и т.д. (полный список - в схеме). Значения вроде "Station" сервер отвергает.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Order>? [orderElement]  - Заказ
  <Table>? [refItem]  - Стол
  <Station>? [refItem]  - Станция
  <Waiter>? [refItem]  - Официант
  <GuestType>? [refItem]  - Тип гостей
  @CMD: string = "GetUsageValue"
  @name!: filterType {BonusTypes | Order Category | Trade Group | Service scheme | Cash Doser | Keyboard layout | Selector group | Cash Drawer | Maket scheme | Business Period | Discount | Parameter | Form Scheme | Color Scheme | Price Type | Course | Check lists | Plugins configurations}  - Имя использования
  @param: integer  - Параметр (для некоторых типов использований)
  @dateTime: dateTime  - ДатаВремя
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Value> [resRefItem]  - Выбранный объект
@name!: normalizedString  - Имя использования
@param: integer  - Параметр использования
```

## Пример: GetUsageValue

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetUsageValue" name="Order Category">
    <Station id="{{stationId}}"/>
    <Table id="{{tableId}}"/>
  </RK7CMD>
</RK7Query>
```
