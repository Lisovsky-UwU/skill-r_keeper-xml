# LoginOnStation

[Касса, Кассовый сервер] Зарегистрировать работника на кассе

Схемы: `schemas/qryLoginOnStation.xsd`, `schemas/resLoginOnStation.xsd`
Влияние: изменяет данные

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
  <Station>? [refItem]  - Станция. При запросе к серверу обязательно для заполнения, при запросе к кассе можно не заполнять
  <Waiter>? [refItem]  - Работник
  @CMD: string = "LoginOnStation"
  @cardCode: nonNegativeInteger  - Код карты. Если задан, то Waiter и password не используется
  @password: normalizedString  - Пароль. Проверяется, если не задан cardCode
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Drawer>? [resRefItem]  - Ящик, на который зарегистрирован работник
<OpRights>?  - Список прав на операции
  <oper>*
    @id: positiveInteger  - ID операции
<ObjRights>?  - Список прав на объекты
  <right>*
    @id: positiveInteger  - ID права
<Tables>?  - Список доступных столов
  <table>*
    @id: positiveInteger  - ID стола
<Orders>?  - Список доступных столов
  <Order>*
    @orderIdent!: positiveInteger
    @own_order: boolean  - Флаг "Свой заказ"
```

## Пример: LoginOnStation

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="LoginOnStation" password="{{managerPassword}}">
    <Station id="{{stationId}}"/>
    <Waiter id="{{waiterId}}"/>
  </RK7CMD>
</RK7Query>
```
