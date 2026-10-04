# DeliverySetLastProcessTime

[Кассовый сервер] Доставка: изменить "время обработки заказа"

Схемы: `schemas/Delivery/qryDeliverySetLastProcessTime.xsd`, `schemas/Delivery/resDeliverySetLastProcessTime.xsd`
Влияние: изменяет данные

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Order> [orderElement]  - Заказ
  @CMD: string = "DeliverySetLastProcessTime"
  @lastProcessTime: dateTime  - Время последней обработки заказа
```

## Пример: DeliverySetLastProcessTime

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="DeliverySetLastProcessTime" lastProcessTime="{{readyTime}}">
    <Order guid="{{deliveryGuid}}"/>
  </RK7CMD>
</RK7Query>
```
