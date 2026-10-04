# GetSelectedDishes

[Кассовый сервер] Получить список избранных блюд

Схемы: `schemas/qryGetSelectedDishes.xsd`, `schemas/resGetSelectedDishes.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  @CMD: string = "GetSelectedDishes"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Dish>* [refItem]  - Избранное блюдо
```

## Пример: GetSelectedDishes

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetSelectedDishes"/>
</RK7Query>
```
