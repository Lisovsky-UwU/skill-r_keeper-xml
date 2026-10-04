# GetModifierStopList

[Кассовый сервер] Получить стоп-лист по модификаторам

Схемы: `schemas/qryGetModifierStopList.xsd`, `schemas/resGetModifierStopList.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  @CMD: string = "GetModifierStopList"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Modifier>* [resRefItem]  - Модификатор
```

## Пример: GetModifierStopList

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetModifierStopList"/>
</RK7Query>
```
