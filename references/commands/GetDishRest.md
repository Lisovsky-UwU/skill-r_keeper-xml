# GetDishRest

Получить остаток по блюду

Схемы: `schemas/qryGetDishRest.xsd`, `schemas/resGetDishRest.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Dish> [refItem]  - Блюдо
  @CMD: string = "GetDishRest"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
@quantity: nonNegativeInteger  - Остаток блюда (в тысячных долях)
```

## Пример: GetDishRest

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetDishRest">
    <Dish id="{{dishId}}"/>
  </RK7CMD>
</RK7Query>
```
