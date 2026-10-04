# GetRefList

GetRefList: Получить список имен коллекций

Схемы: `schemas/qryGetRefList.xsd`, `schemas/resGetRefList.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  @CMD!: string = "GetRefList"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<RK7RefList>
  <RK7Reference>* [RK7Reference]  - Коллекция
    @RefName: refName {122 значений, см. XSD}  - Имя коллекции
    @Count: int  - Количество элементов в коллекции
    @DataVersion: int  - Номер версии данных в коллекции. Версия увеличивается при каждом изменении данных в коллекции
  @Count!: positiveInteger  - Количество записей
```

## Пример: GetRefList

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetRefList"/>
</RK7Query>
```
