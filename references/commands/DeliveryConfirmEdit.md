# DeliveryConfirmEdit

[Касса, Кассовый сервер] Доставка: подтверждение редактирования

Схемы: `schemas/Delivery/qryDeliveryConfirmEdit.xsd`, `schemas/Delivery/resDeliveryConfirmEdit.xsd`
Влияние: изменяет данные

## Практика

- readyTime должен быть не позже чем примерно через сутки от текущего времени сервера, иначе "Введенное время не может превышать ... (максимальное время)".

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <LicenseInfo>? [LicenseInfoItem]  - Информация о лицензии, необходимой для выполнения запроса
    <LicenseInstance> [LicenseInstanceItem]
      @guid!: guidString  - Генерируется клиентом один раз при инсталляции или первом запуске приложения/инстанса как настоящий уникальный GUID и сохраняется. Количество разных значений в течении суток ограничено и связано с количеством подключений в лицензии.
      @seqNumber: nonNegativeInteger  - При первом вызове для конкретного guid должно быть 0, в дальнейшем каждый следующий вызов на 1 больше, можно повторить идентичный запрос (с там же seqNumber), ответ может кэшироваться RK7 (заново не обязан вычисляться)
    @anchor: normalizedString  - формат якоря: 6:_ProductGUID_#_RestCode_/17, где _ProductGUID_ - GUID продукта, сообщается UCS, _RestCode_ - 9-значный код ресторана
    @licenseToken: normalizedString  - Токен лицензии запрашивается у системы лицензирования, инструкции по обращению к системе лицензирования за токеном лицензии сообщаются UCS вместе с GUID продукта
  <Order> [orderElement]  - Заказ
  <OrderType>? [refItem]  - Тип заказа
  <Restaurant>? [refItem]  - Ресторан
  <LockStation>? [refItem]  - Станция, от имени которой будет заблокирован заказ
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
  <ExtSource>?  - Внешний id заказа
    @source!: string  - id-программы, создавшей заказ
    @extID: positiveInteger  - Дополнительный id заказа
  <ClientID>? [long]  - ID клиента
  <AddressID>? [long]  - ID адреса доставки
  <HolderXML> [anyType]  - Информация о клиенте (xml из CardSystem)
  @CMD: string = "DeliveryConfirmEdit"
  @lockguid: normalizedString  - Токен блокировки (идентификатор сессии блокировки). С версии 7.6.4.005
  @persistentComment: normalizedString  - Сохраняемый комментарий
  @nonPersistentComment: normalizedString  - Несохраняемый комментарий
  @readyTime!: dateTime  - Время, к которому заказ должен быть приготовлен
  @minCookTime: dateTime  - Минимальное время приготовления заказа
  @printImmediately: boolean  - Сервис-печать выполнить сразу. Если false, то сервис-печать начнется по достижению времени начала готовки
  @closeOrder: boolean  - Закрыть заказ
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
@version: nonNegativeInteger  - Версия заказа
@crc32!: int  - Контрольная сумма по содержимому заказа
```

## Пример: DeliveryConfirmEdit

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="DeliveryConfirmEdit" readyTime="{{readyTime}}">
    <Order guid="{{deliveryGuid}}"/>
    <HolderXML>
      <holder>
        <Holders_Addresses/>
      </holder>
    </HolderXML>
  </RK7CMD>
</RK7Query>
```
