# DeliveryLockOrder

[Касса, Кассовый сервер] Доставка: временная блокировака заказа

Схемы: `schemas/Delivery/qryDeliveryLockOrder.xsd`, `schemas/Delivery/resDeliveryLockOrder.xsd`
Влияние: изменяет данные

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Order> [orderElement]  - Заказ
  <Station>? [refItem]  - Станция, от имени которой блокируется заказ
  <Employee>? [refItem]  - Работник, блокирующий заказ
  @CMD: string = "DeliveryLockOrder"
  @lockTime: dateTime  - Время, на которое нужно заблокировать заказ (с точностью до минуты)
  @lockguid: normalizedString  - Токен блокировки (идентификатор сессии блокировки). Если указан, то с заказом может работать только тот, кто использует такой же токен блокировки
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
@locked!: boolean  - Флаг "Заказ заблокирован"
```

## Пример: DeliveryLockOrder

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="DeliveryLockOrder" lockguid="{{lockGuid}}">
    <Order guid="{{deliveryGuid}}"/>
  </RK7CMD>
</RK7Query>
```
