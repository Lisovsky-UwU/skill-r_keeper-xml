# UpdateOrder

[Кассовый сервер] Обновить свойства заказа

Схемы: `schemas/qryUpdateOrder.xsd`, `schemas/resUpdateOrder.xsd`
Влияние: изменяет данные

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <LockStation>? [refItem]  - Станция, от имени которой будет заблокирован заказ
  <Manager>? [refItem]  - Менеджер, от имени которого выполняется операция
  <Order>? [orderElement]  - Заказ
  <Table>? [refItem]  - Стол
  <Waiter>? [refItem]  - Главный официант
  <OrderType>? [refItem]  - Тип заказа
  <Defaulter>? [refItem]  - Тип неплательщика
  <GuestType>? [refItem]  - Тип гостей
  <Guests>? [Guests_Item]  - Список гостей
    <Guest>* [guest_item]
      <Interface>? [refItem]  - Интерфейс к карте гостя
      <EntranceCardType>? [refItem]  - Тип карты на входе. Добавлено в 7.07.00.300
      @guestLabel!: token  - Текстовая метка гостя
      @cardCode: normalizedString  - Код карты гостя
      @clientID: int  - ID адреса гостя
      @addressID: int  - ID адреса гостя
      @maxamount: int  - Максимальная сумма по заказам, в копейках. Только для чтения. Добавлено в 7.07.00.300
      @restAmount: int  - Остаток масимальной суммы по заказам, в копейках. Только для чтения. Добавлено в 7.07.00.362+
    @count: int  - Количество гостей
  <ExtraTables>?  - Список дополнительных столов
    <Item>+ [refItem]
  <ExternalProps>? [externalProps]  - Список внешних свойств заказа
    <Prop>* [externalPropItem]
      @name!: normalizedString  - Имя свойства
      @value: normalizedString (по умолчанию "")  - Значение свойства
  @CMD: string = "UpdateOrder"
  @lockguid: normalizedString  - Токен блокировки (идентификатор сессии блокировки). С версии 7.6.4.005
  @persistentComment: normalizedString  - Сохраняемый комментарий
  @nonPersistentComment: normalizedString  - Несохраняемый комментарий
  @openTime: dateTime  - Время начала заказа (для резерва)
  @duration: dateTime  - Длительность заказа (для резерва)
  @holder: normalizedString  - Владелец (для резерва)
  @promoCode: normalizedString  - Промо-код заказа
  @rkFriendsAnchor: normalizedString  - Якорь в Friends (идентификатор заявки)
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Errors>? [ErrorStack]
  <Error>*  - Стэк ошибок, возникших при выполнени команды
    (текстовое содержимое: string)
    @RK7ErrorN!: positiveInteger  - Код ошибки RK7
    @Component!: errorArea {Printer | Authorization terminal | PDS | Rights}  - Компонент, в котором была сгенерирована ошибка
@ServerVersion!: normalizedString  - Версия кассовой программы
@XmlVersion!: positiveInteger  - Версия xml протокола
@NetName: token  - Сетевое имя программы (с 7.5.3.260)
@CMD: token  - Исходная xml-команда
@Status!: string {Ok | No changes | Execution Started | Query Parse Error | Bad Query Parameters | Query Executing Error | Result Writing Error}  - Статус выполнения запроса
@RK7ErrorN: positiveInteger  - Код ошибки RK7
@ErrorText!: normalizedString  - Текст ошибки
@WorkTime!: nonNegativeInteger  - Время обработки запроса (в миллисекундах)
@DateTime!: dateTime  - Дата и время генерации ответного xml (xmlver>=39)
@Processed!: nonNegativeInteger  - Количество обработанных команд
```

## Пример: UpdateOrder

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="UpdateOrder" persistentComment="example: изменено">
    <Manager id="{{managerId}}"/>
    <Order guid="{{orderGuid}}"/>
    <Waiter id="{{waiterId}}"/>
    <Guests>
      <Guest guestLabel="1"/>
      <Guest guestLabel="2"/>
    </Guests>
    <ExternalProps>
      <Prop name="source" value="example"/>
    </ExternalProps>
  </RK7CMD>
</RK7Query>
```
