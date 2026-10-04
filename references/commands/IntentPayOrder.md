# IntentPayOrder

[Кассовый сервер] Печать чека намерения, с 7.25.04.0

Схемы: `schemas/qryIntentPayOrder.xsd`, `schemas/resIntentPayOrder.xsd`
Влияние: изменяет данные

## Практика

- Создает чек намерения: <PrintCheck state="3" intentReceiptType="OneCheck" intentReceiptStage="First stage"> с платежом promised="1"; у заказа unpaidSum становится 0, сумма уходит в promisedSum. Одновременно печатается пречек (bill="1").
- Если включен параметр "Печатать пречек с чеком намерения", PrintBill запрещен - пречек печатается через IntentPayOrder.
- Отменяется CorrectIntentReceipt.

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
  <Station> [refItem]  - Станция
  <Cashier> [refItem]  - Кассир
  <ReceiptMaket>? [refItem]  - Представление документа для чека
  <InvoiceMaket>? [refItem]  - Представление документа для счет-фактуры
  <BillMaket>? [refItem]  - Представление документа для пречека
  <FiscalDocInfo>? [poFiscalDocInfo]  - Информация о фискальном документе. Для использования в отчетах. Работает только при нефискальной печати, в случае фискального чека данный тэг игнорируется
    <FiscDev>? [refItem]  - Тип фискального устройства. Указанное значение заносится в поле PrintChecks.FiscDev
    @PrintNumber!: nonNegativeInteger  - Печатный номер чека, в России номер чека ФН. Указанное значение заносится в поле PrintChecks.PrintNumber.
    @FiscDocNumber!: nonNegativeInteger  - Фискальный номер документа, в России номер документа ФН. Указанное значение заносится в поле PrintChecks.FiscDocNumber.
    @GlobalFiscalId: normalizedString  - Глобальный номер чека, в России не используется. Указанное значение заносится в поле PrintChecks.GlobalFiscalID.
    @ExtFiscID!: normalizedString  - Номер фискального регистратора. Указанное значение заносится в поле PrintChecks.ExtFiscID.
    @FiscShiftNum: positiveInteger  - Номер фискальной смены фискального регистратора. Указанное значение заносится в поле PrintChecks.iFiscShift.
  (одно из - повторяется:)
    <Payment> [poPaymentItem]  - Общий платеж. Разделяется между всеми чеками заказа
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
      <TipCharge>? [refItem]  - Наценка в чаевые
      <TerminalMaket>? [refItem]  - Представление документа для терминала авторизации
      @tipAmount: positiveInteger  - Сумма чаевых (в копейках)
      @terminalNumber: normalizedString  - Пользовательский номер терминала. Если задан, то для авторизации будет выбран терминал, у которого в настройках указан такой же TerminalNumber. С версии 7.07.00.287.
      @sbpPayGuid: normalizedString  - Идентификатор СБП платежа. Используется при необходимости отмены платежа до его подтверждения на стороне банка
    <PrintCheck> [poPrintCheckItem]  - Чек с платежами. Идентифицируется seat или line_guid
      <Payment>* [poPaymentItem]  - Платежи чека (структура - см. выше)
      @line_guid: normalizedString  - GUID чека
      @seat: nonNegativeInteger  - Номер места
  @CMD: string = "IntentPayOrder"
  @lockguid: normalizedString  - Токен блокировки (идентификатор сессии блокировки). С версии 7.6.4.005
  @pdsPaysTimeout: integer (по умолчанию "0")  - Время в милисекундах, которое отведено на подтверждение ПДС оплат. 0 - таймаута нет. Версия 7.7.0.306+
  @calcBySeats: boolean  - true - рассчет по местам, false - общий чек
  @sendtovdu: boolean (по умолчанию "true")  - Флаг "Отправить заказ на VDU". Если включен, то заказ будет передан на VDU, иначе не будет. Версия 7.5.8.065+
  @seat: integer  - Номер посадочного места
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

## Пример: IntentPayOrder

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="IntentPayOrder">
    <Order guid="{{orderGuid}}"/>
    <Station id="{{stationId}}"/>
    <Cashier id="{{cashierId}}"/>
    <Payment id="{{currencyId}}" amount="{{orderSum}}"/>
  </RK7CMD>
</RK7Query>
```
