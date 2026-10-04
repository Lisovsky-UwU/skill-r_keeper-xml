# DeleteReceiptPayments

[Кассовый сервер] Удалить оплаты в ошибочном чеке

Схемы: `schemas/qryDeleteReceiptPayments.xsd`, `schemas/resDeleteReceiptPayments.xsd`
Влияние: **опасно** - необратимые или массовые изменения, блокировка кассы

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Order> [refItem]  - Заказ
  <Manager> [refItem]  - Менеджер
  <LockStation>? [refItem]  - Станция, от имени которой будет заблокирован заказ. С версии 7.6.4.009.
  (одно из - повторяется:)
    <Pay> [LineGuidItem]  - GUID платежа, который нужно удалить
      @line_guid: normalizedString  - GUID строки
    <PrintCheck> [LineGuidItem]  - GUID чека, в котором нужно удалить оплаты (структура - см. выше)
  @CMD: string = "DeleteReceiptPayments"
  @lockguid: guidString (по умолчанию "")  - Токен блокировки (идентификатор сессии блокировки). С версии 7.6.4.009. При блокировке заказа использовать указанный токен. Если заказ был заблокирован, то проверить токен блокировки, выдавать ошибку если заказ был заблокирован при помощи другого токена
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Errors>? [ErrorStack]
  <Error>*  - Стэк ошибок, возникших при выполнени команды
    (текстовое содержимое: string)
    @RK7ErrorN!: positiveInteger  - Код ошибки RK7
    @Component!: errorArea {Printer | Authorization terminal | PDS | Rights}  - Компонент, в котором была сгенерирована ошибка
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

## Пример: DeleteReceiptPayments

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="DeleteReceiptPayments">
    <Order guid="{{orderGuid}}"/>
    <Manager id="{{managerId}}"/>
    <PrintCheck line_guid="{{printCheckGuid}}"/>
  </RK7CMD>
</RK7Query>
```
