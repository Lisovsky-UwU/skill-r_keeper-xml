# DeliveryGetOrderList

[Касса,Кассовый сервер]Доставка: получить список заказов доставки

Схемы: `schemas/Delivery/qryDeliveryGetOrderList.xsd`, `schemas/Delivery/resDeliveryGetOrderList.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <ExtSource>+ [positiveInteger]  - Фильтр: Заказ.ExtSource = указанному значению
  <NotExtSource>+ [positiveInteger]  - Фильтр: Заказ.ExtSource != указанному значению
  @CMD!: string = "DeliveryGetOrderList"
  @lastversion: integer  - Кэшировать результат запроса. Если версия таблицы заказов совпадает с lastversion, то возвращается "No changes", иначе обычный ответ
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<ExtraInfo>
  @restaurantState: boolean  - Статус ресторана (0 - неактивен, 1 - активен)
  @restaurantTime: dateTime  - Время начала деятельности (окончание периода неактивности)
<Order>*
  <ExtSource>*  - Внешний id заказа
    @source!: string  - id-программы, создавшей заказ
    @extID!: string  - ID визита в базе кассового сервера коллцентра
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
  <MainWaiter> [resRefItem]  - Главный официант
  <Creator> [resRefItem]  - Работник, создавший заказ (оператор)
  <Restaurant>? [resRefItem]  - Ресторан доставки
  @orderIdent!: nonNegativeInteger
  @version: nonNegativeInteger  - Версия заказа
  @crc32!: int  - Контрольная сумма по содержимому заказа
  @guid: normalizedString  - GUID заказа
  @orderName: normalizedString  - Имя заказа
  @createTime: dateTime  - Время создания заказа
  @lastChangeTime: dateTime  - Время последнего редактирования заказа
  @totalPieces!: nonNegativeInteger  - Количество порций в заказе (в тысячных долях)
  @prepaySum: integer (по умолчанию "0")  - Сумма незакрытых предоплат (в копейках)
  @promisedSum: integer (по умолчанию "0")  - Сумма обещанных платежей (в копейках)
  @locked: boolean (по умолчанию "false")  - Флаг - заказ заблокирован для редактирования
  @deleted: boolean  - Флаг - все блюда заказа удалены
  @started: boolean  - Флаг - начата готовка блюд заказа
  @ready: boolean  - Флаг - все блюда заказа уже приготовлены
  @paid: boolean  - Флаг - заказ оплачен
  @orderSum: int  - Сумма заказа (в копейках)
  @clientID: long  - ID клиента
  @addressID: long  - ID адреса доставки
@lastversion: integer  - Версия таблицы заказов
```

## Пример: DeliveryGetOrderList

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="DeliveryGetOrderList"/>
</RK7Query>
```
