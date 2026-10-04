# GetXMLLicenseInstanceSeqNumber

[Касса,Кассовый сервер] Получение номера запроса по инстансу

Схемы: `schemas/qryGetXMLLicenseInstanceSeqNumber.xsd`, `schemas/resGetXMLLicenseInstanceSeqNumber.xsd`
Влияние: только чтение

## Практика

- Сервер требует <LicenseInfo>, хотя в XSD он необязательный; без настоящего anchor/licenseToken от UCS - "Bad license anchor".

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
  <MobileLicenseInfo>? [MobileLicenseInfoItem]  - Информация о лицензии мобильного официанта, необходимой для выполнения запроса
    <LicenseInstance> [MobileLicenseInstanceItem]
      @guid!: guidString  - Генерируется клиентом один раз при инсталляции или первом запуске приложения/инстанса как настоящий уникальный GUID и сохраняется. Количество разных значений в течении суток ограничено и связано с количеством подключений в лицензии.
      @seqNumber: nonNegativeInteger  - При первом вызове для конкретного guid должно быть 0, в дальнейшем каждый следующий вызов на 1 больше, можно повторить идентичный запрос (с там же seqNumber), ответ может кэшироваться RK7 (заново не обязан вычисляться)
      @name: normalizedString  - имя инстанса
    @kind: MobileLicenseKind {waiter | administrator}  - тип лицензии (официант/админ)
  <Timeout>? [TimeoutItem]  - Время, отведенное на выполнение запроса
    @value!: nonNegativeInteger  - Время в милисекундах, за которое должна выполниться операция или вернуть ошибку
  @CMD: string = "GetXMLLicenseInstanceSeqNumber"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<LicenseInfo> [LicenseInfoItem]  - Информация о лицензии
  <LicenseInstance> [LicenseInstanceItem]
    @guid!: guidString  - Генерируется клиентом один раз при инсталляции или первом запуске приложения/инстанса как настоящий уникальный GUID и сохраняется. Количество разных значений в течении суток ограничено и связано с количеством подключений в лицензии.
    @seqNumber: nonNegativeInteger  - При первом вызове для конкретного guid должно быть 0, в дальнейшем каждый следующий вызов на 1 больше, можно повторить идентичный запрос (с там же seqNumber), ответ может кэшироваться RK7 (заново не обязан вычисляться)
  @anchor: normalizedString  - формат якоря: 6:_ProductGUID_#_RestCode_/17, где _ProductGUID_ - GUID продукта, сообщается UCS, _RestCode_ - 9-значный код ресторана
  @licenseToken: normalizedString  - Токен лицензии запрашивается у системы лицензирования, инструкции по обращению к системе лицензирования за токеном лицензии сообщаются UCS вместе с GUID продукта
```

## Пример: GetXMLLicenseInstanceSeqNumber

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetXMLLicenseInstanceSeqNumber">
    <LicenseInfo anchor="6:{ProductGUID}#{RestCode}/17" licenseToken="">
      <LicenseInstance guid="{{licenseInstanceGuid}}" seqNumber="0"/>
    </LicenseInfo>
  </RK7CMD>
</RK7Query>
```
