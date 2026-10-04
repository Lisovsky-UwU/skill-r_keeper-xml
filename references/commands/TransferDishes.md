# TransferDishes

Перенос блюд между заказами

Схемы: `schemas/qryTransferDishes.xsd`, `schemas/resTransferDishes.xsd`
Влияние: изменяет данные

## Практика

- Блюдо указывается line_guid (или uni) из GetOrder исходного заказа; без quantity переносится целиком.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <OrderSource> [orderElement]  - Заказ источник
  <OrderDest> [orderElement]  - Заказ приемник
  <Employee>? [refItem]  - Работник, от имени которого выполняется операция
  <LockStation>? [refItem]  - Станция, от имени которой будут заблокированы заказы
  <Dishes>
    <Dish>+ [TransferDishItem]
      @line_guid: normalizedString  - GUID блюда, которое нужно перенести. Если не задано, то используется uni
      @uni: int  - UNI блюда, которое нужно перенести
      @quantity: int  - Количество блюда (в тысячных долях). Если не указано, блюдо переносится целиком
  @CMD!: string = "TransferDishes"
  @source_lockguid: normalizedString (по умолчанию "")  - Токен блокировки для заказа-источника(идентификатор сессии блокировки). С версии 7.6.4.006. При блокировке заказа использовать указанный токен. Если заказ был заблокирован, то проверить токен блокировки, выдавать ошибку если заказ был заблокирован при помощи другого токена
  @dest_lockguid: normalizedString (по умолчанию "")  - Токен блокировки для заказа-приемника(идентификатор сессии блокировки). С версии 7.6.4.006. При блокировке заказа использовать указанный токен. Если заказ был заблокирован, то проверить токен блокировки, выдавать ошибку если заказ был заблокирован при помощи другого токена
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Errors>? [ErrorStack]
  <Error>*  - Стэк ошибок, возникших при выполнени команды
    (текстовое содержимое: string)
    @RK7ErrorN!: positiveInteger  - Код ошибки RK7
    @Component!: errorArea {Printer | Authorization terminal | PDS | Rights}  - Компонент, в котором была сгенерирована ошибка
@ServerVersion!: normalizedString  - Версия кассовой программы
@XmlVersion!: positiveInteger  - Версия xml протокола
@NetName: token  - Сетевое имя программы (с 7.5.3.260)
@CMD: token  - Исходная xml-команда
@Status!: string {Ok | No changes | Execution Started | Query Parse Error | Bad Query Parameters | Query Executing Error | Result Writing Error}  - Статус выполнения запроса
@RK7ErrorN: positiveInteger  - Код ошибки RK7
@ErrorText!: normalizedString  - Текст ошибки
@WorkTime!: nonNegativeInteger  - Время обработки запроса (в миллисекундах)
@DateTime!: dateTime  - Дата и время генерации ответного xml (xmlver>=39)
@Processed!: nonNegativeInteger  - Количество обработанных команд
```

## Пример: TransferDishes

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="TransferDishes">
    <OrderSource guid="{{orderGuid}}"/>
    <OrderDest guid="{{orderGuid2}}"/>
    <Employee id="{{waiterId}}"/>
    <Dishes>
      <Dish line_guid="{{dishLineGuid}}" quantity="1000"/>
    </Dishes>
  </RK7CMD>
</RK7Query>
```
