# FarCardsAnyInfoRaw

Выполнение запроса AnyInfo на сервере FarCards

Схемы: `schemas/qryFarCardsAnyInfoRaw.xsd`, `schemas/resFarCardsAnyInfoRaw.xsd`
Влияние: только чтение

## Практика

- Ответ - <RawData> в Base64; без обработчика на стороне FarCards приходит пустой.
- По сути запрос на запись: так передают в FarCards произвольные данные о продаже (как настройка PDS-интерфейса "Всегда передавать данные продаж").

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
(одно из:)
  <RK7CMD> [FarCardsAnyInfoRaw]
    <Interface> [refItem]  - Логический интерфейс, по которому бедет найден сервер Farcards, на котором надо будет выполнить AnyInfo
    <ExtCardProperties>? [extCardProperties]  - Список запрашиваемых свойств
      <Property>+ [extCardProperty]
        @name!: normalizedString
        @value: normalizedString
    <RawData>
      (текстовое содержимое: base64Binary)
    @CMD: string = "FarCardsAnyInfoRaw"
  <RK7Command>+ [FarCardsAnyInfoRaw] (структура - см. выше)
  <RK7Command2>+ [FarCardsAnyInfoRaw] (структура - см. выше)
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<ExtCardProperties>? [extCardProperties]  - Список возвращенных расширенных свойств
  <Property>+ [extCardProperty]
    @name!: normalizedString
    @value: normalizedString
<RawData>
  (текстовое содержимое: base64Binary)
```

## Пример: FarCardsAnyInfoRaw

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="FarCardsAnyInfoRaw">
    <Interface id="{{pdsInterfaceId}}"/>
    <RawData>VGVzdA==</RawData>
  </RK7CMD>
</RK7Query>
```
