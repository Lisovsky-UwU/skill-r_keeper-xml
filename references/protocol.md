# Протокол XML-интерфейса r_keeper 7

## Содержание
1. Транспорт
2. Запрос
3. Ответ и ошибки
4. Ссылки на объекты
5. Единицы и форматы
6. Кто выполняет команду
7. Блокировки, лицензии, версии
8. Чего ждать от сервера
9. Плейсхолдеры в примерах

## 1. Транспорт

- `POST https://<host>:<port>/rk7api/v0/xmlinterface.xml`, тело - XML в UTF-8, `Content-Type: application/xml`
  (подходит и `text/plain`). С `application/x-www-form-urlencoded` - а его ставит, например, `curl -d`
  без заголовка - сервер не видит тело и отвечает `Query Parse Error` "Empty input XML".
- Кодировка - UTF-8. Старые примеры UCS объявляют `encoding="windows-1251"`: они писались для
  библиотеки RK7XML.dll (функции CallRK7XMLRPC*, SetCryptKey), а по HTTP запрос в windows-1251 ломает
  кириллицу - сервер падает с невнятной ошибкой вроде "Sort collection ... Required value is null".
- Авторизация HTTP Basic; логин и пароль выдает администратор r_keeper.
- Сертификат у кассового сервера обычно самоподписанный, часто со слабым ключом (RSA 1024) и иногда
  со старыми версиями TLS, поэтому клиенту нужно отключать проверку сертификата. Многие серверы
  при этом умеют TLS 1.2/1.3 - проверяйте, прежде чем считать, что нужен TLS 1.0.
- HTTP-статус почти всегда 200, даже при ошибке: результат смотрят в атрибуте `Status` ответа.

## 2. Запрос

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetOrder">
    <Order guid="{...}"/>
  </RK7CMD>
</RK7Query>
```

- Имя команды - атрибут `CMD` элемента `RK7CMD`; параметры - его атрибуты и вложенные элементы.
- Часть схем допускает вместо одного `RK7CMD` последовательность `RK7Command` / `RK7Command2`
  (несколько команд в одном запросе); `SetRefData` записывается через `RK7Command`.
- XML-комментарии в теле допустимы - сервер их игнорирует.

## 3. Ответ и ошибки

```xml
<RK7QueryResult ServerVersion="7.26.8.2001" XmlVersion="248" NetName="MIDSERVER" Status="Ok"
    CMD="GetOrder" ErrorText="" DateTime="..." WorkTime="16" Processed="1" ArrivalDateTime="...">
  ...данные команды...
