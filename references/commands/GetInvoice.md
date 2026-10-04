# GetInvoice

[Кассовый сервер] Получить содержимое счет/фактуры. Указать нужно либо заказ, либо guid счет/фактуры

Схемы: `schemas/qryGetInvoice.xsd`, `schemas/resGetInvoice.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  (одно из:)
    <Order> [orderElement]  - Заказ
    <Invoice>  - GUID счет/фактуры
      @guid!: normalizedString  - GUID счет/фактуры
  @CMD: string = "GetInvoice"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Invoice> [invoiceItem]  - Счет/фактура
  @guid: guidString  - GUID счет/фактуры
  @regno!: normalizedString  - ИНН
  @name!: normalizedString  - Наименование
  @address: normalizedString  - Адрес
  @extrainfo: normalizedString  - Доп.инфо
  @comment: normalizedString  - Комментарий
```

## Пример: GetInvoice

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetInvoice">
    <Order guid="{{orderGuid}}"/>
  </RK7CMD>
</RK7Query>
```
