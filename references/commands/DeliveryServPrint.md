# DeliveryServPrint

[Касса, Кассовый сервер] Доставка: ручная отправка на сервис-печать

Схемы: `schemas/Delivery/qryDeliveryServPrint.xsd`, `schemas/Delivery/resDeliveryServPrint.xsd`
Влияние: изменяет данные

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Order> [orderElement]  - Заказ
  <LockStation>? [refItem]  - Станция, от имени которой будет заблокирован заказ
  @CMD: string = "DeliveryServPrint"
  @lockguid: normalizedString (по умолчанию "")  - Токен блокировки (идентификатор сессии блокировки). С версии 7.6.4.006. При блокировке заказа использовать указанный токен. Если заказ был заблокирован, то проверить токен блокировки, выдавать ошибку если заказ был заблокирован при помощи другого токена
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
@version: nonNegativeInteger  - Версия заказа
@crc32!: int  - Контрольная сумма по содержимому заказа
```

## Пример: DeliveryServPrint

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="DeliveryServPrint">
    <Order guid="{{deliveryGuid}}"/>
  </RK7CMD>
</RK7Query>
```
