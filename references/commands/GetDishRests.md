# GetDishRests

[Кассовый сервер] Получить список остатков блюд

Схемы: `schemas/qryGetDishRests.xsd`, `schemas/resGetDishRests.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  @CMD: string = "GetDishRests"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<DishRest>*
  <Reason>? [resRefItem]  - Причина добавления блюда в стоп-лист
  @id: nonNegativeInteger  - Идентификатор блюда
  @code: nonNegativeInteger  - Код блюда
  @name: normalizedString  - Название блюда
  @quantity: nonNegativeInteger  - Остаток блюда (в тысячных долях)
  @prohibited: boolean  - Флаг - запрещена продажа блюда
```

## Пример: GetDishRests

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetDishRests"/>
</RK7Query>
```
