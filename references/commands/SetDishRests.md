# SetDishRests

[Кассовый сервер] Изменить остатки блюд

Схемы: `schemas/qrySetDishRests.xsd`, `schemas/resSetDishRests.xsd`
Влияние: изменяет данные

## Практика

- Reason - причина из ORDERVOIDS с флагом "При добавлении блюда в стоп-лист" (ImplOnAddDishInStopList); без такой причины сервер отказывает даже при prohibited="0".
- storeZeroQuantity="1" у DishRest - хранить нулевой остаток, а не удалять блюдо из списка остатков (по умолчанию false).

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Author> [refItem]  - Работник
  <Reason> [refItem]  - Причина добавления блюда в стоп-лист, учитывается только при значении поля prohibited = true
  <DishRest>*
    @id: nonNegativeInteger
    @code: nonNegativeInteger
    @guid: guidString
    @quantity: nonNegativeInteger  - Остаток блюда (в тысячных долях)
    @prohibited: boolean  - Запретить/разрешить продажу блюда. Если prohibited = true, то продажа блюда запрещена, если prohibited = false, то продажа блюда разрешена
    @storeZeroQuantity: boolean  - Флаг хранения нулевых остатков блюда (если true, то удалять не нужно; если false, то удалять блюдо с нулевым количеством). Если не передан, по умолчанию false.
  @CMD: string = "SetDishRests"
```

## Пример: SetDishRests

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="SetDishRests">
    <Author id="{{managerId}}"/>
    <Reason id="{{deleteReasonId}}"/>
    <DishRest id="{{dishId}}" quantity="10000"/>
  </RK7CMD>
</RK7Query>
```
