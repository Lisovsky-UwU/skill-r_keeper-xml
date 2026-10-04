# Справочники (RefName)

Справочники читаются командой `GetRefData` (или `GetRefDataFiltered` - с учетом станции, официанта,
стола). Полный список с количеством элементов на конкретном сервере - `GetRefList`. Имена
регистронезависимы: в XSD они в CamelCase (`MenuItems`), сервер отдает их ПРОПИСНЫМИ (`MENUITEMS`).

Чтобы не тянуть справочник целиком, ограничивайте свойства и берите только активные элементы:

```xml
<RK7CMD CMD="GetRefData" RefName="EMPLOYEES" OnlyActive="1" PropMask="items.(Ident,Code,Name,GUIDString)"/>
```

`PropMask="*"` у одного элемента (`RefItemIdent="..."`) показывает все его свойства - так удобно
выяснять флаги (например, у причин удаления).

## Какой справочник стоит за элементом запроса

| Элемент запроса | Справочник | Примечание |
|---|---|---|
| Restaurant | RESTAURANTS | |
| Station, LockStation | CASHES | у станции есть NetName |
| Waiter, Cashier, Manager, Employee, Creator, Author | EMPLOYEES | права - `GetEmployeeInfo2` |
| Table, ExtraTables/Item | TABLES | |
| OrderCategory | UNCHANGEABLEORDERTYPES | "категория заказа": Основная, Доставка... |
| OrderType | CHANGEABLEORDERTYPES | "тип заказа" |
| GuestType | GUESTTYPES | |
| Dish, Dishes/Item | MENUITEMS | цены на станции - `GetOrderMenu` |
| Modi | MODIFIERS | группы - MODIGROUPS, схемы - MODISCHEMES |
| Combo, Component | MENUITEMS | |
| Discount | DISCOUNTS | |
| Currency, Pay, Payment, Prepay | CURRENCIES | |
| DeleteReason, Reason (удаление, возврат, стоп-лист) | ORDERVOIDS | нужен флаг под операцию, см. protocol.md, раздел 8 |
| Reason (внесение/изъятие денег) | DEPOSITCOLLECTREASONS | |
| Interface, Device, Drawer | DEVICES | логические устройства и интерфейсы |
| Course | зависит от версии - найдите по `GetRefList` | порядок подачи |
| Operation | OPERATIONS | |
| Document | DOCUMENTS | типы документов: 2 пречек, 27 копия чека, отчеты |
| Maket, Layout, ReceiptMaket, InvoiceMaket | MAKETS | |
| Purpose | PRINTERPURPOSES | назначения печати |
| Position | SERVINGPOSITIONS | |
| PriceScale | PRICETYPES | |
| Image | IMAGELIST | |

## Еще полезные справочники

| RefName | Что внутри |
|---|---|
| CATEGLIST | классификационные категории блюд (не путать с категорией заказа) |
| HALLPLANS | планы залов |
| PARAMETERS | параметры (значение с учетом исключений - `GetParamValue`) |
| PRICES | цены |
| TAXES, TAXRATES | налоги |
| CASHGROUPS | кассовые серверы |
| ROLES, PRIVILEGES | роли и привилегии работников |
| SCRIPTS | скрипты |
| CLASSINFOS | подтипы элементов (ItemKind для SetRefData) |
