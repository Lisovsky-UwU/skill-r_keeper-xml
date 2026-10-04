# GetItemBlob

Выполнение запроса AnyInfo на сервере FarCards

Схемы: `schemas/qryGetItemBlob.xsd` (схемы ответа нет)
Влияние: только чтение

## Практика

- Если поле пустое, сервер отвечает Status="Ok" без данных.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
(одно из:)
  <RK7CMD> [GetItemBlob]
    @CMD!: string = "GetItemBlob"
    @RefName!: refName {114 значений, см. XSD}  - Название коллекции
    @RefItemIdent: integer  - Идентификатор элемента (если надо запросить один элемент), если задан, то атрибуты тэга RK7Reference не пишутся, маска (см. PropMask) задаётся для свойств элемента (а не коллекции!)
    @RefItemGUID: string  - Идентификатор элемента (если надо запросить один элемент), если задан, то атрибуты тэга RK7Reference не пишутся, маска (см. PropMask) задаётся для свойств элемента (а не коллекции!)
    @RefBlobName: string  - Имя BLOB (поля), если не задано - берётся первое
    @EncodeBase64: boolean (по умолчанию "1")  - Нужно ли кодировать Base64
    @UnpackedBlob: boolean (по умолчанию "0")  - Нужно ли распаковать LZ
  <RK7Command>+ [GetItemBlob] (структура - см. выше)
  <RK7Command2>+ [GetItemBlob] (структура - см. выше)
```

## Пример: GetItemBlob

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetItemBlob" RefName="IMAGELIST" RefItemIdent="{{refItemId}}" EncodeBase64="1"/>
</RK7Query>
```
