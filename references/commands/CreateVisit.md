# CreateVisit

Схемы: `schemas/qryCreateVisit.xsd`, `schemas/resCreateVisit.xsd`
Влияние: изменяет данные

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>  - Создать визит
  <GuestType>? [refItem]  - Тип гостей
  <Guests>? [Guests_Item]  - Список гостей
    <Guest>* [guest_item]
      <Interface>? [refItem]  - Интерфейс к карте гостя
      @guestLabel!: token  - Текстовая метка гостя
      @cardCode: normalizedString  - Код карты гостя
      @clientID: long  - ID адреса гостя
      @addressID: long  - ID адреса гостя
    @count: int  - Количество гостей
  @CMD: string = "CreateVisit"
  @guid: normalizedString  - GUID визита. Если не задан, то будет сгенерирован новый guid
  @persistentComment: normalizedString  - Сохраняемый комментарий
  @nonPersistentComment: normalizedString  - Несохраняемый комментарий
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
@VisitID!: positiveInteger  - ID созданного визита
@guid!: normalizedString  - GUID визита
```

## Пример: CreateVisit

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="CreateVisit" persistentComment="example">
    <GuestType id="{{guestTypeId}}"/>
    <Guests count="2"/>
  </RK7CMD>
</RK7Query>
```
