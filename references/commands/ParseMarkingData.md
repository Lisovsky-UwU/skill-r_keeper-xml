# ParseMarkingData

[Кассовый сервер] Определение ГТИНа по марке

Схемы: `schemas/qryParseMarkingData.xsd`, `schemas/resParseMarkingData.xsd`
Влияние: только чтение

## Практика

- Ответ - <Data gtin="..."/>. Разделитель GS (0x1D) марки должен быть внутри данных до кодирования в base64.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  @CMD!: string = "ParseMarkingData"
  @base64data!: base64binary  - Строка с данными в base64 формате
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Data>
  @gtin!: gtinString  - ГТИН из марки
```

## Пример: ParseMarkingData

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="ParseMarkingData" base64data="{{markingData}}"/>
</RK7Query>
```
