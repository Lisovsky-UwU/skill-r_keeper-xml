# GetWaiterMessages

Получить список сообщений официанта

Схемы: `schemas/qryGetWaiterMessages.xsd`, `schemas/resGetWaiterMessages.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Waiter>? [refItem]  - Официант
  <Station>? [refItem]  - Станция
  @CMD: string = "GetWaiterMessages"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Message>* [resWaiterMessage]  - Сообщение официанту
  <Station>? [refItem]  - Станция, на которой должно быть показано сообщение
  <Waiter>? [refItem]  - Официант
  <Manager>? [refItem]  - Менеджер
  <Order>? [orderElement]  - Заказ (сообщение будет показано только если открыт этот заказ)
  <Buttons>? [messageButtons]  - Список кнопок для сообщения
    <Button>* [messageButton]
      <Image> [refItem]  - Картинка для кнопки, ссылка на справочник картинок
      @text!: normalizedString  - Текст на кнопке
      @browseurl: normalizedString (по умолчанию "")  - URL который будет открыт в браузере при нажатии на кнопку
      @httpcall_url: normalizedString (по умолчанию "")  - URL по которому будет выполнен http-get запрос при нажатии на кнопку (без открытия браузера)
  @external_id: ExternalIDString (по умолчанию "")  - Внешний идентификатор сообщения (строка)
  @ondeleteurl: string (по умолчанию "")  - URL по которому будет выполнен http-get запрос при удалении сообщения. С версии 7.6.5.433
  @text!: normalizedString  - Сообщение
  @expireTime: dateTime  - Время жизни сообщения
  @messageType!: messageType {Unknown | FromTable | FromMonitor | DishesReady | ErrorNotify | KitchenRequest | FromStationScript | FromServerScript | XMLInterface | LicenseInfo | TariffClosing | SysTimeChanged | FromManagerStation | SecondScreen | RequestOrderLock}  - Тип сообщения
  @param: integer  - Параметр сообщения
  @id: positiveInteger  - ID сообщения
  @createTime: dateTime  - Время создания сообщения
  @repeatCount: nonNegativeInteger  - Число повторений
```

## Пример: GetWaiterMessages

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetWaiterMessages">
    <Waiter id="{{waiterId}}"/>
  </RK7CMD>
</RK7Query>
```
