# WaiterMessage

[Касса, Кассовый сервер] Отправка сообщения официанту

Схемы: `schemas/qryWaiterMessage.xsd`, `schemas/resWaiterMessage.xsd`
Влияние: изменяет данные

## Практика

- Сервер требует expireTime, хотя в XSD атрибут необязательный ("Attribute RK7CMD/@expireTime is not found").

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
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
  @CMD: string = "WaiterMessage"
  @external_id: ExternalIDString (по умолчанию "")  - Внешний идентификатор сообщения (строка)
  @text!: normalizedString  - Сообщение
  @expireTime: dateTime  - Время жизни сообщения
  @messageType!: messageType {Unknown | FromTable | FromMonitor | DishesReady | ErrorNotify | KitchenRequest | FromStationScript | FromServerScript | XMLInterface | LicenseInfo | TariffClosing | SysTimeChanged | FromManagerStation | SecondScreen | RequestOrderLock}  - Тип сообщения
  @param: integer  - Параметр сообщения
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Message> [resMessageItem]
  @id: positiveInteger  - ID сообщения
```

## Пример: WaiterMessage

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="WaiterMessage" text="Тестовое сообщение" messageType="XMLInterface" expireTime="2030-12-31T23:59:59" external_id="msg-1">
    <Station id="{{stationId}}"/>
    <Waiter id="{{waiterId}}"/>
  </RK7CMD>
</RK7Query>
```
