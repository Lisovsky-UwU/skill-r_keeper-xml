# Команды XML-интерфейса r_keeper 7

Сгенерировано из XSD скриптом `scripts/xsd_to_reference.py`. Подробности по команде -
в `commands/<CMD>.md`. Влияние: R - чтение, W - изменяет данные, D - опасно. ✓ - есть
пример, проверенный на живом сервере.


## Система и справочники

| Команда | Влияние | Назначение |
|---|---|---|
| [CheckLicense](commands/CheckLicense.md) ✓ | R | [Кассовый сервер] Проверить есть ли у ресторана конкретная лицензия |
| [ExchangePriority](commands/ExchangePriority.md) ✓ | D | Команда ExchangePriority - переставить местами элементы по приоритету |
| [GetConnectInfoForNode](commands/GetConnectInfoForNode.md) ✓ | R | Получение низкоуровневой информации о подключенном узле |
| [GetDataListInfo](commands/GetDataListInfo.md) ✓ | R | [Кассовый сервер] Информация об очереди отправки данных |
| [GetFunctions](commands/GetFunctions.md) ✓ | R | [ВСЕ] Список поддерживаемых XML-функций |
| [GetItemBlob](commands/GetItemBlob.md) ✓ | R | Выполнение запроса AnyInfo на сервере FarCards |
| [GetParamValue](commands/GetParamValue.md) ✓ | R | Получить значение параметра |
| [GetRefData](commands/GetRefData.md) ✓ | R | Получить коллекцию |
| [GetRefDataFiltered](commands/GetRefDataFiltered.md) ✓ | R | xml-запрос GetRefDataLimited: Получить коллекцию |
| [GetRefList](commands/GetRefList.md) ✓ | R | GetRefList: Получить список имен коллекций |
| [GetSystemInfo2](commands/GetSystemInfo2.md) ✓ | R | [Касса, Кассовый сервер] Получить инфо о программе |
| [GetUsageValue](commands/GetUsageValue.md) ✓ | R | [Касса, Кассовый сервер] Получить значение использования |
| [GetXMLLicenseInstanceSeqNumber](commands/GetXMLLicenseInstanceSeqNumber.md) ✓ | R | [Касса,Кассовый сервер] Получение номера запроса по инстансу |
| [RegisterLogs](commands/RegisterLogs.md) ✓ | W | Зарегистрировать маски файлов логов |
| [SetRefData](commands/SetRefData.md) ✓ | D | Записать элементы коллекции |

## Устройства

| Команда | Влияние | Назначение |
|---|---|---|
| [CallDeviceMenu](commands/CallDeviceMenu.md) ✓ | W | Пользовательское меню на конкретной кассе для конкретного логического устройства |
| [DeviceStatuses](commands/DeviceStatuses.md) ✓ | R | Пользовательское меню на конкретной кассе для конкретного логического устройства |
| [ListDeviceMenu](commands/ListDeviceMenu.md) ✓ | R | Пользовательское меню на конкретной кассе для конкретного логического устройства |
| [LogicalDevices](commands/LogicalDevices.md) ✓ | R | Список загруженных драйверов на станции, запрос можно выполнять на любой санции и на любом кассовом сервере |
| [PrintDataXML](commands/PrintDataXML.md) ✓ | W | Печать пользовательского документа |

## Персонал

| Команда | Влияние | Назначение |
|---|---|---|
| [GetEmployeeInfo](commands/GetEmployeeInfo.md) ✓ | R | [Кассовый сервер] Получить информацию о работнике (права, список обслуживаемых столов) |
| [GetEmployeeInfo2](commands/GetEmployeeInfo2.md) ✓ | R | [Касса,Кассовый сервер] Получить информацию о работнике (права/привилегии) |
| [GetWaiterList](commands/GetWaiterList.md) ✓ | R | [Кассовый сервер] Получить список официантов, работающих со столом |
| [LoginOnStation](commands/LoginOnStation.md) ✓ | W | [Касса, Кассовый сервер] Зарегистрировать работника на кассе |
| [RegisterEmployee](commands/RegisterEmployee.md) ✓ | W | [Кассовый сервер] Зарегистрировать сотрудника |
| [UnregisterEmployee](commands/UnregisterEmployee.md) ✓ | W | [Кассовый сервер] Отменить регистрацию сотрудника |

## Заказы

