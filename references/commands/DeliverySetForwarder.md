# DeliverySetForwarder

[Касса, Кассовый сервер] Доставка: назначить экспедитора

Схемы: `schemas/Delivery/qryDeliverySetForwarder.xsd`, `schemas/Delivery/resDeliverySetForwarder.xsd`
Влияние: изменяет данные

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Employee> [refItem]  - Экспедитор
  <Order>* [orderElement]  - Заказ
  @CMD: string = "DeliverySetForwarder"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Order>*
  @orderIdent!: positiveInteger
  @version: nonNegativeInteger  - Версия заказа
  @crc32!: int  - Контрольная сумма по содержимому заказа
```

## Пример: DeliverySetForwarder

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="DeliverySetForwarder">
    <Employee id="{{waiterId}}"/>
    <Order guid="{{deliveryGuid}}"/>
  </RK7CMD>
</RK7Query>
```
