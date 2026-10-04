# GetRefData

Получить коллекцию

Схемы: `schemas/qryGetRefData.xsd` (схемы ответа нет)
Влияние: только чтение

## Практика

- PropMask ограничивает свойства: items.(Ident,Code,Name,GUIDString). Без него ответ по большим справочникам огромный.
- OnlyActive="1" - только активные элементы; IgnoreEnums="1" - перечисления числами.
- Фильтр <PROPFILTERS><PROPFILTER Name=... Value=... | Substring=.../></PROPFILTERS>.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
(одно из:)
  <RK7CMD> [GetRefDataCommand]
    <PROPFILTERS>?  - Список фильтров
      <PROPFILTER>+
        @Name!: normalizedString  - Имя свойства для фильтрации. Небходимо если нет подфильтров
        @Value!: normalizedString  - Значение свойства для фильтрации. Небходимо если нет подфильтров и Substring
        @Substring!: normalizedString  - Часть значения свойства для фильтрации. Необходимо если нет подфильтров и Value
        @Masked: integer  - Использовать RegExp выражения для фильтрации. Используется с Value. Принимает значеня 0 и 1, по умолчанию 0
        @Kind: string  - Вид связи подфильтров. Используется если есть подфильтры. Принимает значения AND и OR, по умолчанию OR
    @CMD!: string = "GetRefData"
    @RefName!: refName {120 значений, см. XSD}  - Название коллекции
    @RefItemIdent: integer  - Идентификатор элемента (если надо запросить один элемент), если задан, то атрибуты тэга RK7Reference не пишутся, маска (см. PropMask) задаётся для свойств элемента (а не коллекции!)
    @RefItemGUID: string  - Идентификатор элемента (если надо запросить один элемент), если задан, то атрибуты тэга RK7Reference не пишутся, маска (см. PropMask) задаётся для свойств элемента (а не коллекции!)
    @PropMask: string  - Маска свойств. При заполненном RefItemIdent или RefItemGUID относится к элементу, иначе к коллекции Можно запросить ограниченный список свойств. * - все свойства, пусто - ничего. Для вложенных объектов необходимо указывать полный путь к свойству, либо использовать круглые скобки для общего префикса…
    @WithMacroProp: boolean (по умолчанию "0")  - Нужно ли добавлять генерируемые свойства
    @MacroPropExtra: boolean (по умолчанию "0")  - Нужно ли добавлять ДОПОЛНИТЕЛЬНЫЕ генерируемые (расширенные) свойства которые не являются обычной частью элемента, а как правило относятся к одному из других св-в.
    @WithBlobsData: boolean (по умолчанию "0")  - Нужно ли добавлять BLOB поля, будут добавлены подтэгами в кодировке Base64
    @UnpackedBlob: boolean (по умолчанию "0")  - Возвращать BLOB-данные в распакованном виде (без LZ-сжатия)
    @MacroPropTags: boolean (по умолчанию "0")  - если 1, то добавлять генерируемые свойства подтэгами PropXXX, где XXX общая часть имени подсвойства (до ^)
    @WithChildItems: WithChildItemType {0 | 1 | 2 | 3} (по умолчанию "0")  - 0 - без дочерних элементов, 1 - только иерархия внутри справочника в разделе RIChildItems коллекции, 2 - дети в разделе items только из других справочников, 3 - и иерархия внутри справочника и дети из других справочников в разделе RIChildItems коллекции. Добавляется псевдосвойство RIChildItems, мож…
    @IgnoreEnums: boolean (по умолчанию "0")  - если 0 - перечисляемые типы как строки, 1 - перечисляемые типы и их множества как числа
    @IgnoreDefaults: boolean (по умолчанию "0")  - если 1 - не писать атрибуты, если значения свойств "по умолчанию"
    @OnlyActive: boolean (по умолчанию "0")  - если 1 - то будут возвращены только активные записи, иначе все записи"
    @LinkNames: boolean (по умолчанию "0")  - если 1 - то дополнительно будут возвращены имена элементов для всех ссылочных свойств. Например, если у элемента есть свойство RightLvl (идентификатор права доступа), то в ответ будет добавлено также свойство RightLvlName (наименование этого права доступа), и так для всех свойств, которые содержат …
    @Offset: integer (по умолчанию "0")  - Paging. Смещение возвращаемого окна от начала. По умолчанию 0 - вернуть с первого элемента (с начала). Если значение больше или равно количеству элементов, то вернётся пустой список
    @ItemCount: integer (по умолчанию "0")  - Paging. Количество элементов, которое надо вернуть. По умолчанию 0 - вернуть всё
    @MaxRunMs: integer (по умолчанию "0")  - Примерное максимальное время в миллисекундах на выполнение запроса. Половина от этого времени используется на запись в бинарный стрим, потом происходит конверсия в XML, которая занимает примерно такое же время. Как только время исчерпано вывод прекращается и возвращается то количество элементов, ко…
  <RK7Command>+ [GetRefDataCommand] (структура - см. выше)
  <RK7Command2>+ [GetRefDataCommand] (структура - см. выше)
```

## Пример: GetRefData - Сотрудники

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetRefData" RefName="EMPLOYEES" OnlyActive="1" PropMask="items.(Ident,Code,Name,GUIDString,MainParentIdent)"/>
</RK7Query>
```

## Пример: GetRefData - Меню

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetRefData" RefName="MENUITEMS" OnlyActive="1" PropMask="items.(Ident,Code,Name,GUIDString,CategPath,Status)"/>
</RK7Query>
```

## Пример: GetRefData - Столы

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetRefData" RefName="TABLES" OnlyActive="1" PropMask="items.(Ident,Code,Name,GUIDString)"/>
</RK7Query>
```

## Пример: GetRefData - Валюты

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetRefData" RefName="CURRENCIES" OnlyActive="1" PropMask="items.(Ident,Code,Name,GUIDString)"/>
</RK7Query>
```

## Пример: GetRefData - Станции

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetRefData" RefName="CASHES" OnlyActive="1" PropMask="items.(Ident,Code,Name,GUIDString,NetName)"/>
</RK7Query>
```

## Пример: GetRefData - Один элемент

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetRefData" RefName="MENUITEMS" RefItemIdent="{{dishId}}" PropMask="*"/>
</RK7Query>
```

## Пример: GetRefData - С фильтром

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetRefData" RefName="MENUITEMS" OnlyActive="1" PropMask="items.(Ident,Code,Name)">
    <PROPFILTERS>
      <PROPFILTER Name="Name" Substring="Салат"/>
    </PROPFILTERS>
  </RK7CMD>
</RK7Query>
```
