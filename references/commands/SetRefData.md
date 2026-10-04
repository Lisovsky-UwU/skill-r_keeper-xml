# SetRefData

Записать элементы коллекции

Схемы: `schemas/qrySetRefData.xsd` (схемы ответа нет)
Влияние: **опасно** - необратимые или массовые изменения, блокировка кассы

## Практика

- Команда справочного сервера (RK7 Manager): кассовый сервер отвечает "Unknown command SetRefData". У RK7Query там задаются UserID/UserGUID/UserPass.
- Логика записи - вставка или обновление; ключ - GUIDString. Не заполненные атрибуты не меняются; чтобы очистить значение, передайте "".
- Родитель (группа) - MainParentIdent: GUID родителя, который уже существует или идет в этом же запросе раньше.
- Физически ничего не удаляется: удаление - Status="rsDeleted" (rsActive - активен, rsInactive - недоступен). Есть и <ItemsToDelete>.
- Цена блюда - PRICETYPES-0 (в копейках, тип цены 0 - по умолчанию), категория - CLASSIFICATORGROUPS-0 (GUID), налог - TaxDishType. Полный список свойств - чтение справочника через GetRefData.
- Ответ: <RK7QueryResult Status="Ok"><CommandResult CMD="SetRefData" Status="Ok" ErrorText=""/></RK7QueryResult>.

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
  @UnpackedBlob: boolean (по умолчанию "0")  - Передаются ли BLOB-данные в распакованном виде (LZ не применяется)
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

## Пример: Группы меню (из документации UCS, на кассовом сервере не выполняется)

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7Command CMD="SetRefData" RefName="CATEGLIST">
    <Items>
      <Item GUIDString="{{groupGuid}}" Code="20" Name="Кухня" AltName="" Status="rsActive" ExtCode="12"/>
      <Item GUIDString="{{subgroupGuid}}" MainParentIdent="{{groupGuid}}" Code="13" Name="Вторые блюда" AltName="" Status="rsActive" ExtCode="14"/>
    </Items>
  </RK7Command>
</RK7Query>
```

## Пример: Блюда (из документации UCS, на кассовом сервере не выполняется)

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7Command CMD="SetRefData" RefName="MenuItems">
    <Items>
      <Item GUIDString="{{newGuid}}" MainParentIdent="{{subgroupGuid}}" Code="33" Name="Рыба" AltName="" Status="rsActive" TaxDishType="1" ExtCode="33" PRICETYPES-0="5000"/>
    </Items>
  </RK7Command>
</RK7Query>
```
