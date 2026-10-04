# GetOrderMenu2

Получение списка доступных блюд и модификаторов

Схемы: `schemas/qryGetOrderMenu2.xsd`, `schemas/resGetOrderMenu2.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Station> [refItem]  - Станция
  <Order>? [orderElement]  - Заказ
  <Waiter>? [refItem]  - Официант
  <Table>? [refItem]  - Стол
  <OrderCategory>? [refItem]  - Категория заказа
  <OrderType>? [refItem]  - Тип заказа
  <GuestType>? [refItem]  - Тип гостей
  <Course>? [refItem]  - Порядок подачи
  <Dishes>?  - Список свойств блюд, которые должны быть в ответе
    <Item>* [refItem]
  <Modifiers>?  - Список свойств модификаторов, которые должны быть в ответе
    <Item>* [refItem]
  <OrderTypes>?  - Список свойств типов заказа, которые должны быть в ответе
    <Item>* [refItem]
  @CMD: string = "GetOrderMenu2"
  @dateTime: dateTime  - Время, на которое нужно получить список блюд
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<PriceScale> [resRefItem]  - Тип цены, используемый для содержимого пакета
<TradeGroup> [resRefItem]  - Торговая группа
<Dishes>  - Список доступных блюд
  <Item>* [uDishItem]
    @Ident: positiveInteger  - Идентификатор
    @Price: nonNegativeInteger  - Цена (в копейках)
    @quantity: nonNegativeInteger  - Остаток блюда (в тысячных долях). Если не задан, то остаток не ограничен
    @Avail: boolean  - Признак доступности блюда
<Modifiers>?  - Список доступных модификаторов
  <Item>* [uModiItem]
    @Ident: positiveInteger  - Идентификатор
    @ID: positiveInteger  - Идентификатор (оставлен для совместимости)
    @Price: int  - Цена (в копейках)
    @Avail: boolean  - Признак доступности модификатора
<OrderTypes>  - Список доступных типов заказа
  <Item>* [OrderTypeItem]
    @Ident: positiveInteger  - Идентификатор
    @Avail: boolean  - Признак доступности типа заказа
```

## Пример: GetOrderMenu2

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetOrderMenu2">
    <Station id="{{stationId}}"/>
    <Dishes>
      <Item id="{{dishId}}"/>
    </Dishes>
  </RK7CMD>
</RK7Query>
```
