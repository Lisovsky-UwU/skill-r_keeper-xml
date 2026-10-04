# GetOrderList

Получить список заказов

Схемы: `schemas/qryGetOrderList.xsd`, `schemas/resGetOrderList.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Waiter>? [refItem]  - Официант. Если задан, то возвращаются заказы, которые официант может обслуживать
  <Table>? [refItem]  - Стол. Если задан, то возвращаются заказы для этого стола
  @CMD: string = "GetOrderList"
  @lastversion: integer  - Кэшировать результат запроса. Если версия таблицы заказов совпадает с lastversion, то возвращается "No changes", иначе обычный ответ
  @onlyOpened: boolean  - Флаг - вернуть только активные заказы
  @needIdents: boolean (по умолчанию "1")  - Флаг - возвращать идентификаторы элементов
  @needCodes: boolean (по умолчанию "1")  - Флаг - возвращать коды элементов
  @needNames: boolean (по умолчанию "0")  - Флаг - возвращать имена элементов
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Visit>* [visitItem]
  <Guests>?  - Информация о гостях
    <Guest>* [guestItem]
      @GuestLabel: token  - Текстовая метка гостя
      @closed: boolean  - Признак того, что место закрыто
      @CardCode: normalizedString  - Код карты гостя
      @IntfID: integer  - ID интефейса
      @IntfCode: integer  - Код интефейса
      @IntfName: normalizedString  - Наименование интефейса
    @count: int  - Количество гостей
  <Orders>?  - Информация о гостях
    <Order>* [orderItem]
      <LockedByWaiter>? [resRefItem]  - Работник, который заблокировал заказ (если заказ заблокирован)
      <LockedByStation>? [resRefItem]  - Станция, которая заблокировала заказ (если заказ заблокирован)
      <ExternalID>*  - Внешний id заказа
        @ExtSource!: positiveInteger  - id-программы, создавшей заказ
        @ExtID: normalizedString  - Дополнительный id заказа
      <ExtraTables>?  - Список дополнительных столов
        <item>+ [refItem]
      @OrderID: positiveInteger  - ID заказа
      @Version: integer  - Версия заказа (с 7.4.8.0)
      @crc32!: int  - Контрольная сумма по содержимому заказа
      @guid!: normalizedString  - GUID заказа
      @purchase: boolean  - Признак заказа возврата
      @dontcheckLicense: boolean  - Флаг "Не проверять лицензию xml-сохранение заказа". Такие заказы не видны на кассе"
      @promoCode: normalizedString  - Промо-код заказа
      @locked: boolean  - Флаг "Заказ заблокирован"
      @url!: normalizedString  - URL заказа для code.ucs.ru
      @OrderName: normalizedString  - Пользовательское имя заказа
      @OrderSum: integer  - Сумма заказа (в копейках)
      @ToPaySum: integer  - Неоплаченная сумма (в копейках). Начиная с версии 7.5.3.130 сумма возвращается с учетом предоплат
      @PrepaySum: integer (по умолчанию "0")  - Сумма незакрытых предоплат (в копейках)
      @PromisedSum: integer (по умолчанию "0")  - Сумма обещанных платежей (в копейках)
      @PriceListSum: integer  - Сумма заказа по прейскуранту (в копейках)
      @TotalPieces: nonNegativeInteger  - Сумма порций всех блюд заказа( в тысячных долях)
      @CreateTime: dateTime  - Дата и время создания заказа
      @FinishTime: dateTime  - Дата и время завершения заказа
      @Finished: boolean  - 0 - заказ открыт, 1 - обслуживание по заказу завершено
      @Bill: boolean  - Флаг - в заказе есть пречек
      @ReceiptError: boolean  - Флаг - в заказе есть ошибочный чек
      @Dessert: boolean  - Флаг - в заказе есть десерт
      @bySeats: boolean  - Флаг - заказ рассчитан по местам
      @ReadyExists: boolean  - Флаг - в заказе есть готовые, но незабранные блюда
      @WeightNeeded: boolean  - Флаг - в заказе есть блюда, для которых требуется указание веса
      @BillTime: dateTime  - ДатаВремя печати пречека
      @DessertTime: dateTime  - ДатаВремя добавления в заказ десерта
      @TableID: integer  - ID стола
      @TableCode: integer  - Код стола
      @TableName: normalizedString  - Наименование стола
      @WaiterID: integer  - ID официанта
      @WaiterCode: integer  - Код официанта
      @WaiterName: normalizedString  - Наименование официанта
      @OrderCategID: integer  - ID категории заказа
      @OrderCategCode: integer  - Код категории заказа
      @OrderCategName: normalizedString  - Наименование категории заказа
      @OrderTypeID: integer  - ID типа заказа
      @OrderTypeCode: integer  - Код типа заказа
      @OrderTypeName: normalizedString  - Наименование типа заказа
      @DefaulterID: integer  - ID типа неплательщика
      @DefaulterCode: integer  - Код типа неплательщика
      @DefaulterName: normalizedString  - Наименование типа неплательщика
      @reserve: boolean  - Резервный заказ
      @duration: dateTime  - Длительность заказа (банкета)
  @VisitID: integer  - Идентификатор визита
  @guid!: normalizedString  - GUID визита
  @Finished: boolean  - Флаг - визит завершен
  @GuestsCount: integer  - Количество гостей
  @PersistentComment: normalizedString  - Сохраняемый комментарий
  @NonPersistentComment: normalizedString  - Несохраняемый комментарий
  @GuestTypeID: integer  - ID типа гостей
  @GuestTypeCode: integer  - Код типа гостей
  @GuestTypeName: normalizedString  - Наименование типа гостей
@lastversion: integer  - Версия таблицы заказов
```

## Пример: GetOrderList

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetOrderList" onlyOpened="1" needIdents="1" needCodes="1" needNames="1"/>
</RK7Query>
```