</RK7QueryResult>
```

| Атрибут | Смысл |
|---|---|
| `Status` | `Ok`, `No changes` (сработал кэш по `lastversion`), `Execution Started`, `Query Parse Error` (сломан XML), `Bad Query Parameters` (в т.ч. `Unknown command`), `Query Executing Error` (бизнес-ошибка), `Result Writing Error` |
| `ErrorText`, `RK7ErrorN` | текст и код ошибки; подробности - в `<Errors><Error RK7ErrorN="...">` |
| `NetName` | кто реально выполнил запрос: кассовый сервер или станция, куда он переслал команду |
| `WorkTime` | время выполнения на сервере, мс |
| `ServerVersion`, `XmlVersion` | версия r_keeper и протокола |

Типичные тексты:
- `Error: child element "X" not found` / `Attribute ".../@x" is not found` - не хватает обязательного
  элемента или атрибута (сервер иногда требует то, что в XSD помечено необязательным).
- `Не найден элемент N в коллекции Employees` - ссылка на несуществующий объект справочника.
- `Unknown command X` - этот узел команду не выполняет (см. раздел 6).
- `Не получается заблокировать. Заказ заблокирован другим ключом блокировки` - см. раздел 7.

## 4. Ссылки на объекты

**Элемент справочника (`refItem`)** - любой из атрибутов: `id` (Ident), `code` или `guid`.
По имени объекты не ищутся. В ответах те же элементы приходят с `id`, `code`, `name`, `guid`.

```xml
<Station id="15004"/>   <Waiter code="34"/>   <Currency guid="{16D72549-...}"/>
```

**Заказ (`orderElement`)** - `guid`, либо пара `visit` + `orderIdent`:

```xml
<Order guid="{2CB7FB2C-...}"/>
<Order visit="640419540" orderIdent="256"/>
```

**Строки заказа** (пакеты, блюда, скидки, оплаты, чеки) идентифицируются `uni` (номер в заказе) и
`line_guid`. Их берут из ответа `GetOrder` и передают в TransferDishes, MakeReturnGoods,
KDSSetDishData, TerminalAuthPay2, DeleteReceiptPayments и т.д.

Какой справочник стоит за каким элементом - `references/refnames.md`.

## 5. Единицы и форматы

| Что | Формат |
|---|---|
| Количество (`quantity`) | в тысячных: `1000` = 1 шт, `500` = 0,5 |
| Деньги (`price`, `amount`, `...Sum`) | в копейках: `40000` = 400,00 |
| Дата-время | `2026-10-03T16:05:00`, локальное время сервера, без часового пояса |
| Время-интервал (`lockTime`) | `чч:мм:сс` |
| Логические | только `1`/`0`: на `true`/`false` часть атрибутов дает `Bad integer attribute ... value: "true"` |
| GUID | в фигурных скобках, верхний регистр: `{8C9E446E-3A3F-4A4F-938E-69941B784AF2}` |

Состояния строк (`state`): 1 открыт, 3 зафиксирован, 4 распечатан, 5 частично закрыт, 6 закрыт, 7 удален.
Статус авторизации оплаты (`TransactionStatus`): 1 не выполнена, 3 в процессе, 4 успешна, 5 подтверждена, 6 аннулирована.
КДС-статус (`kdsstate`): sent, started, ready, taken, collect, collected, startpark, endpark, removed.

## 6. Кто выполняет команду

В описании команды в XSD стоит пометка: `[Кассовый сервер]`, `[Касса]` или обе.

- **Кассовый сервер** - основной адресат; запрос идет на его адрес.
- Часть команд сервер сам пересылает на станцию (LogicalDevices, ListDeviceMenu, DeliveryEditOrder,
  печать): в ответе `NetName` будет именем станции. Станция должна быть запущена и в сети.
- `SetRefData` - команда справочного сервера (RK7 Manager); кассовый сервер отвечает
  `Unknown command`. Читать справочники (`GetRefData`) можно и с кассового сервера.
- Список того, что реально поддерживает конкретный узел, - `GetFunctions` (там же пометка `deprecated="1"`).
  Но и он не исчерпывающий: ReloadWorkUdb сервер 7.26.8 не объявляет, а выполняет.
- Схемы и сервер расходятся в обе стороны:
  - схема есть, а сервер 7.26 команду не знает (`Unknown command`): GotoOrder, PostMessage, PerformMessage
    (по наблюдениям интеграторов, убраны в 7.5.8), ApplyMCR, WaitWindow; SetRefData - только справочный сервер;
  - UCS убрала схему из актуального набора, а сервер команду выполняет: CheckLicense, ReloadWorkUdb
    (их схемы сохранены из предыдущего набора в `schemas/Hidden/`);
  - команда есть, а схемы нет: GetSystemInfo и GetBatchOfGoodsList (для них страницы собраны из
    проверки на сервере), а также GetOrders, FindEmployee, AddReservation / DelReservation /
    GetReservationResults, GetRefItemBlob, KDSGetRefsData, KDSGetSystemInfo, KDSSetDishFlag, PrintRawData,
    SetDishRate, WriteGtinToMenuItem, WriteOperationToLog, CheckEgaisMark, DeleteBottle и другие -
    по ним справочника нет, пробуйте на стенде.
- Имена команд чувствительны к регистру (`getsysteminfo` - `Unknown command`). Исключение -
  CreaterkFriendsAnchor: сервер принимает и CreateRkFriendsAnchor.

## 7. Блокировки, лицензии, версии

- **lockguid.** `LockOrder` блокирует заказ на `lockTime` с токеном `lockguid` (произвольный GUID
  клиента). Пока блокировка действует, изменяющие запросы должны передавать тот же `lockguid`
  (атрибут есть у SaveOrder, PayOrder, UpdateOrder, VoidOrder и многих других). Заказ, открытый на
  кассе (или через DeliveryEditOrder), заблокирован ключом станции - его отпускают на кассе.
- **Лицензии.** SaveOrder требует лицензию XML SaveOrder (`CheckLicense license="XMLSaveOrder"`).
  Элемент `LicenseInfo` (anchor, licenseToken, LicenseInstance guid/seqNumber) нужен в SaaS-схеме
  лицензирования UCS; без настоящих значений сервер отвечает `Bad license anchor`.
- **Версии.** Справочник собран из XSD UCS для r_keeper 7.26 (файлы 2023-2026 годов). Сервер другой
  версии может знать иной набор команд - сверяйтесь с `GetFunctions`.
- **Смена.** Если общая смена открыта слишком давно, новые заказы не создаются (RK7ErrorN 2133), а
  пока смена закрывается, любые запросы получают "UCSERR(2172): В данный момент закрывается общая смена".

## 8. Чего ждать от сервера

- **Проверка нестрогая.** Неизвестные элементы и атрибуты часто молча игнорируются: `Status="Ok"` не
  доказывает, что разметка правильная (PrintDataXML отвечает Ok на выдуманный тег). Сверяйтесь с XSD.
- **И наоборот:** иногда сервер требует то, что в XSD необязательно (expireTime у WaiterMessage,
  LicenseInfo у GetXMLLicenseInstanceSeqNumber, readyTime и Table у DeliveryEditOrder).
- **Ошибки в самих XSD.** В наборе UCS встречаются невалидные места: в `qryAddBatchOfGoods.xsd`
  атрибуты записаны без complexType, тип `resLoyaltyInfo` в `common.xsd` описан не по правилам XSD.
  Генератор такие места переживает, но в спорных случаях проверяйте на стенде.
- **Регистр элементов ответа.** С 7.26 статусы КДС у блюд приходят как `<KdsState name at>` (не
  `KDSState`); XML чувствителен к регистру, разборщик ответа должен это учитывать.
- **Причины удаления с флагами.** Справочник ORDERVOIDS один на все случаи, но каждая операция
  принимает только причину с нужным флагом: удаление чека (ImplOnCheckVoid), аннулирование
  (ImplOnCheckUndo), возврат блюд (ImplOnDishReturn), стоп-лист (ImplOnAddDishInStopList), отмена
  пречека (ImplOnBillCancel), удаление предоплаты (ImplOnPrepayDeletion). Флаги видны через
  `GetRefData RefName="ORDERVOIDS" PropMask="*"`.
- **Окна на кассе.** OpenWebForm и DeliveryEditOrder открывают окно на станции и не отвечают, пока
  его не закроют; HTTP-соединение обычно рвется по таймауту около 60 с.
- **Параметры ресторана** могут запрещать операции (например, PrintBill при включенном
  "Печатать пречек с чеком намерения") - текст ошибки называет параметр.

## 9. Плейсхолдеры в примерах

Примеры в `commands/*.md` проверены на живом сервере (r_keeper 7.26); конкретные значения заменены на `{{имя}}`.
`scripts/rk7.py --var имя=значение` подставляет их при отправке.

| Плейсхолдер | Что подставить | Где взять |
|---|---|---|
| `restaurantId` | ресторан | RESTAURANTS, или `GetSystemInfo` |
| `stationId`, `stationNetName` | кассовая станция и ее сетевое имя | CASHES (Ident, NetName) |
| `waiterId`, `cashierId`, `managerId` | работники с нужными правами | EMPLOYEES |
| `managerPassword` | пароль менеджера | у администратора |
| `tableId`, `tableId2`, `deliveryTableId` | столы | TABLES |
| `orderCategoryId`, `deliveryCategoryId` | категория заказа (Основная / Доставка) | UNCHANGEABLEORDERTYPES |
| `orderTypeId` | тип заказа | CHANGEABLEORDERTYPES |
| `guestTypeId` | тип гостей | GUESTTYPES |
| `dishId`, `dishPrice` | блюдо и его цена в копейках | MENUITEMS, цены - `GetOrderMenu` |
| `discountId` | скидка | DISCOUNTS |
| `currencyId`, `cardCurrencyId` | валюта (наличные / банковская карта) | CURRENCIES |
| `deleteReasonId`, `checkDeleteReasonId`, `checkUndoReasonId`, `returnReasonId` | причины с нужными флагами (раздел 8) | ORDERVOIDS |
| `depositReasonId` | причина внесения/изъятия | DEPOSITCOLLECTREASONS |
| `pdsInterfaceId` | интерфейс к карточной системе (FarCards) | DEVICES |
| `deviceId` | логическое устройство | DEVICES, `LogicalDevices` |
| `operationId` | операция | OPERATIONS |
| `printPurposeId` | назначение печати | PRINTERPURPOSES |
| `refItemId` | элемент справочника | `GetRefData` |
| `cardCode` | номер карты гостя | карточная система |
| `orderGuid`, `visitId`, `orderIdent`, `orderGuid2` | заказы | ответ `CreateOrder` / `GetOrderList` |
| `sessionUni`, `dishLineGuid`, `prepayLineGuid` | строки заказа | ответ `GetOrder` / TerminalAuthStart2 |
| `orderSum` | сумма к оплате заказа, копейки | `unpaidSum` из `CalcOrder2` |
| `receiptNum`, `printCheckGuid` | номер и GUID чека | ответ `PayOrder` / `GetReceiptList` |
| `lockGuid`, `deliveryGuid`, `licenseInstanceGuid` | GUID, придуманные клиентом | сгенерировать новый |
| `newGuid`, `groupGuid`, `subgroupGuid` | GUID новых элементов справочника и их групп (SetRefData) | сгенерировать новый |
| `modifierId`, `modifierId2` | модификаторы | MODIFIERS |
| `employeeId`, `cryptedPassword` | работник и его зашифрованный пароль | EMPLOYEES; `scripts/rk7.py --crypt-password` |
| `markingData`, `gtin` | марка (DataMatrix) в base64 и GTIN товара | сканер марок; GTIN - `ParseMarkingData` |
| `tariffTableId`, `tariffDetailId` | тарифицируемый стол и тип тарификации | TABLES (стол-устройство), типы тарификации |
| `sbpPayGuid` | идентификатор СБП-платежа | задан при оплате через PayOrder / IntentPayOrder |
| `loyaltyPhone` | телефон участника лояльности r_k Friends | от гостя |
| `maxSessionId` | сессия проверки возраста | QR-код в мессенджере MAX |
| `readyTime` | время готовности доставки | не позже ~суток от текущего времени сервера |
