# KDSGetDishData2

[Кассовый север] КДС: Получить данные по блюдам и заказам. Начиная с 7.5.3.222, 7.5.4.068

Схемы: `schemas/qryKDSGetDishData2.xsd`, `schemas/resKDSGetDishData2.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  @CMD: string = "KDSGetDishData2"
  @lastversion: int  - Кэшировать результат запроса. Если lastversion совпадает с контрольной суммой, то возвращается "No changes", иначе обычный ответ
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Orders>
  <Order>* [KDSOrderItem]
    <Waiter> [resRefItem]  - Главный официант заказа
    <OrderCategory>? [resRefItem]  - Категория заказа
    <OrderType>? [resRefItem]  - Категория заказа
    <Table>? [resRefItem]  - Стол
    <Session>+ [KDSSessionItem]  - Пакет
      <Station>? [resRefItem]  - Касса, на которой пакет был добавлен
      <Course>? [resRefItem]  - Порядок подачи
      <DishData> [KDSDishData]  - Список блюд
        <Dish>+ [KDSDishItem]
          <ModiData>?
            <Modi>+ [KDSModiItem]
              @line_guid: normalizedString  - GUID строки
              @id: nonNegativeInteger  - Идентификатор модификатора
              @openname: normalizedString  - Имя модификатора
              @count: integer  - Кол-во модификаторов (начиная с 7.5.5.104+)
            @count: integer  - Количество заказов
          @line_guid: normalizedString  - GUID строки
          @id: nonNegativeInteger  - Идентификатор блюда
          @quantity!: int  - Количество блюда (в тысячных долях)
          @seqnum!: int  - Уникальный последовательный номер блюда
          @stream!: int  - Идентификатор категории блюд (потока сервис-печати)
          @parent_guid: normalizedString  - GUID комбо-блюда. Заполняется для комбо-компонентов
          @state: int  - Статус блюда (с версии 7.5.4.150)
          @kdsstate: int  - КДС статус блюда (с версии 7.5.4.156)
          @seat: nonNegativeInteger  - Номер места
          @seatname: normalizedString  - Тестовая метка места
          @source_line_guid: normalizedString  - GUID исходной строки с блюдом. Если блюдо было перенесено из другого заказа, то в этом поле записывается line_guid исходной строки с блюдом
        @count: integer  - Количество блюд
      @line_guid: normalizedString  - GUID пакета
      @senttime: dateTime  - Время отправки на КДС
      @seqnum!: int  - Уникальный последовательный номер пакета
    @guid!: normalizedString  - GUID заказа
    @seqnum!: int  - Уникальный последовательный номер заказа
    @comment: normalizedString  - Сохраняемый комментарий
    @nonpersistentcomment: normalizedString  - Несохраняемый комментарий
  @count: integer  - Количество заказов
@lastversion: integer  - Контрольная сумма, посчитанная по используемым таблицам
```

## Пример: KDSGetDishData2

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="KDSGetDishData2"/>
</RK7Query>
```