| Команда | Влияние | Назначение |
|---|---|---|
| [CalcOrder](commands/CalcOrder.md) ✓ | R | [Кассовый сервер] Рассчет суммы заказа |
| [ChangeSessionCourse](commands/ChangeSessionCourse.md) ✓ | W |  |
| [CloseSeat](commands/CloseSeat.md) ✓ | W | Пометить посадочное место закрытым |
| [CloseVisit](commands/CloseVisit.md) ✓ | W | Закрыть визит |
| [CreateOrder](commands/CreateOrder.md) ✓ | W | [Кассовый сервер] Создать заказ |
| [CreateVisit](commands/CreateVisit.md) ✓ | W |  |
| [GetOrder](commands/GetOrder.md) ✓ | R | Получение содержимого заказа |
| [GetOrderBindings](commands/GetOrderBindings.md) ✓ | R | Получение биндингов по заказу |
| [GetOrderList](commands/GetOrderList.md) ✓ | R | Получить список заказов |
| [GetOrderList2](commands/GetOrderList2.md) ✓ | R | Получить список заказов (ver 2) |
| [LockOrder](commands/LockOrder.md) ✓ | W | [Касса, Кассовый сервер] Временная блокировка заказа |
| [OpenSeat](commands/OpenSeat.md) ✓ | W | [Кассовый сервер] Открыть закрытое посадочное место, начиная с версии 7.5.0.1 |
| [SaveOrder](commands/SaveOrder.md) ✓ | W | [Кассовый сервер, Касса] Запись содержимого заказа в базу |
| [SendToVDU](commands/SendToVDU.md) ✓ | W | [Кассовый сервер] Отправка блюд на VDU |
| [TransferDishes](commands/TransferDishes.md) ✓ | W | Перенос блюд между заказами |
| [UpdateOrder](commands/UpdateOrder.md) ✓ | W | [Кассовый сервер] Обновить свойства заказа |
| [ValidateOrder](commands/ValidateOrder.md) ✓ | R | Проверка корректности заказа |
| [VoidOrder](commands/VoidOrder.md) ✓ | D | [Кассовый сервер] Удалить заказ |

## Меню и остатки

| Команда | Влияние | Назначение |
|---|---|---|
| [ClearDishRests](commands/ClearDishRests.md) ✓ | D | [Кассовый сервер] Очистить список остатков блюд |
| [GetDishRest](commands/GetDishRest.md) ✓ | R | Получить остаток по блюду |
| [GetDishRests](commands/GetDishRests.md) ✓ | R | [Кассовый сервер] Получить список остатков блюд |
| [GetOrderMenu](commands/GetOrderMenu.md) ✓ | R | Получение списка доступных блюд и модификаторов |
| [GetOrderMenu2](commands/GetOrderMenu2.md) ✓ | R | Получение списка доступных блюд и модификаторов |
| [SetDishRests](commands/SetDishRests.md) ✓ | W | [Кассовый сервер] Изменить остатки блюд |

## Оплата и чеки

| Команда | Влияние | Назначение |
|---|---|---|
| [CalcOrder2](commands/CalcOrder2.md) ✓ | R | [Кассовый сервер] Рассчет суммы заказа (версия 2) |
| [CalcOrder3](commands/CalcOrder3.md) ✓ | R | [Кассовый сервер] Рассчет суммы заказа (версия 3), с возвратом причины недоступности валют |
| [CreateInvoice](commands/CreateInvoice.md) ✓ | W | [Кассовый сервер] Создать счет/фактуру, привязать к заказу |
| [DeleteReceipt](commands/DeleteReceipt.md) ✓ | D | Удаление чека |
| [DeleteReceiptPayments](commands/DeleteReceiptPayments.md) ✓ | D | [Кассовый сервер] Удалить оплаты в ошибочном чеке |
| [FindReceiptsForReturn](commands/FindReceiptsForReturn.md) ✓ | R | Поиск чеков для возврата |
| [GetInvoice](commands/GetInvoice.md) ✓ | R | [Кассовый сервер] Получить содержимое счет/фактуры. Указать нужно либо заказ, либо guid счет/фактуры |
| [GetReceiptList](commands/GetReceiptList.md) ✓ | R | [Кассовый сервер] Получить список чеков (с версии 7.5.3.202) |
| [MakeReturnGoods](commands/MakeReturnGoods.md) ✓ | D | [Кассовый сервер] Возврат товара |
| [PayOrder](commands/PayOrder.md) ✓ | W | [Касса,Кассовый сервер] Оплата заказа/чека |
| [PrintBill](commands/PrintBill.md) ✓ | W | [Кассовый сервер] Печать пречека |
| [UndoBill](commands/UndoBill.md) ✓ | W | [Кассовый сервер] Отмена пречека |
| [UndoReceipt](commands/UndoReceipt.md) ✓ | D | Аннулирование чека |

## Касса и смены

