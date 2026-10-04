# TerminalAuthPay

Авторизация карты через терминал: оплата

Схемы: `schemas/qryTerminalAuthPay.xsd`, `schemas/resTerminalAuthPay.xsd`
Влияние: изменяет данные

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Order> [orderElement]  - Заказ
  <LockStation>? [refItem]  - Станция, от имени которой будет заблокирован заказ. С версии 7.6.4.009.
  @CMD: string = "TerminalAuthPay"
  @lockguid: guidString (по умолчанию "")  - Токен блокировки (идентификатор сессии блокировки). С версии 7.6.4.009. При блокировке заказа использовать указанный токен. Если заказ был заблокирован, то проверить токен блокировки, выдавать ошибку если заказ был заблокирован при помощи другого токена
  @transactionID: int  - ID транзакции
  @extTransactionInfo: normalizedString  - Внешний код авторизации
  @authCode: normalizedString  - Код авторизации
  @owner: normalizedString  - Владелец карты
  @cardCode: normalizedString  - Номер карты (для отображения)
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Errors>? [ErrorStack]
  <Error>*  - Стэк ошибок, возникших при выполнени команды
    (текстовое содержимое: string)
    @RK7ErrorN!: positiveInteger
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

## Пример: TerminalAuthPay

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="TerminalAuthPay" transactionID="1" authCode="000000" cardCode="**** 0000">
    <Order guid="{{orderGuid}}"/>
  </RK7CMD>
</RK7Query>
```
