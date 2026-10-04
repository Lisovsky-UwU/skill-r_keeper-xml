# GetFunctions

[ВСЕ] Список поддерживаемых XML-функций

Схемы: `schemas/qryGetFunctions.xsd`, `schemas/resGetFunctions.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  @CMD: string = "GetFunctions"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Query>*
  @name: normalizedString  - Имя xml-запроса
  @deprecated: boolean  - Флаг - устаревший запрос (не рекомендуется использовать)
```

## Пример: GetFunctions

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetFunctions"/>
</RK7Query>
```
