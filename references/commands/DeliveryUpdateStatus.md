# DeliveryUpdateStatus

[Касса, Кассовый сервер] Доставка: изменение статуса доставки

Схемы: `schemas/Delivery/qryDeliveryUpdateStatus.xsd`, `schemas/Delivery/resDeliveryUpdateStatus.xsd`
Влияние: изменяет данные

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Order> [orderElement]  - Заказ
  <DeliveryBlock>? [deliveryBlock]
    @deliveryState: int  - Статус доставки
    @startTime: dateTime  - Время создания заказа
    @travelTime: dateTime  - Время в пути
    @deliveryTime: dateTime  - Ожидаемое время доставки
    @forwarderSendTime: dateTime  - Время отправки экспедитора
    @forwarderReturnTime: dateTime  - Время возвращения экспедитора
    @realDeliveryTime: dateTime  - Реальное время доставки
    @lastProcessTime: dateTime  - Время последней обработки заказа. Заполняет Delivery
    @minCookTime: dateTime  - Минимальное время приготовления заказа
    @zoneID: int  - ID зоны доставки
    @zoneName: normalizedString  - Имя зоны доставки
    @orderPrefix: normalizedString  - Префиск для имени заказа
    @isTakeOut: boolean  - Флаг - доставка на вынос. Если флаг выставлен, то статусами доставки на филиале управляет RK7
    @autoChangeState: boolean  - Флаг - разрешение автоматического изменения статусов доставки в rk7
  <Restaurant>? [refItem]  - Ресторан, выполняющий доставку
  <LockStation>? [refItem]  - Станция, от имени которой будет заблокирован заказ
  <ExtSource>  - Внешний id заказа
    @source!: integer  - id-программы, создавшей заказ
    @extID!: positiveInteger  - ID визита в базе кассового сервера коллцентра
  <Table>? [refItem]  - Стол
  <Waiter>? [refItem]  - Главный официант
  <OrderType>? [refItem]  - Тип заказа
  <Defaulter>? [refItem]  - Тип неплательщика
  <GuestType>? [refItem]  - Тип гостей
  <Guests>? [Guests_Item]  - Список гостей
    <Guest>* [guest_item]
      <Interface>? [refItem]  - Интерфейс к карте гостя
      @guestLabel!: token  - Текстовая метка гостя
      @cardCode: normalizedString  - Код карты гостя
      @clientID: long  - ID адреса гостя
      @addressID: long  - ID адреса гостя
    @count: int  - Количество гостей
  <ExtraTables>?  - Список дополнительных столов
    <Item>+ [refItem]
  <ExternalProps>? [externalProps]  - Список внешних свойств заказа
    <Prop>* [externalPropItem]
      @name!: normalizedString  - Имя свойства
      @value: normalizedString (по умолчанию "")  - Значение свойства
  @CMD: string = "DeliveryUpdateStatus"
  @lockguid: normalizedString  - Токен блокировки (идентификатор сессии блокировки). С версии 7.6.4.005
  @persistentComment: normalizedString  - Сохраняемый комментарий
  @nonPersistentComment: normalizedString  - Несохраняемый комментарий
  @openTime: dateTime  - Время начала заказа (для резерва)
  @duration: dateTime  - Длительность заказа (для резерва)
  @holder: normalizedString  - Владелец (для резерва)
  @promoCode: normalizedString  - Промо-код заказа
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
@version: nonNegativeInteger  - Версия заказа
@crc32!: int  - Контрольная сумма по содержимому заказа
```

## Пример: DeliveryUpdateStatus

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="DeliveryUpdateStatus">
    <Order guid="{{deliveryGuid}}"/>
    <DeliveryBlock deliveryState="1"/>
    <ExtSource source="example" extID="1"/>
  </RK7CMD>
</RK7Query>
```
