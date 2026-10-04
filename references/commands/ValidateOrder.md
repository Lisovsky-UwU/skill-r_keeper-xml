# ValidateOrder

Проверка корректности заказа

Схемы: `schemas/qryValidateOrder.xsd`, `schemas/resValidateOrder.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Order>? [orderElement]  - Заказ
  <Table>? [refItem]  - Стол, на который оформляется заказ
  <OrderCategory>? [refItem]  - Категория заказа
  <GuestType>? [refItem]  - Тип гостей
  <Session>+ [sessionItem]  - Пакет
  @CMD: string = "ValidateOrder"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Error>* [ErrorItem]  - Список ошибочных записей
  <FaultyTag>  - Сбойный тэг
    <любой XML>
  @RK7ErrorN!: positiveInteger  - Код ошибки RK7
  @ErrorText!: normalizedString  - Текст ошибки
<Session>*
  @sessionID!: positiveInteger  - ID пакета
```

## Пример: ValidateOrder

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="ValidateOrder">
    <Order guid="{{orderGuid}}"/>
    <Session>
      <Dish id="{{dishId}}" quantity="1000"/>
    </Session>
  </RK7CMD>
</RK7Query>
```
