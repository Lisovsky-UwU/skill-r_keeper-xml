# SetRefData

Записать элементы коллекции

Схемы: `schemas/qrySetRefData.xsd` (схемы ответа нет)
Влияние: **опасно** - необратимые или массовые изменения, блокировка кассы

## Практика

- Команда справочного сервера (RK7 Manager): кассовый сервер отвечает "Unknown command SetRefData". У RK7Query там задаются UserID/UserGUID/UserPass.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7Command>  - Записать элементы коллекции
  <Items> [referentItems]  - Referent items
    <Item>? [referentItem]  - Элемент справочника (идентификатор элемента)
      @Ident: nonNegativeInteger
      @GUIDString: normalizedString
      @* - допускаются любые другие атрибуты
  <ItemsToDelete>? [referentItems]  - Items to delete (структура - см. выше)
  <MovePriorityItem>?  - Move first Item before second or to the end
    <Item> [referentItem] (структура - см. выше)
    @BeforeIdent: nonNegativeInteger
    @BeforeGUIDString: normalizedString
  @CMD!: string = "SetRefData"
  @RefName!: refName {115 значений, см. XSD}  - Название коллекции
  @ItemKind: int (по умолчанию "0")  - ID подтипа (идентификатор из справочника ClassInfos)
@UserGUID: guidString (по умолчанию "{D8476175-30F4-415A-97BB-68043A26FA82}")  - GUID пользователя
@UserID: integer (по умолчанию "9006")  - Идентификатор пользователя
@UserPass: normalizedString (по умолчанию "")  - Пароль пользователя
```

## Пример: SetRefData

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7Command CMD="SetRefData" RefName="TABLES">
    <Items>
      <Item Ident="{{tableId}}" Name="4"/>
    </Items>
  </RK7Command>
</RK7Query>
```
