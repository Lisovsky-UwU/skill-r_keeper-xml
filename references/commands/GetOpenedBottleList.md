# GetOpenedBottleList

GetOpenedBottleList: Получить список вскрытых бутылок

Схемы: `schemas/qryGetOpenedBottleList.xsd`, `schemas/resGetOpenedBottleList.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Station>? [refItem]  - Станция. Если заполнен, то при вызове выполняется синхронизация списка бутылок с учетной системой
  @CMD!: string = "GetOpenedBottleList"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Bottle>* [resBottle]
  <Author> [refItem]  - Работник, вскрывший бутылку
  <Station> [refItem]  - Станция, на которой была вскрыта бутылка
  @markingData!: base64Binary  - Марка PDF-417 в формате base64
  @ean!: long  - EAN марка
  @startDateTime: dateTime  - Дата-время добавления записи
  @bottleVolume!: integer  - Объем бутылки
  @restVolume!: integer  - Остаток в бутылке
  @isOldRest!: boolean  - Признак того, что бутылка уже была вскрытой
```

## Пример: GetOpenedBottleList

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetOpenedBottleList"/>
</RK7Query>
```
