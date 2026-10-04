# UndoBill

[Кассовый сервер] Отмена пречека

Схемы: `schemas/qryUndoBill.xsd`, `schemas/resUndoBill.xsd`
Влияние: изменяет данные

## Практика

- seat="0" отменяет все пречеки заказа.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Order> [orderElement]  - Заказ
  <Station> [refItem]  - Станция
  <Cashier> [refItem]  - Кассир
  <Maket>? [refItem]  - Представление документа для отмены пречека. Если не задано, то представление опредляется по схеме печати
  <DeleteReason>? [deleteReasonItem]  - Причина отмены пречека
    (refItem: id | code | guid)
    @openName: normalizedString  - Произвольное имя для причины удаления. С версии 7.6.4.417
  @CMD: string = "UndoBill"
  @lockguid: guidString (по умолчанию "")  - Токен блокировки (идентификатор сессии блокировки). С версии 7.6.4.009. При блокировке заказа использовать указанный токен. Если заказ был заблокирован, то проверить токен блокировки, выдавать ошибку если заказ был заблокирован при помощи другого токена
  @seat: nonNegativeInteger  - Номер места, для которого будет отменен пречек. Если 0, то будут отменены все пречеки
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

## Пример: UndoBill

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="UndoBill" seat="0">
    <Order guid="{{orderGuid}}"/>
    <Station id="{{stationId}}"/>
    <Cashier id="{{cashierId}}"/>
    <DeleteReason id="{{deleteReasonId}}"/>
  </RK7CMD>
</RK7Query>
```
