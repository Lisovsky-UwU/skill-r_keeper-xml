# DeliveryVoidOrder

[Касса, Кассовый сервер] Доставка: удалить заказ

Схемы: `schemas/Delivery/qryDeliveryVoidOrder.xsd`, `schemas/Delivery/resDeliveryVoidOrder.xsd`
Влияние: **опасно** - необратимые или массовые изменения, блокировка кассы

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Order> [orderElement]  - Заказ
  <Employee> [refItem]  - Менеджер, удаляющий заказ
  <DeleteReason> [refItem]  - Причина удаления
  <Station> [refItem]  - Станция
  @CMD: string = "DeliveryVoidOrder"
  @lockguid: normalizedString (по умолчанию "")  - Токен блокировки (идентификатор сессии блокировки). С версии 7.6.4.006. При блокировке заказа использовать указанный токен. Если заказ был заблокирован, то проверить токен блокировки, выдавать ошибку если заказ был заблокирован при помощи другого токена
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
@version: nonNegativeInteger  - Версия заказа
@crc32!: int  - Контрольная сумма по содержимому заказа
```

## Пример: DeliveryVoidOrder

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="DeliveryVoidOrder">
    <Order guid="{{deliveryGuid}}"/>
    <Employee id="{{managerId}}"/>
    <DeleteReason id="{{deleteReasonId}}"/>
    <Station id="{{stationId}}"/>
  </RK7CMD>
</RK7Query>
```
