# GetOrderMenu

Получение списка доступных блюд и модификаторов

Схемы: `schemas/qryGetOrderMenu.xsd`, `schemas/resGetOrderMenu.xsd`
Влияние: только чтение

## Практика

- Комбо-блюдо есть в <Dishes> со своей ценой, комбо-элементы - в <Modifiers> со своей ценой: это цена блюда внутри комбо, она может отличаться от цены самого блюда (проверено).
- Цена модификатора в <Modifiers> отдается всегда, независимо от ChangesPrice группы в схеме блюда: по ней нельзя понять, начислит ли сервер модификатор в заказе - смотри MODISCHEMEDETAILS ChangesPrice (проверено).
- Блюдо на стопе (SetDishRests prohibited="1") пропадает из <Dishes>, и вместе с ним из <Modifiers> пропадают комбо-элементы с этим блюдом. Блюдо с нулевым остатком (quantity="0") тоже пропадает из <Dishes>, но его комбо-элементы в <Modifiers> остаются - закончившийся компонент комбо видно только по GetDishRests. Остаток блюда - атрибут quantity у <Item> в <Dishes>; у комбо-элементов его нет (проверено).

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
  @CMD: string = "GetOrderMenu"
  @dateTime: dateTime  - Время, на которое нужно получить список блюд
  @checkrests: boolean (по умолчанию "true")  - Нужно ли проверять ограничения по остаткам блюд
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
<Modifiers>?  - Список доступных модификаторов
  <Item>* [uModiItem]
    @Ident: positiveInteger  - Идентификатор
    @ID: positiveInteger  - Идентификатор (оставлен для совместимости)
    @Price: int  - Цена (в копейках)
<OrderTypes>  - Список доступных типов заказа
  <Item>* [OrderTypeItem]
    @Ident: positiveInteger  - Идентификатор
```

## Пример: GetOrderMenu

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetOrderMenu" checkrests="1">
    <Station id="{{stationId}}"/>
  </RK7CMD>
</RK7Query>
```
