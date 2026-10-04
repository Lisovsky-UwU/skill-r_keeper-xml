# FarCardsAnyInfoXML

Выполнение запроса AnyInfo на сервере FarCards

Схемы: `schemas/qryFarCardsAnyInfoXML.xsd`, `schemas/resFarCardsAnyInfoXML.xsd`
Влияние: только чтение

## Практика

- Содержимое XMLData передается в FarCards как есть; что вернется, определяет расширение карточной системы - без обработчика ответ Ok без данных.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
(одно из:)
  <RK7CMD> [FarCardsAnyInfoXML]
    <Interface> [refItem]  - Логический интерфейс, по которому бедет найден сервер Farcards, на котором надо будет выполнить AnyInfo
    <ExtCardProperties>? [extCardProperties]  - Список запрашиваемых свойств
      <Property>+ [extCardProperty]
        @name!: normalizedString
        @value: normalizedString
    <XMLData>
    @CMD: string = "FarCardsAnyInfoXML"
  <RK7Command>+ [FarCardsAnyInfoXML] (структура - см. выше)
  <RK7Command2>+ [FarCardsAnyInfoXML] (структура - см. выше)
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<ExtCardProperties>? [extCardProperties]  - Список возвращенных расширенных свойств
  <Property>+ [extCardProperty]
    @name!: normalizedString
    @value: normalizedString
<XMLData>  - xml, переданный из farcards. Имя тэга и его состав может быть любым
```

## Пример: FarCardsAnyInfoXML

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="FarCardsAnyInfoXML">
    <Interface id="{{pdsInterfaceId}}"/>
    <XMLData>
      <Request Card="{{cardCode}}"/>
    </XMLData>
  </RK7CMD>
</RK7Query>
```
