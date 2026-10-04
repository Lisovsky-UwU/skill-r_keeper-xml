# DeliveryPayOrders

Доставка: печать чека/пречека при отправке экспедитора

Схемы: `schemas/Delivery/qryDeliveryPayOrders.xsd`, `schemas/Delivery/resDeliveryPayOrders.xsd`
Влияние: изменяет данные

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Employee> [refItem]  - Работник, выполняющий операцию
  <Cashier>? [refItem]  - Кассир, от имени которого будет напечатан чек. Если не задан, то берется Employee
  <Station> [refItem]  - Станция, на которой нужно распечатать накладную
  <Order>+ [orderElement]  - Заказ
  @CMD: string = "DeliveryPayOrders"
  @lockguid: normalizedString  - Токен блокировки (идентификатор сессии блокировки). С версии 7.6.4.006
  @docType: string {receipt | bill} (по умолчанию "receipt")  - Тип документа для печати (чек, пречек)
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Order>*
  @orderIdent!: positiveInteger
  @version: nonNegativeInteger  - Версия заказа
  @crc32!: int  - Контрольная сумма по содержимому заказа
```

## Пример: DeliveryPayOrders

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="DeliveryPayOrders" docType="bill">
    <Employee id="{{waiterId}}"/>
    <Station id="{{stationId}}"/>
    <Order guid="{{deliveryGuid}}"/>
  </RK7CMD>
</RK7Query>
```