| Команда | Влияние | Назначение |
|---|---|---|
| [ChangeDrawerBalance](commands/ChangeDrawerBalance.md) ✓ | W | [Кассовый сервер] Внести/изъять деньги из ящика |
| [CloseCardValShift](commands/CloseCardValShift.md) ✓ | D | [Кассовый сервер] Закрытие смены на банковском терминале |
| [CloseCashShift](commands/CloseCashShift.md) ✓ | D | [Кассовый сервер] Закрыть кассовую смену |
| [CloseCommonShift](commands/CloseCommonShift.md) ✓ | D | [Кассовый сервер] Закрыть общую смену |
| [ConfirmOperation](commands/ConfirmOperation.md) ✓ | W | [Кассовый сервер, Касса] Подвердить выполнение операции, записать операцию в журнал операций |
| [GetDrawerBalance](commands/GetDrawerBalance.md) ✓ | R | [Кассовый сервер] Получить остатки денег в ящике |

## Карты и ПДС

| Команда | Влияние | Назначение |
|---|---|---|
| [ApplyPersonalCard](commands/ApplyPersonalCard.md) ✓ | W | Применение карты ПДС |
| [FarCardsAnyInfoRaw](commands/FarCardsAnyInfoRaw.md) ✓ | R | Выполнение запроса AnyInfo на сервере FarCards |
| [FarCardsAnyInfoXML](commands/FarCardsAnyInfoXML.md) ✓ | R | Выполнение запроса AnyInfo на сервере FarCards |
| [GetCardInfo](commands/GetCardInfo.md) ✓ | R | [Касса, Кассовый сервер] Получить инфо о карте ПДС |
| [MakeCardDeposit](commands/MakeCardDeposit.md) ✓ | W | [Кассовый сервер] Пополнить/изъять средства с/на карту ПДС |
| [ParseMCR](commands/ParseMCR.md) ✓ | R | [Касса] Парсинг строки при помощи MCR-алгоритмов |
| [UndoPersonalCard](commands/UndoPersonalCard.md) ✓ | W | [Кассовый сервер] Отмена карты ПДС |

## Банковский терминал

| Команда | Влияние | Назначение |
|---|---|---|
| [TerminalAuthError](commands/TerminalAuthError.md) ✓ | W | Авторизация карты через терминал: ошибка |
| [TerminalAuthError2](commands/TerminalAuthError2.md) ✓ | W | Отменить авторизацию терминалом (ver 2) |
| [TerminalAuthPay](commands/TerminalAuthPay.md) ✓ | W | Авторизация карты через терминал: оплата |
| [TerminalAuthPay2](commands/TerminalAuthPay2.md) ✓ | W | Завершить авторизацию терминалом (ver 2) |
| [TerminalAuthStart](commands/TerminalAuthStart.md) ✓ | W | Авторизация карты через терминал: старт |
| [TerminalAuthStart2](commands/TerminalAuthStart2.md) ✓ | W | Начать авторизацию карты через терминал (ver 2) |

## Печать и отчеты

| Команда | Влияние | Назначение |
|---|---|---|
| [GetDocByLayout](commands/GetDocByLayout.md) ✓ | R | [Кассовый сервер] Получить данные по макету печати. УСТАРЕВШИЙ!!! Рекомендуется использовать GetPrintLayout |
| [GetPrintLayout](commands/GetPrintLayout.md) ✓ | R | [Кассовый сервер] Получить данные по макету печати |
| [PrintMaket](commands/PrintMaket.md) ✓ | W | Печать документа |

## Сообщения и станция

| Команда | Влияние | Назначение |
|---|---|---|
| [CloseWebForm](commands/CloseWebForm.md) ✓ | W | [Касса, Кассовый сервер] Закрыть на кассе окно с web-браузером |
| [DelWaiterMessages](commands/DelWaiterMessages.md) ✓ | W | Удалить сообщения официанта |
| [GetWaiterMessages](commands/GetWaiterMessages.md) ✓ | R | Получить список сообщений официанта |
| [OpenWebForm](commands/OpenWebForm.md) ✓ | D | [Касса, Кассовый сервер] Показать на кассе окно с web-браузером |
| [WaiterMessage](commands/WaiterMessage.md) ✓ | W | [Касса, Кассовый сервер] Отправка сообщения официанту |

## КДС

