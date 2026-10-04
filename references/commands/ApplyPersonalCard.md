# ApplyPersonalCard

Применение карты ПДС

Схемы: `schemas/qryApplyPersonalCard.xsd`, `schemas/resApplyPersonalCard.xsd`
Влияние: изменяет данные

## Практика

- Карта привязывается к гостю (Guest cardCode=...), а скидка по карте появляется в заказе строкой <Discount charge_source="pdsCard" cardCode=...> - ее видно в GetOrder.
- Неизвестная карта - Query Executing Error с текстом карточной системы, например «FC Test: Ошибка "Пользователь не найден!"(18)» (RK7ErrorN 3813).
- Если в заказе уже есть другая скидка, а их сочетание не описано в композициях скидок (DISCOUNTCOMPOSITIONS), будет "Не найдена композиция для скидки '...'" - скидка по карте не ляжет.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Order> [orderElement]  - Заказ
  <Station> [refItem]  - Станция, на которой прокатывается карточка
  <Interface> [refItem]  - Интерфейс, обрабатывающий карточку
  <Cashier>? [refItem]  - Кассир, от имени которого прокатывается карточка
  <Coupons> [anyType]  - xml с купонами (по 29-протоколу), с версии 7.6.4.014
  <ExtCardProperties>? [extCardProperties]  - Список запрашиваемых свойств
    <Property>+ [extCardProperty]
      @name!: normalizedString
      @value: normalizedString
  @CMD!: string = "ApplyPersonalCard"
  @lockguid: normalizedString (по умолчанию "")  - Токен блокировки (идентификатор сессии блокировки). С версии 7.6.4.006. При блокировке заказа использовать указанный токен. Если заказ был заблокирован, то проверить токен блокировки, выдавать ошибку если заказ был заблокирован при помощи другого токена
  @CardCode!: normalizedString  - Код карточки
  @seat: nonNegativeInteger (по умолчанию "0")  - Номер посадочного места: 0 - не задано
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<ExtCardProperties>? [extCardProperties]  - Список возвращенных расширенных свойств
  <Property>+ [extCardProperty]
    @name!: normalizedString
    @value: normalizedString
```

## Пример: ApplyPersonalCard

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="ApplyPersonalCard" CardCode="{{cardCode}}">
    <Order guid="{{orderGuid}}"/>
    <Station id="{{stationId}}"/>
    <Interface id="{{pdsInterfaceId}}"/>
    <Cashier id="{{cashierId}}"/>
  </RK7CMD>
</RK7Query>
```
