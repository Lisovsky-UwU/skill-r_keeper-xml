# GetParamValue

Получить значение параметра

Схемы: `schemas/qryGetParamValue.xsd`, `schemas/resGetParamValue.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Order>? [orderElement]  - Заказ
  <Table>? [refItem]  - Стол
  <Station>? [refItem]  - Станция
  <Waiter>? [refItem]  - Официант
  <GuestType>? [refItem]  - Тип гостей
  @CMD: string = "GetParamValue"
  @ParamName!: normalizedString  - Имя параметра
  @dateTime: dateTime  - ДатаВремя
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
@Value!: normalizedString
```

## Пример: GetParamValue

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetParamValue" ParamName="CashStation">
    <Station id="{{stationId}}"/>
  </RK7CMD>
</RK7Query>
```
