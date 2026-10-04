# Типовые сценарии

Последовательности команд, проверенные на живом сервере. Стрелка `->` показывает, какое значение
из ответа идет в следующий запрос. Полные схемы и примеры - в `commands/<CMD>.md`.

## Содержание
1. Знакомство с сервером
2. Жизненный цикл заказа в зале
3. Расчет без создания заказа
4. Предоплата и банковский терминал
5. Отмена, возврат, удаление
6. Блокировка и перенос блюд
7. Доставка
8. Стоп-лист
9. Касса, смены, печать
10. Сообщения, КДС, опрос изменений

## 1. Знакомство с сервером

Пароль работника проверяет `CheckPassword` (пароль шифруется - `scripts/rk7.py --crypt-password`).

1. `GetSystemInfo` / `GetSystemInfo2` - версия, ресторан, текущая общая смена.
2. `GetFunctions` - какие команды этот узел поддерживает.
3. `GetRefData` по CASHES, EMPLOYEES, TABLES, CURRENCIES, UNCHANGEABLEORDERTYPES - идентификаторы
   для запросов (с `PropMask` и `OnlyActive="1"`).
4. `GetOrderMenu` со `<Station>` - доступные на станции блюда и цены.
5. `CheckLicense license="XMLSaveOrder"` - можно ли сохранять заказы по XML.
6. `GetEmployeeInfo2` - хватит ли прав у работника, от имени которого пойдут операции.

## 2. Жизненный цикл заказа в зале

1. `CreateOrder` (Table обязателен) -> `guid`, `visit`, `orderIdent` нового заказа.
2. `SaveOrder` с `<Session>` и блюдами (`quantity` в тысячных) - добавить пакет. Скидки, модификаторы,
   предоплаты - тоже через SaveOrder.
3. `GetOrder` -> `uni` пакетов, `line_guid` блюд, суммы (`orderSum`, `unpaidSum`).
4. При необходимости `UpdateOrder` (официант, гости, комментарии, внешние свойства), `ChangeSessionCourse`.
5. `CalcOrder2` -> `unpaidSum`, который реально нужно оплатить (учитывает обещанные предоплаты;
   `unpaidSum` из GetOrder их не учитывает).
6. Необязательно: `PrintBill` (пречек), `UndoBill` (отмена пречека).
7. `PayOrder` с `<Payment id="валюта" amount="unpaidSum"/>` -> `<PrintCheck CheckNum line_guid>`;
   заказ закрыт, чек напечатан на станции.
8. `CloseVisit`, если визит больше не нужен.

Чек намерения (с 7.25.04, режим "Печатать пречек с чеком намерения"): вместо PrintBill + PayOrder
сначала `IntentPayOrder` с платежами - он печатает пречек и создает чек намерения (платеж становится
обещанным, unpaidSum = 0). Отмена - `CorrectIntentReceipt` (заказ снова не оплачен). Расчет с учетом
двух фискальных регистраторов - `CalcOrder5`, виртуальный расчет с добавленными пакетами - `CalcOrder4`.

## 3. Расчет без создания заказа

- `CalcOrder` - стол, категория, тип, официант и пакеты с блюдами; вернет суммы, ничего не сохраняя.
- `ValidateOrder` - проверить, что блюда можно продать (по существующему заказу или столу).
- `GetOrderMenu2` - цены только по нужным блюдам.

## 4. Предоплата и банковский терминал

- Предоплата валютой: `SaveOrder` с `<Session><Prepay id="валюта" amount="..."/></Session>`.
- Терминал, версия 2 (предпочтительно):
  1. `TerminalAuthStart2` с `<Prepay id="валюта-карта" amount="..."/>` -> `line_guid` предоплаты
     (атрибут корня ответа).
  2. Внешний терминал проводит оплату.
  3. `TerminalAuthPay2` (успех) или `TerminalAuthError2` (отказ) с этим `line_guid`.
- Версия 1: `TerminalAuthStart` (создает обещанную предоплату) -> `TerminalAuthPay` / `TerminalAuthError`.

## 5. Отмена, возврат, удаление

