# GetPrintLayout

[Кассовый сервер] Получить данные по макету печати

Схемы: `schemas/qryGetPrintLayout.xsd`, `schemas/resGetPrintLayout.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  (одно из:)
    <ReceiptNum>? [int]  - Номер чека (чтобы напечатать макет по конкретному чеку)
    <Order>? [orderElement]  - Заказ
  (одно из:)
    <Layout> [refItem]  - Макет
    <Document> [refItem]  - Тип документа. Используется если не задан макет
  @CMD: string = "GetPrintLayout"
  @LayoutFilters: normalizedString  - Фильтры для макета вида поле=значение[{;поле=значение}]
  @DataSourceParams: normalizedString  - Фильтры для куба вида поле=значение[{;поле=значение}]
  @format: string {xml | txt | xls | odt | ods | pdf | html} (по умолчанию "xml")  - В каком формате нужно вернуть отчет: xls, pdf, html, xml, text
  @EncodeBase64: boolean  - Закодировать ответ в base64
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<LayoutResult> [string]  - Строка с данными макета печати
```

## Пример: GetPrintLayout

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetPrintLayout" format="txt">
    <Order guid="{{orderGuid}}"/>
    <Document id="1"/>
  </RK7CMD>
</RK7Query>
```
