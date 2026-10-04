# PrintBill

[Кассовый сервер] Печать пречека

Схемы: `schemas/qryPrintBill.xsd`, `schemas/resPrintBill.xsd`
Влияние: изменяет данные

## Практика

- Может быть запрещен параметром "Печатать пречек с чеком намерения" - тогда ошибка с этим текстом.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Order> [orderElement]  - Заказ
  <Station> [refItem]  - Станция
  <Cashier> [refItem]  - Кассир
  <Maket>? [refItem]  - Представление документа для пречека. Если не задано, то представление опредляется по схеме печати
  @CMD: string = "PrintBill"
  @lockguid: normalizedString (по умолчанию "")  - Токен блокировки (идентификатор сессии блокировки). С версии 7.6.4.009. При блокировке заказа использовать указанный токен. Если заказ был заблокирован, то проверить токен блокировки, выдавать ошибку если заказ был заблокирован при помощи другого токена
  @bySeats: boolean  - true - пречек по местам, false - общий пречек
  @seat: nonNegativeInteger  - Номер места, по которому будет распечатан пречек (при расчете по местам). xmlver=32
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

## Пример: PrintBill

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="PrintBill">
    <Order guid="{{orderGuid}}"/>
    <Station id="{{stationId}}"/>
    <Cashier id="{{cashierId}}"/>
  </RK7CMD>
</RK7Query>
```