| Задача | Команда | Нюанс |
|---|---|---|
| Удалить неоплаченный заказ | `VoidOrder` | причина из ORDERVOIDS |
| Вернуть оплаченный заказ в редактирование | `UndoReceipt` ReceiptNum=CheckNum | причина с флагом ImplOnCheckUndo; нельзя, если были возвраты |
| Удалить чек вместе с заказом | `DeleteReceipt` | причина с флагом ImplOnCheckVoid |
| Вернуть часть блюд по чеку | `MakeReturnGoods` | PrintCheck line_guid + блюда line_guid/quantity; создает чек возврата |
| Найти чек для возврата | `FindReceiptsForReturn` | задавайте узкие фильтры, иначе медленно |
| Убрать оплаты из ошибочного чека | `DeleteReceiptPayments` | |

## 6. Блокировка и перенос блюд

- `LockOrder lockTime="00:01:00" lockguid="{свой GUID}"` - дальше изменяющие запросы передают тот же
  `lockguid`. Без него во время блокировки - "заблокирован другим ключом блокировки".
- `TransferDishes`: `OrderSource`, `OrderDest`, блюда по `line_guid` из GetOrder исходного заказа,
  `quantity` - для частичного переноса.

## 7. Доставка

1. `DeliveryPostOrder` с GUID заказа, сгенерированным клиентом, категорией "Доставка", `ExtSource`,
   `DeliveryBlock`, пакетами и `HolderXML` (минимум `<holder><Holders_Addresses/></holder>`).
   Повторная отправка с тем же GUID перезаписывает заказ.
2. Дальше по тому же GUID: `DeliveryUpdateStatus` (статус в `DeliveryBlock deliveryState`),
   `DeliverySetForwarder` (экспедитор), `DeliveryServPrint` (сервис-печать), `DeliveryPrintInvoice`
   (накладная), `DeliveryPayOrders` (чек или пречек при отправке экспедитора).
3. Редактирование: `DeliveryEditOrder` открывает редактор на кассе и блокирует заказ до закрытия
   окна; завершение - `DeliveryConfirmEdit` (readyTime не позже ~суток) или `DeliveryCancelEdit`.
4. `DeliveryGetOrderList` - список заказов доставки, `DeliveryVoidOrder` - удалить.

## 8. Стоп-лист и маркировка

- `GetDishRests` / `GetDishRest` - текущие остатки.
- `SetDishRests` - остаток (`quantity` в тысячных) или запрет продажи (`prohibited="1"`); нужна
  причина с флагом ImplOnAddDishInStopList.
- `ClearDishRests` - сбросить весь стоп-лист.
- Модификаторы: `GetModifierStopList`, `AddModifierToStopList`, `DeleteModifierFromStopList`.
- Маркировка: `ParseMarkingData` (GTIN по марке), `CheckMarking` (проверка марки в ОФД),
  партии - `AddBatchOfGoods` / `GetBatchOfGoodsList` / `DeleteBatchOfGoods`.
- Разливное: кеги - `LowAlcKegOpen` / `LowAlcKegList` / `LowAlcKegStatus` / `LowAlcKegDeactivate`
  (нужна настройка "Честного знака" у ресторана), крепкий алкоголь - `OpenBottle` /
  `GetOpenedBottleList` (нужен сервис учета алкоголя).

## 9. Касса, смены, печать

- `GetDrawerBalance` / `ChangeDrawerBalance` (amount > 0 - внесение, < 0 - изъятие, причина из
  DEPOSITCOLLECTREASONS).
- `RegisterEmployee` / `UnregisterEmployee` - смена работника на станции; `LoginOnStation` - вход.
- `CloseCardValShift`, `CloseCashShift`, `CloseCommonShift` - закрытие смен (необратимо).
- `GetPrintLayout` - получить документ (xml, txt, pdf, html...) без печати; `PrintMaket` - напечатать
  на станции (копия чека - Document 27 + ReceiptNum); `PrintDataXML` - произвольный текст разметкой
  из unifr.xsd.

## 10. Сообщения, КДС, опрос изменений

- `WaiterMessage` (обязателен expireTime) -> `GetWaiterMessages` -> `DelWaiterMessages` по id или
  external_id.
- КДС: `KDSGetDishData3` -> статусы блюд по `line_guid` -> `KDSSetDishData3`.
- Опрос без лишней нагрузки: GetOrderList, GetReceiptList, DeliveryGetOrderList, KDSGetDishData*
  принимают `lastversion` из предыдущего ответа и возвращают `Status="No changes"`, если ничего не менялось.
