# TerminalAuthStart

Авторизация карты через терминал: старт

Схемы: `schemas/qryTerminalAuthStart.xsd`, `schemas/resTerminalAuthStart.xsd`
Влияние: изменяет данные

## Практика

- Добавляет в заказ обещанную (promised) предоплату; закрывается TerminalAuthPay (успех) или TerminalAuthError (отмена).

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Order> [orderElement]  - Заказ
  <Currency> [refItem]  - Валюта
  <Waiter> [refItem]  - Кассир, от имени которого прокатывается карточка
  <LockStation>? [refItem]  - Станция, от имени которой будет заблокирован заказ. С версии 7.6.4.009.
  @CMD: string = "TerminalAuthStart"
  @lockguid: guidString (по умолчанию "")  - Токен блокировки (идентификатор сессии блокировки). С версии 7.6.4.009. При блокировке заказа использовать указанный токен. Если заказ был заблокирован, то проверить токен блокировки, выдавать ошибку если заказ был заблокирован при помощи другого токена
  @amount!: nonNegativeInteger  - Сумма к оплате (в копейках)
  @asPrepayment: boolean  - Провести платеж как предоплату
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

## Пример: TerminalAuthStart

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="TerminalAuthStart" amount="100" asPrepayment="1">
    <Order guid="{{orderGuid}}"/>
    <Currency id="{{cardCurrencyId}}"/>
    <Waiter id="{{cashierId}}"/>
  </RK7CMD>
</RK7Query>
```