| Команда | Влияние | Назначение |
|---|---|---|
| [KDSGetDishData2](commands/KDSGetDishData2.md) ✓ | R | [Кассовый север] КДС: Получить данные по блюдам и заказам. Начиная с 7.5.3.222, 7.5.4.068 |
| [KDSGetDishData3](commands/KDSGetDishData3.md) ✓ | R | [Кассовый север] КДС: Получить данные по блюдам и заказам. Данный запрос возвращает все блюда, как распечатанные так и нераспечатанные, включая пакеты-черновики |
| [KDSSetDishData2](commands/KDSSetDishData2.md) ✓ | W | [Кассовый сервер] Изменить статус готовности у блюда (КДС) |
| [KDSSetDishData3](commands/KDSSetDishData3.md) ✓ | W | [Кассовый сервер] Изменить статус готовности у блюда (КДС) ver 3 |

## Тарификация

| Команда | Влияние | Назначение |
|---|---|---|
| [AddExternalTariff](commands/AddExternalTariff.md) ✓ | W | Добавить данные по внешней тарификации |

## Доставка

| Команда | Влияние | Назначение |
|---|---|---|
| [DeliveryCancelEdit](commands/DeliveryCancelEdit.md) ✓ | W | [Касса, Кассовый сервер] Доставка: отмена редактирования |
| [DeliveryChangeRestState](commands/DeliveryChangeRestState.md) ✓ | W | [Касса] Доставка: изменение статуса ресторана |
| [DeliveryConfirmEdit](commands/DeliveryConfirmEdit.md) ✓ | W | [Касса, Кассовый сервер] Доставка: подтверждение редактирования |
| [DeliveryEditOrder](commands/DeliveryEditOrder.md) ✓ | D | [Касса, Кассовый сервер] Доставка: Редактировать заказ |
| [DeliveryGetOrderList](commands/DeliveryGetOrderList.md) ✓ | R | [Касса,Кассовый сервер]Доставка: получить список заказов доставки |
| [DeliveryLockOrder](commands/DeliveryLockOrder.md) ✓ | W | [Касса, Кассовый сервер] Доставка: временная блокировака заказа |
| [DeliveryPayOrders](commands/DeliveryPayOrders.md) ✓ | W | Доставка: печать чека/пречека при отправке экспедитора |
| [DeliveryPostOrder](commands/DeliveryPostOrder.md) ✓ | W | [Касса, Кассовый сервер] Отправка заказа в ресторан. Требуется лицензиция XML-Save order |
| [DeliveryPrintInvoice](commands/DeliveryPrintInvoice.md) ✓ | W | [Касса, Кассовый сервер] Доставка: напечатать накладную |
| [DeliveryServPrint](commands/DeliveryServPrint.md) ✓ | W | [Касса, Кассовый сервер] Доставка: ручная отправка на сервис-печать |
| [DeliverySetForwarder](commands/DeliverySetForwarder.md) ✓ | W | [Касса, Кассовый сервер] Доставка: назначить экспедитора |
| [DeliverySetLastProcessTime](commands/DeliverySetLastProcessTime.md) ✓ | W | [Кассовый сервер] Доставка: изменить "время обработки заказа" |
| [DeliverySetOrderNumGen](commands/DeliverySetOrderNumGen.md) ✓ | D | [Касса,Кассовый сервер] Доставка: изменение генератора для нумерации заказа |
| [DeliveryUpdateStatus](commands/DeliveryUpdateStatus.md) ✓ | W | [Касса, Кассовый сервер] Доставка: изменение статуса доставки |
| [DeliveryValidateOrder](commands/DeliveryValidateOrder.md) ✓ | R | [Касса, Кассовый сервер]Доставка: проверить блюда заказа на доступность + расчет новых цен |
| [DeliveryVoidOrder](commands/DeliveryVoidOrder.md) ✓ | D | [Касса, Кассовый сервер] Доставка: удалить заказ |

## Только касса

| Команда | Влияние | Назначение |
|---|---|---|
| [ApplyMCR](commands/ApplyMCR.md) ✓ | W | [Касса] Применение MCR-алгоритмов к кассе (эмуляция прокатывания карты) |
| [GotoOrder](commands/GotoOrder.md) ✓ | D | [Касса] Открыть на кассе заказ на редактирование |
| [PerformMessage](commands/PerformMessage.md) ✓ | W | [Касса] Выполнить операцию с ожиданием завершения |
| [PostMessage](commands/PostMessage.md) ✓ | W | [Касса] Поместить сообщение в очередь сообщений |
| [WaitWindow](commands/WaitWindow.md) ✓ | W | [Касса] Ожидание появления опреденного окна |

## Служебные

| Команда | Влияние | Назначение |
|---|---|---|
| [ReloadWorkUdb](commands/ReloadWorkUdb.md) ✓ | D | [Кассовый сервер] Загрузить новый work.udb без перезапуска кассового сервера |

## Прочее

| Команда | Влияние | Назначение |
|---|---|---|
| [ETPC](commands/ETPC.md) |  | xml-query to ETPC |
