# GetOrderBindings

Получение биндингов по заказу

Схемы: `schemas/qryGetOrderBindings.xsd`, `schemas/resGetOrderBindings.xsd`
Влияние: только чтение

## Практика

- Для обычного заказа возвращает только ссылку на сам заказ (<Order visit orderIdent guid>).

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Order> [orderElement]  - Заказ
  @CMD: string = "GetOrderBindings"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Order> [OrderItem]
  <PrintCheck>* [PrintCheckType]  - Список чеков
    <CurrLine>+ [CurrLineType]  - Список платежей чека
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
      <Binding>* [BindingType]  - Биндинг
        <DiscPart>* [DiscPartType]  - Элемент скидки
          @disc_line_guid: string  - GUID скидки
          @amount: long  - Сумма скидки в базовой валюте (в копейках)
          @bonussum: long  - Сумма бонуса в базовой валюте (в копейках)
        <TaxPart>* [TaxPartType]  - Элемент налога
          @id: int  - Идентификатор налога
          @code: int  - Код налога
          @name: normalizedString  - Имя налога
          @amount: long  - Сумма налога (в копейках)
          @rate: long  - Ставка налога (в сотых долях)
          @rateid: int  - Идентификатор ставки налога, с версии 7.6.5.301
        @line_guid: string  - GUID блюда или нераспределяемой наценки
        @amount: long  - Сумма в базовой валюте (в копейках)
        @quantity: long  - Количество блюда (в тысячных долях)
    @line_guid: string  - GUID чека
    @state: CheckItemState {1 | 3 | 4 | 5 | 6 | 7}  - Статус чека
    @CheckNum: nonNegativeInteger  - Номер чека
  @guid: normalizedString
  @visit: positiveInteger
  @orderIdent: positiveInteger
```

## Пример: GetOrderBindings

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetOrderBindings">
    <Order guid="{{orderGuid}}"/>
  </RK7CMD>
</RK7Query>
```
