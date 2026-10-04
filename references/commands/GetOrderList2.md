# GetOrderList2

Получить список заказов (ver 2)

Схемы: `schemas/qryGetOrderList2.xsd`, `schemas/resGetOrderList2.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Waiter>? [refItem]  - Официант. Если задан, то возвращаются заказы, которые официант может обслуживать
  <Table>? [refItem]  - Стол. Если задан, то возвращаются заказы для этого стола
  @CMD: string = "GetOrderList2"
  @lastversion: integer  - Кэшировать результат запроса. Если версия таблицы заказов совпадает с lastversion, то возвращается "No changes", иначе обычный ответ
  @onlyOpened: boolean  - Флаг - вернуть только активные заказы
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Visit>* [visitItem]
  <GuestType>? [resRefItem]  - Тип гостей
  <Guests>? [Guests_Item]  - Список гостей
    <Guest>* [guest_item]
      <Interface>? [refItem]  - Интерфейс к карте гостя
      @guestLabel!: token  - Текстовая метка гостя
      @cardCode: normalizedString  - Код карты гостя
      @clientID: long  - ID адреса гостя
      @addressID: long  - ID адреса гостя
    @count: int  - Количество гостей
  <Orders>?  - Список заказов
    <Order>* [orderItem]
      <Creator> [resRefItem]  - Работник, создавший заказ
      <Waiter> [resRefItem]  - Главный официант
      <OrderCategory> [resRefItem]  - Категория заказа
      <OrderType>? [resRefItem]  - Тип заказа
      <Table> [resRefItem]  - Стол
      <Defaulter>? [resRefItem]  - Неплательщик
      <LockedByWaiter>? [resRefItem]  - Работник, который заблокировал заказ (если заказ заблокирован)
      <LockedByStation>? [resRefItem]  - Станция, которая заблокировала заказ (если заказ заблокирован)
      <ExternalProps>? [externalProps]  - Список внешних свойств заказа
        <Prop>* [externalPropItem]
          @name!: normalizedString  - Имя свойства
          @value: normalizedString (по умолчанию "")  - Значение свойства
      <ExtraTables>?  - Список дополнительных столов
        <item>+ [refItem]
      @visit: positiveInteger
      @orderIdent: positiveInteger
      @guid!: normalizedString  - GUID заказа
      @url!: normalizedString  - URL заказа для code.ucs.ru
      @version!: nonNegativeInteger  - Версия заказа
      @crc32!: int  - Контрольная сумма по содержимому заказа
      @persistentComment: normalizedString  - Сохраняемый комментарий заказа
      @nonPersistentComment: normalizedString  - Несохраняемый комментарий заказа
      @openTime!: dateTime  - Время создания заказа (для банкетных столов время начала банкета)
      @FinishTime: dateTime  - Дата и время завершения заказа
      @duration: dateTime  - Длительность заказа (банкета)
      @holder: normalizedString  - Владелец банкета (для банкетных заказов)
      @promoCode: normalizedString  - Промо-код заказа
      @orderName!: normalizedString  - Имя заказа
      @seqNumber: int  - Последовательный номер заказа
      @locked: boolean  - Флаг - заказ заблокирован для редактирования
      @deleted: boolean  - Флаг - все блюда заказа удалены
      @orderSum!: nonNegativeInteger  - Сумма заказа (в копейках)
      @prepaySum: nonNegativeInteger (по умолчанию "0")  - Сумма незакрытых предоплат (в копейках)
      @promisedSum: nonNegativeInteger (по умолчанию "0")  - Сумма обещанных платежей (в копейках)
      @discountSum!: int  - Сумма скидок (в копейках)
      @unpaidSum!: int  - Неоплаченная сумма заказа (в копейках)
      @totalPieces!: nonNegativeInteger  - Количество порций в заказе (в тысячных долях)
      @paid: boolean (по умолчанию "false")  - Флаг - заказ оплачен
      @finished: boolean  - Флаг - заказ завершен
      @receiptError: boolean  - Флаг - в заказе есть ошибочный чек
      @bySeats: boolean  - Флаг - заказ рассчитан по местам
      @readyExists: boolean  - Флаг - в заказе есть готовые, но незабранные блюда
      @weightNeeded: boolean  - Флаг - в заказе есть блюда, для которых требуется указание веса
      @billTime: dateTime  - ДатаВремя печати пречека
      @dessertTime: dateTime  - ДатаВремя добавления в заказ десерта
      @reserve: boolean  - Резервный заказ
      @duration: dateTime  - Длительность заказа (банкета)
  @visit: integer  - Идентификатор визита
  @guid!: normalizedString  - GUID визита
  @finished: boolean  - Флаг - визит завершен
  @persistentComment: normalizedString  - Сохраняемый комментарий
  @nonPersistentComment: normalizedString  - Несохраняемый комментарий
@lastversion: integer  - Версия таблицы заказов
```

## Пример: GetOrderList2

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetOrderList2" onlyOpened="1"/>
</RK7Query>
```
