# AddBatchOfGoods

[Кассовый сервер] Регистрация партии маркированной продукции

Схемы: `schemas/qryAddBatchOfGoods.xsd`, `schemas/resAddBatchOfGoods.xsd`
Влияние: изменяет данные

## Практика

- Ответ - <Batch quantity srcQuantity markingData gtin startDateTime>: GTIN определяется по марке. Атрибут name сервер 7.26 не сохраняет (в ответе пустой).
- Список партий - GetBatchOfGoodsList (команда без XSD, объявлена в GetFunctions); удалить - DeleteBatchOfGoods с той же маркой.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Batch>
    @markingData!: base64binary  - Строка с данными в base64 формате
    @quantity!: nonNegativeInteger  - Остаток блюда (в тысячных долях)
  <Author> [refItem]  - Сотрудник, выполнивший регистрацию партии
  <Station> [refItem]  - Станция, на которой была зарегистрирована партия
  @CMD!: string = "AddBatchOfGoods"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Batch>
  @name!: normalizedString  - Наименование продукта
  @quantity!: nonNegativeInteger  - Остаток блюда (в тысячных долях)
  @markingData!: base64binary  - Строка с данными в base64 формате
  @gtin!: gtinString  - ГТИН из марки
  @startDateTime!: dateTime  - Дата и время добавления партии
```

## Пример: AddBatchOfGoods

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="AddBatchOfGoods">
    <Batch markingData="{{markingData}}" name="Тестовая партия" quantity="1000"/>
    <Author id="{{managerId}}"/>
    <Station id="{{stationId}}"/>
  </RK7CMD>
</RK7Query>
```
