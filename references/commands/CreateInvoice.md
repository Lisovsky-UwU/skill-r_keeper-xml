# CreateInvoice

[Кассовый сервер] Создать счет/фактуру, привязать к заказу

Схемы: `schemas/qryCreateInvoice.xsd`, `schemas/resCreateInvoice.xsd`
Влияние: изменяет данные

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Order> [orderElement]  - Заказ
  <Invoice> [invoiceItem]  - Счет-фактура
    @guid: guidString  - GUID счет/фактуры
    @regno!: normalizedString  - ИНН
    @name!: normalizedString  - Наименование
    @address: normalizedString  - Адрес
    @extrainfo: normalizedString  - Доп.инфо
    @comment: normalizedString  - Комментарий
  @CMD: string = "CreateInvoice"
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

## Пример: CreateInvoice

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="CreateInvoice">
    <Order guid="{{orderGuid}}"/>
    <Invoice regno="7700000000" name="ООО Ромашка" address="г. Москва" comment="example"/>
  </RK7CMD>
</RK7Query>
```
