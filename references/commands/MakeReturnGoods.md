# MakeReturnGoods

[Кассовый сервер] Возврат товара

Схемы: `schemas/qryMakeReturnGoods.xsd`, `schemas/resMakeReturnGoods.xsd`
Влияние: **опасно** - необратимые или массовые изменения, блокировка кассы

## Практика

- Reason - причина из ORDERVOIDS с флагом возврата блюд (ImplOnDishReturn).
- Создает отдельный чек возврата (новый CheckNum); после возврата исходный чек нельзя аннулировать.

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
  <Station> [refItem]  - Станция
  <Cashier> [refItem]  - Кассир
  <Reason> [refItem]  - Причина (удаления) для возврата блюд
  <ReceiptMaket>? [refItem]  - Представление документа для возврата товара
  <OrderType>? [resRefItem]  - Тип заказа
  <PrintCheck>? [roPrintCheckItem]  - Исходный чек, блюдо из которого нужно вернуть, идентифицируется line_guid
    @line_guid: normalizedString  - GUID чека
  <Order>? [roOrder]  - Заказ, из которого нужно вернуть блюдо. Используется только в случае, если не указан чек. Если в заказе более 1 чека, то возврат с указанием только guid заказа осуществить нельзя
    @guid: normalizedString  - GUID заказа
  <Dishes>  - Список блюд для возврата
    <Dish>+ [roDishItem]
      @line_guid: normalizedString  - LINE_GUID блюда
      @quantity!: int  - Количество блюда (в тысячных долях)
  <ExternalProps>? [externalProps]  - Список внешних свойств заказа
    <Prop>* [externalPropItem]
      @name!: normalizedString  - Имя свойства
      @value: normalizedString (по умолчанию "")  - Значение свойства
  <FiscalDocInfo>? [poFiscalDocInfo]  - Информация о фискальном документе. Для использования в отчетах.
    <FiscDev>? [refItem]  - Тип фискального устройства. Указанное значение заносится в поле PrintChecks.FiscDev
    @PrintNumber!: nonNegativeInteger  - Печатный номер чека, в России номер чека ФН. Указанное значение заносится в поле PrintChecks.PrintNumber.
    @DeleteFiscDocNumber!: nonNegativeInteger  - Фискальный номер документа, в России номер документа ФН. Указанное значение заносится в поле PrintChecks.DeleteFiscDocNumber.
    @GlobalFiscalId: normalizedString  - Глобальный номер чека, в России не используется. Указанное значение заносится в поле PrintChecks.GlobalFiscalID.
    @ExtFiscID!: normalizedString  - Номер фискального регистратора. Указанное значение заносится в поле PrintChecks.ExtFiscID.
    @FiscShiftNum: positiveInteger  - Номер фискальной смены фискального регистратора. Указанное значение заносится в поле PrintChecks.iFiscShift.
  @CMD: string = "MakeReturnGoods"
  @persistentComment: normalizedString  - Сохраняемый комментарий заказа
  @nonPersistentComment: normalizedString  - Несохраняемый комментарий заказа
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<PrintCheck>* [PrintCheckItem]
  <Author>? [resEmployeeItem]  - Кассир, создавший чек
    (resRefItem: id | code | guid)
    <Role>? [resRefItem]  - Роль работника
  <Reason>? [refItem]  - Причина удаления чека
  <DeleteManager>? [resEmployeeItem]  - Работник, удаливший чек (структура - см. выше)
  <Pay>* [payItem]  - Оплата
    (refItem: id | code | guid)
    @uni: nonNegativeInteger  - UNI элемента. Если задан, то элемент обновляется, иначе создается новый. Только для нераспечатанных элементов
    @line_guid: guidString  - GUID строки
    @state: CheckItemState {1 | 3 | 4 | 5 | 6 | 7}  - Статус элемента (с версии 7.5.4.206)
    @* - допускаются любые другие атрибуты
    <Interface>? [refItem]  - Интерфейс, связанный с оплатой
    @amount!: int  - Сумма (в копейках)
    @basicSum: int  - Сумма платежа в базовой валюте (в копейках). Начиная с 7.6.0.087
    @cardCode: normalizedString  - Номер персональной карты
    @extTransactionInfo: normalizedString  - Расширенная информация об авторизации. Начиная с версии 7.5.3.111
    @TransactionStatus: TransactionStatusType {1 | 2 | 3 | 4 | 5 | 6}  - Статус авторизации. Начиная с версии 7.5.4.211
    @seat: nonNegativeInteger (по умолчанию "0")  - Номер посадочного места: 0 - не задано
    @discount_line_guid: guidString (по умолчанию "")  - GUID-связанной с оплатой скидкой (для оплат как скидка). Начиная с 7.6.0.087
    @deleted: boolean  - Признак того что платеж удален
    @owner: normalizedString (по умолчанию "")  - Владелец валюты (VISA, Master card). С версии 7.06.04.430+, 7.06.05.296+
    @authtype: AuthType {error | auto | voice | terminal | voicepossible} (по умолчанию "auto")  - Тип авторизации. С версии 7.06.04.430+, 7.06.05.296+
    @authcode: normalizedString (по умолчанию "")  - Код авторизации. С версии 7.06.04.430+, 7.06.05.296+
    @extIntegerInfo: int (по умолчанию "0")  - Номер банковского терминала. С версии 7.06.04.430+, 7.06.05.296+
    @transactionNumber: int (по умолчанию "0")  - Номер транзакции. С версии 7.06.04.430+, 7.06.05.296+
  <Prepay>* [prepayItem]  - Предоплата
    (refItem: id | code | guid)
    @uni: nonNegativeInteger  - UNI элемента. Если задан, то элемент обновляется, иначе создается новый. Только для нераспечатанных элементов
    @line_guid: guidString  - GUID строки
    @state: CheckItemState {1 | 3 | 4 | 5 | 6 | 7}  - Статус элемента (с версии 7.5.4.206)
    @* - допускаются любые другие атрибуты
    <Interface>? [refItem]  - Интерфейс, связанный с оплатой
    @amount!: int  - Сумма (в копейках)
    @basicSum: int  - Сумма платежа в базовой валюте (в копейках). Начиная с 7.6.0.087
    @cardCode: normalizedString  - Номер персональной карты
    @extTransactionInfo: normalizedString  - Расширенная информация об авторизации. Начиная с версии 7.5.3.111
    @TransactionStatus: TransactionStatusType {1 | 2 | 3 | 4 | 5 | 6}  - Статус авторизации. Начиная с версии 7.5.4.211
    @seat: nonNegativeInteger (по умолчанию "0")  - Номер посадочного места: 0 - не задано
    @discount_line_guid: guidString (по умолчанию "")  - GUID-связанной с оплатой скидкой (для оплат как скидка). Начиная с 7.6.0.087
    @deleted: boolean  - Признак того что платеж удален
    @owner: normalizedString (по умолчанию "")  - Владелец валюты (VISA, Master card). С версии 7.06.04.430+, 7.06.05.296+
    @authtype: AuthType {error | auto | voice | terminal | voicepossible} (по умолчанию "auto")  - Тип авторизации. С версии 7.06.04.430+, 7.06.05.296+
    @authcode: normalizedString (по умолчанию "")  - Код авторизации. С версии 7.06.04.430+, 7.06.05.296+
    @extIntegerInfo: int (по умолчанию "0")  - Номер банковского терминала. С версии 7.06.04.430+, 7.06.05.296+
    @transactionNumber: int (по умолчанию "0")  - Номер транзакции. С версии 7.06.04.430+, 7.06.05.296+
    <Reason>? [refItem]  - Причина внесения предоплаты
    @promised: boolean  - Предоплата является обещанным платежом
  @uni: nonNegativeInteger  - UNI элемента. Если задан, то элемент обновляется, иначе создается новый. Только для нераспечатанных элементов
  @line_guid: guidString  - GUID чека
  @seat: nonNegativeInteger (по умолчанию "0")  - Номер посадочного места: 0 - не задано
  @CheckNum: nonNegativeInteger  - Номер чека
  @invoice: nonNegativeInteger  - Номер накладной
  @amount!: positiveInteger  - Сумма чека (в копейках)
  @unpaidSum: int (по умолчанию "0")  - Сумма к оплате, с учетом ранее внесенных оплат/предоплат (в копейках)
  @GlobalFiscalID: string  - Глобальный фискальный номер чека
  @state: CheckItemState {1 | 3 | 4 | 5 | 6 | 7}  - Статус элемента (с версии 7.5.4.206)
  @deleted: boolean  - Флаг "Чек удален"
  @bill: boolean  - Флаг "Чек является пречеком"
  @printTime: dateTime  - Время печати чека
  @startTime: dateTime  - Время начала обслуживания чека
  @intentReceiptType: IntentReceiptType {"" | OneCheck | CreditCheck}  - Тип чека намерения (с версии 7.25.03.0)
  @intentReceiptStage: IntentReceiptStage {"" | First stage | Completed}  - Этап печати чека намерения (с версии 7.25.03.0)
<PrintCheckWarning>? [string]
```

## Пример: MakeReturnGoods

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="MakeReturnGoods">
    <Station id="{{stationId}}"/>
    <Cashier id="{{cashierId}}"/>
    <Reason id="{{returnReasonId}}"/>
    <PrintCheck line_guid="{{printCheckGuid}}"/>
    <Dishes>
      <Dish line_guid="{{dishLineGuid}}" quantity="1000"/>
    </Dishes>
  </RK7CMD>
</RK7Query>
```
