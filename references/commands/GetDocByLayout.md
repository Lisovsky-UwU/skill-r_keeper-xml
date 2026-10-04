# GetDocByLayout

[Кассовый сервер] Получить данные по макету печати. УСТАРЕВШИЙ!!! Рекомендуется использовать GetPrintLayout

Схемы: `schemas/qryGetDocByLayout.xsd`, `schemas/resGetDocByLayout.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Layout> [refItem]  - Макет
  <Order>? [orderElement]  - Заказ
  @CMD: string = "GetDocByLayout"
  @LayoutFilters: normalizedString  - Фильтры для макета вида поле=значение[{;поле=значение}]
  @DataSourceParams: normalizedString  - Фильтры для куба вида поле=значение[{;поле=значение}]
  @TextReport: boolean  - Флаг - выводить отчет в виде текста, иначе в виде xml
  @ReceiptNum: int  - Номер чека (чтобы напечатать макет по конкретному чеку)
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<LayoutResult>  - Строка с данными макета печати
  (текстовое содержимое: string)
  @LayoutCode: int  - Код выбранного макета
  @LayoutFilters: normalizedString  - Фильтры для макета вида поле=значение[{;поле=значение}]
  @DataSourceParams: normalizedString  - Фильтры для куба вида поле=значение[{;поле=значение}]
```

## Пример: GetDocByLayout

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetDocByLayout" TextReport="1">
    <Layout id="1"/>
    <Order guid="{{orderGuid}}"/>
  </RK7CMD>
</RK7Query>
```
