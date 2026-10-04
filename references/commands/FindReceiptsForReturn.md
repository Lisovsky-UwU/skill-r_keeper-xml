# FindReceiptsForReturn

Поиск чеков для возврата

Схемы: `schemas/qryFindReceiptsForReturn.xsd`, `schemas/resFindReceiptsForReturn.xsd`
Влияние: только чтение

## Практика

- Без узких фильтров (CheckNum, CloseTime) ищет по всем чекам - даже на маленькой базе это 10+ секунд.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Station> [refItem]  - Станция, от имени которой осуществляется поиск
  <Cashier> [refItem]  - Кассир, от имени которого осуществляется поиск
  <CheckNum>? [RangeFilter]  - Фильтр по номеру чека
    @Value: string  - Значение фильтра (может быть указано в формате "Наименьшее значение"chr(#10)"Наибольшее значение")
    @ValueL: string  - Наименьшее значение фильтра (игнорируется, если задано значнеие атрибута value)
    @ValueH: string  - Наибольшее значение фильтра (игнорируется, если задано значнеие атрибута value)
  <Comment>? [ValueFilter]  - Фильтр по комментарию
    @Value: string  - Значение фильтра
  <Employee>? [ValueFilter]  - Фильтр по основному официанту (структура - см. выше)
  <Table>? [ValueFilter]  - Фильтр по номеру стола (структура - см. выше)
  <CardCode>? [ValueFilter]  - Фильтр по номеру карты (структура - см. выше)
  <Dish>? [ValueFilter]  - Фильтр по блюду (структура - см. выше)
  <Currency>? [ValueFilter]  - Фильтр по использованной валюте (структура - см. выше)
  <PaySum>? [RangeFilter]  - Фильтр по сумме чека (структура - см. выше)
  <CloseTime>? [RangeFilter]  - Фильтр по времени закрытия (структура - см. выше)
  <COT>? [ValueFilter]  - Фильтр по типу заказа (структура - см. выше)
  <UOT>? [ValueFilter]  - Фильтр по категории заказа (структура - см. выше)
  <StartTime>? [RangeFilter]  - Фильтр по времени создания (структура - см. выше)
  <CustomProp>? [ValueFilter]  - Фильтр по использованным пользовательским свойствам (структура - см. выше)
  <INN>? [ValueFilter]  - Фильтр по ИНН сотрудника (структура - см. выше)
  <FiscalDevice>? [ValueFilter]  - Фильтр по идентификатору фискального устройства (структура - см. выше)
  <FiscalReportNumber>? [RangeFilter]  - Фильтр по фискальному номеру (структура - см. выше)
  @CMD!: string = "FindReceiptsForReturn"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Items>
  <Receipt>* [ReceiptItem]  - Информация о чеке
    @CheckUNI: int  - UNI чека
    @CheckNum: int  - Номер чека
    @BasicSum: int  - Сумма чека в базовой валюте
    @iAuthor: int  - Идентификатор официанта, создавшего чек
    @iCloseStation: int  - Идентификатор станции, на которой чек был закрыт
    @iPrintStation: int  - Идентификатор станции, на которой чек был распечатан
    @iPrinter: int  - Идентификатор принтера, на который был распечатан чек
    @CloseDateTime: dateTime  - Дата-время печати чека
    @iDrawer: int  - Идентификатор ящика
    @OrderId: int  - Идентификатор заказа
    @Midserver: int  - Идентификатор кассового сервера
    @TableName: int  - Название стола
    @OrderName: int  - Название заказа
    @INN: int  - ИНН сотрудника, создавшего чек
    @GlobalFiscalID: int  - Фискальный номер документа
    @GuidString: guidString  - GUid чека
```

## Пример: FindReceiptsForReturn

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="FindReceiptsForReturn">
    <Station id="{{stationId}}"/>
    <Cashier id="{{cashierId}}"/>
    <CheckNum ValueL="1" ValueH="999999"/>
  </RK7CMD>
</RK7Query>
```
