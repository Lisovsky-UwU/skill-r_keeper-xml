# GetReceiptList

[Кассовый сервер] Получить список чеков (с версии 7.5.3.202)

Схемы: `schemas/qryGetReceiptList.xsd`, `schemas/resGetReceiptList.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Order>? [refItem]  - Если задан, то возвращаются чеки для этого заказа
  @CMD: string = "GetReceiptList"
  @line_guid: normalizedString  - GUID чека. Если задан, то возвращаются данные только по этому чеку
  @lastversion: integer  - Кэшировать результат запроса. Если версия таблицы чеков совпадает с lastversion, то возвращается "No changes", иначе обычный ответ
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<ReceiptsList>
  <Receipt>* [Item]
    <Order> [resOrderElement]  - Заказ
      (orderElement: id | code | guid)
      @url: normalizedString  - URL заказа для code.ucs.ru
    <CloseStation>? [resRefItem]  - Станция, с которой чек был распечатан
    <PrintStation>? [resRefItem]  - Станция, на которой чек был распечатан
    <Cashier>? [resRefItem]  - Кассир
    <DeleteManager>? [resRefItem]  - Менеджер, удаливший чек
    <DeleteReason>? [resRefItem]  - Причина удаления чека
    @line_guid!: normalizedString  - GUID чека
    @checknum!: int  - Номер чека
    @sum: int  - Сумма чека (в копейках)
    @state!: int  - Статус чек (4 - пречек, 6 - чек, 7 - удален)
    @seat: int  - Номер посадочного места
    @printtime: dateTime  - ДатаВремя печати чека
    @starttime: dateTime  - ДатаВремя начала рассчета чека
    @billtime: dateTime  - ДатаВремя печати пречека
    @deletetime: dateTime  - ДатаВремя удаления чека
  @count: integer  - Количество чеков
  @lastversion: integer  - Версия таблицы чеков
```

## Пример: GetReceiptList

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetReceiptList"/>
</RK7Query>
```
