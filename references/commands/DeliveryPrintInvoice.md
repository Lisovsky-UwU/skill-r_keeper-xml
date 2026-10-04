# DeliveryPrintInvoice

[Касса, Кассовый сервер] Доставка: напечатать накладную

Схемы: `schemas/Delivery/qryDeliveryPrintInvoice.xsd`, `schemas/Delivery/resDeliveryPrintInvoice.xsd`
Влияние: изменяет данные

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Order> [resOrderItem]  - Заказ с cодержимым. Содержимое нужно заполнять в том случае, если заказа больше нет в базе
    <Creator>? [resEmployeeItem]  - Работник, создавший заказ
      (resRefItem: id | code | guid)
      <Role>? [resRefItem]  - Роль работника
    <Waiter>  - Главный официант заказа
      (resRefItem: id | code | guid)
      <Role> [resRefItem]  - Роль главного официанта
    <Station>? [resRefItem]  - Станция, на которой был создан заказ
    <OrderCategory>? [resRefItem]  - Категория заказа
    <OrderType> [resRefItem]  - Тип заказа
    <Table> [resRefItem]  - Стол
    <GuestType>? [resRefItem]  - Тип гостей
    <Restaurant>? [resRefItem]  - Ресторан доставки
    <Guests>? [Guests_Item]  - Список гостей
      <Guest>* [guest_item]
        <Interface>? [refItem]  - Интерфейс к карте гостя
        <EntranceCardType>? [refItem]  - Тип карты на входе. Добавлено в 7.07.00.300
        @guestLabel!: token  - Текстовая метка гостя
        @cardCode: normalizedString  - Код карты гостя
        @clientID: int  - ID адреса гостя
        @addressID: int  - ID адреса гостя
        @maxamount: int  - Максимальная сумма по заказам, в копейках. Только для чтения. Добавлено в 7.07.00.300
        @restAmount: int  - Остаток масимальной суммы по заказам, в копейках. Только для чтения. Добавлено в 7.07.00.362+
      @count: int  - Количество гостей
    <ExternalProps>? [externalProps]  - Список внешних свойств заказа
      <Prop>* [externalPropItem]
        @name!: normalizedString  - Имя свойства
        @value: normalizedString (по умолчанию "")  - Значение свойства
    <ExtraTables>? [extraTables]  - Список дополнительных столов заказа
      <item>*  - Дополнительный стол
        @id: nonNegativeInteger
        @code: nonNegativeInteger
        @guid: guidString
    <SourceOrder>? [orderElement]  - Исходный заказ. Заполняется в случае заказа возврата, содержит ссылку на заказ, из которого выполняется возврат блюд
    <DeliveryBlock>? [deliveryBlock]
      @deliveryState: int  - Статус доставки
      @startTime: dateTime  - Время создания заказа
      @travelTime: dateTime  - Время в пути
      @deliveryTime: dateTime  - Ожидаемое время доставки
      @forwarderSendTime: dateTime  - Время отправки экспедитора
      @forwarderReturnTime: dateTime  - Время возвращения экспедитора
      @realDeliveryTime: dateTime  - Реальное время доставки
      @lastProcessTime: dateTime  - Время последней обработки заказа. Заполняет Delivery
      @minCookTime: dateTime  - Минимальное время приготовления заказа
      @zoneID: int  - ID зоны доставки
      @zoneName: normalizedString  - Имя зоны доставки
      @orderPrefix: normalizedString  - Префиск для имени заказа
      @isTakeOut: boolean  - Флаг - доставка на вынос. Если флаг выставлен, то статусами доставки на филиале управляет RK7
      @autoChangeState: boolean  - Флаг - разрешение автоматического изменения статусов доставки в rk7
    <Session>* [resSessionItem]  - Список пакетов заказа
      @uni: nonNegativeInteger  - UNI пакета. Если задан, то перезаписывается содержимое пакета. Иначе создается новый пакет
      @line_guid: guidString  - GUID пакета
      @isDraft: boolean  - Флаг "Пакет является черновиком"
      @printed: boolean  - Флаг - пакет распечатан
      @printTime: dateTime  - Время первой сервис-печати. Если не задано, то используется время remindAt
      @remindTime: dateTime  - Время начала готовки блюд пакета. Если не задано, то используется текущее время
      @readyTime: dateTime  - Время, к которому должны быть приготовлены все блюда пакета
      @startService: dateTime  - Время, в которое блюда были добавлены в заказ. Если не задано, то используется время printAt
      @* - допускаются любые другие атрибуты
      <Station>? [resRefItem]  - Станция, на которой пакет был добавлен
      <Author>? [resEmployeeItem]  - Работник, последний редактировавший заказ (структура - см. выше)
      <Creator>? [resEmployeeItem]  - Работник, создавший пакет (структура - см. выше)
      <Course>? [resRefItem]  - Порядок подачи
      (одно из - повторяется:)
        <Dish> [resDishItem]  - Блюдо
          (refItem: id | code | guid)
          @uni: nonNegativeInteger  - UNI элемента. Если задан, то элемент обновляется, иначе создается новый. Только для нераспечатанных элементов
          @line_guid: guidString  - GUID строки
          @state: CheckItemState {1 | 3 | 4 | 5 | 6 | 7}  - Статус элемента (с версии 7.5.4.206)
          @* - допускаются любые другие атрибуты
          (одно из - повторяется:)
            <Modi> [modiItem]  - Модификатор
              (refItem: id | code | guid)
              @uni: nonNegativeInteger  - UNI элемента. Если задан, то элемент обновляется, иначе создается новый. Только для нераспечатанных элементов
              @line_guid: guidString  - GUID строки
              @state: CheckItemState {1 | 3 | 4 | 5 | 6 | 7}  - Статус элемента (с версии 7.5.4.206)
              @* - допускаются любые другие атрибуты
              <Marking>? [markingData]  - Данные маркировки, заполняется для модификаторов маркировки. Свойство read only, его нельзя заполнять. Добавлено в 7.07.00.329
                @reqId: normalizedString  - Уникальный идентификатор запроса проверки маркировки (UUID)
                @reqTimestamp: int  - Дата и время формирования запроса (с точностью до миллисекунд)
              @price: int  - Цена или открытая цена модификатора (в копейках)
              @count: positiveInteger (по умолчанию "1")  - Количество модификаторов (не умноженное на количество блюда)
              @openName: normalizedString  - Произвольное имя модификатора
              @data: base64Binary  - Произвольное имя модификатора в base64-формате (для записи бинарных данных), начиная с 7.07.00.242
              @isDefault: boolean (по умолчанию "1")  - Флаг - модификатор по умолчанию
              @freeCount: int  - количество бесплатных модификаторов у позиции (не умноженное на количество блюда)
              @amount: int  - Сумма модификатора, добавленная к блюду (в копейках) к оплате
              @priceListAmount: int  - Сумма модификатора, добавленная к блюду (в копейках) по прайс-листу (без скидок и добавляемых налогов)
            <Discount> [discountItem]  - Скидка
              (refItem: id | code | guid)
              @uni: nonNegativeInteger  - UNI элемента. Если задан, то элемент обновляется, иначе создается новый. Только для нераспечатанных элементов
              @line_guid: guidString  - GUID строки
              @state: CheckItemState {1 | 3 | 4 | 5 | 6 | 7}  - Статус элемента (с версии 7.5.4.206)
              @* - допускаются любые другие атрибуты
              <Interface>? [refItem]  - Интерфейс к карте гостя. Обезателен для заполнения, если задан cardCode
              <BonusType>? [refItem]  - Тип бонуса, заполняется для скидок ПДС
              @amount: int  - Сумма скидки (в копейках) для суммовых скидок, или процент скидки (в долях) для процентных скидок, для скидок с ручным вводом значения скидки
              @maxamount: int  - Максимальная сумма скидки (в копейках)
              @seat: nonNegativeInteger (по умолчанию "0")  - Номер посадочного места: 0 - не задано
              @cardCode: normalizedString  - Код карточки
              @deleted: boolean  - Признак того что скидка удалена
              @charge_dish_line_guid: guidString (по умолчанию "")  - GUID-блюда нераспределяемой наценки (для нераспределяемых наценок). Начиная с 7.6.0.101
              @charge_source: ChargeSource {byHand | pay | automatic | changeTip | pdsCard | discountCard | fiscalDeposit | comboDiscount | script | orderMinimalAmount | xmlInterface | currencyRound | coupon | latePrepayDeletion | payAsDiscount | bankCardDiscount | forReturnOrders}  - Источник добавления наценки (с версии 7.25.07.X)
            <Void> [voidItem]  - Отказы (для распечатанных блюд)
              (refItem: id | code | guid)
              @uni: nonNegativeInteger  - UNI элемента. Если задан, то элемент обновляется, иначе создается новый. Только для нераспечатанных элементов
              @line_guid: guidString  - GUID строки
              @state: CheckItemState {1 | 3 | 4 | 5 | 6 | 7}  - Статус элемента (с версии 7.5.4.206)
              @* - допускаются любые другие атрибуты
              <Author> [refItem]  - Работник, выполняющий удаление
              @dateTime: dateTime  - ДатаВремя создания воида
              @quantity!: int  - Количество удаляемого блюда (в тысячных долях)
              @amount: int  - Сумма удаляемого блюда
              @openName: normalizedString  - Открытое имя причины удаления
            <Consum> [consumItem]  - Консуманты
              (refItem: id | code | guid)
              @uni: nonNegativeInteger  - UNI элемента. Если задан, то элемент обновляется, иначе создается новый. Только для нераспечатанных элементов
              @line_guid: guidString  - GUID строки
              @state: CheckItemState {1 | 3 | 4 | 5 | 6 | 7}  - Статус элемента (с версии 7.5.4.206)
              @* - допускаются любые другие атрибуты
              <Author> [refItem]  - Работник, который добавил консуманта
              @amount: int  - Сумма консумации (в копейках)
          @price: nonNegativeInteger  - Цена блюда (в копейках)
          @SourceGUIDString: guidString  - line_guid возвращаемого блюда. Заполняется в случае заказа возврата, содержит ссылку на исходное блюдо, возврат которого выполняется данной строкой
          <OrderType> [refItem]  - Тип заказа на блюдо
          @quantity!: int  - Количество блюда (в тысячных долях), для добавляемых блюд. Если кол-во меньше нуля, то это блюдо выкупа, иначе обычная продажа
          @srcQuantity: int  - Количество блюда, без учета отказов (в тысячных долях, с 7.4.16.2)
          @seat: nonNegativeInteger (по умолчанию "0")  - Номер посадочного места: 0 - не задано
          @changeWeight: boolean (по умолчанию "0")  - Атрибут учитывается только для весовых блюд. Если в запросе передан тот же вес, что задан в заказе и в этом поле передано true, то будет считаться, что вес для блюда указан. Если же в запросе передан тот же вес, что задан в заказе и этот атрибут не передан (передано false), то будет считаться, что …
          <Tariff>? [tariff]  - Информация о тарифе, заполняется для блюд тарификации
            <Table> [refItem]  - Тарифицируемое устройство
            <Detail> [tariffDetail]  - Детализация тарификации
              @id: nonNegativeInteger
              @code: nonNegativeInteger
              @guid: guidString
              @startTime: dateTime  - Время начала детализации тарификации
              @endTime: dateTime  - Время окончания детализации тарификации
            @moneyLimit: int  - Лимит по деньгам (в копейках)
            @timeLimit: dateTime  - Лимит по времени
            @status: tariffStatus {active | paused | finished}  - Статус тарификации (active, paused, finished)
            @startTime: dateTime  - Время начала тарификации
            @endTime: dateTime  - Время окончания тарификации
          <KDSState>* [KDSStateItem]  - Подробная информация о КДС статусе блюда (с версии 7.26.03.0)
            @name: KDSStateType {"" | sent | started | ready | taken | collect | collected | startpark | endpark | removed}  - КДС статус блюда
            @at: dateTime  - Датавремя выставления КДС статуса
          @amount: int  - Сумма блюда (в копейках)
          @priceListAmount: int  - Сумма блюда (в копейках) по прайс-листу (без скидок и добавляемых налогов)
          @kdsstate: KDSStateType {"" | sent | started | ready | taken | collect | collected | startpark | endpark | removed} (по умолчанию "")  - КДС статус блюда (с версии 7.5.5.037)
          @new: boolean (по умолчанию "false")  - Флаг - новое блюдо (последний добавленный элемент)
          @sortOrder: int  - Порядковый номер записи (с версии 7.07.00.246)
          @WeightNeeded: boolean  - Флаг "Для блюда требуется указание веса"
          @isTareDish: boolean (по умолчанию "0")  - Признак, что блюдо является тарой
          @tare_dish_line_guid: guidString  - GUID блюда-тары, которое связано с текущим блюдом
        <Combo> [resComboItem]  - Комбо блюдо
          (refItem: id | code | guid)
          @uni: nonNegativeInteger  - UNI элемента. Если задан, то элемент обновляется, иначе создается новый. Только для нераспечатанных элементов
          @line_guid: guidString  - GUID строки
          @state: CheckItemState {1 | 3 | 4 | 5 | 6 | 7}  - Статус элемента (с версии 7.5.4.206)
          @* - допускаются любые другие атрибуты
          (одно из - повторяется:)
            <Modi> [modiItem]  - Модификатор (структура - см. выше)
            <Discount> [discountItem]  - Скидка (структура - см. выше)
            <Void> [voidItem]  - Отказы (для распечатанных блюд) (структура - см. выше)
            <Consum> [consumItem]  - Консуманты (структура - см. выше)
          @price: nonNegativeInteger  - Цена блюда (в копейках)
          @SourceGUIDString: guidString  - line_guid возвращаемого блюда. Заполняется в случае заказа возврата, содержит ссылку на исходное блюдо, возврат которого выполняется данной строкой
          <OrderType> [refItem]  - Тип заказа на блюдо
          @quantity!: int  - Количество блюда (в тысячных долях), для добавляемых блюд. Если кол-во меньше нуля, то это блюдо выкупа, иначе обычная продажа
          @srcQuantity: int  - Количество блюда, без учета отказов (в тысячных долях, с 7.4.16.2)
          @seat: nonNegativeInteger (по умолчанию "0")  - Номер посадочного места: 0 - не задано
          @changeWeight: boolean (по умолчанию "0")  - Атрибут учитывается только для весовых блюд. Если в запросе передан тот же вес, что задан в заказе и в этом поле передано true, то будет считаться, что вес для блюда указан. Если же в запросе передан тот же вес, что задан в заказе и этот атрибут не передан (передано false), то будет считаться, что …
          <Modi>? [modiItem] (структура - см. выше)
          <Component>* [resComboComponent]  - Комбо компонент
            (refItem: id | code | guid)
            @uni: nonNegativeInteger  - UNI элемента. Если задан, то элемент обновляется, иначе создается новый. Только для нераспечатанных элементов
            @line_guid: guidString  - GUID строки
            @state: CheckItemState {1 | 3 | 4 | 5 | 6 | 7}  - Статус элемента (с версии 7.5.4.206)
            @* - допускаются любые другие атрибуты
            (одно из - повторяется:)
              <Modi> [modiItem]  - Модификатор (структура - см. выше)
              <Discount> [discountItem]  - Скидка (структура - см. выше)
              <Void> [voidItem]  - Отказы (для распечатанных блюд) (структура - см. выше)
              <Consum> [consumItem]  - Консуманты (структура - см. выше)
            @price: nonNegativeInteger  - Цена блюда (в копейках)
            @SourceGUIDString: guidString  - line_guid возвращаемого блюда. Заполняется в случае заказа возврата, содержит ссылку на исходное блюдо, возврат которого выполняется данной строкой
            <ComboModi>? [refItem]  - Комбо-модификатор, соответствующий комбо-компоненту. По умолчанию возьмется первый подходящий
            @count: positiveInteger (по умолчанию "1")
            @isDefault: boolean (по умолчанию "1")  - Флаг - компонент по умолчанию
            <KDSState>* [KDSStateItem]  - Подробная информация о КДС статусе блюда (с версии 7.26.03.0) (структура - см. выше)
            @kdsstate: KDSStateType {"" | sent | started | ready | taken | collect | collected | startpark | endpark | removed} (по умолчанию "")  - КДС статус блюда (с версии 7.5.5.037)
          <KDSState>* [KDSStateItem]  - Подробная информация о КДС статусе блюда (с версии 7.26.03.0) (структура - см. выше)
          @kdsstate: KDSStateType {"" | sent | started | ready | taken | collect | collected | startpark | endpark | removed} (по умолчанию "")  - КДС статус блюда (с версии 7.5.5.037)
          @amount: int  - Сумма блюда (в копейках)
          @new: boolean  - Флаг - новое блюдо (последний добавленный элемент)
        <Discount> [resDiscountItem]  - Скидка
          (refItem: id | code | guid)
          @uni: nonNegativeInteger  - UNI элемента. Если задан, то элемент обновляется, иначе создается новый. Только для нераспечатанных элементов
          @line_guid: guidString  - GUID строки
          @state: CheckItemState {1 | 3 | 4 | 5 | 6 | 7}  - Статус элемента (с версии 7.5.4.206)
          @* - допускаются любые другие атрибуты
          <Interface>? [refItem]  - Интерфейс к карте гостя. Обезателен для заполнения, если задан cardCode
          <BonusType>? [refItem]  - Тип бонуса, заполняется для скидок ПДС
          @amount: int  - Сумма скидки (в копейках) для суммовых скидок, или процент скидки (в долях) для процентных скидок, для скидок с ручным вводом значения скидки
          @maxamount: int  - Максимальная сумма скидки (в копейках)
          @seat: nonNegativeInteger (по умолчанию "0")  - Номер посадочного места: 0 - не задано
          @cardCode: normalizedString  - Код карточки
          @deleted: boolean  - Признак того что скидка удалена
          @charge_dish_line_guid: guidString (по умолчанию "")  - GUID-блюда нераспределяемой наценки (для нераспределяемых наценок). Начиная с 7.6.0.101
          @charge_source: ChargeSource {byHand | pay | automatic | changeTip | pdsCard | discountCard | fiscalDeposit | comboDiscount | script | orderMinimalAmount | xmlInterface | currencyRound | coupon | latePrepayDeletion | payAsDiscount | bankCardDiscount | forReturnOrders}  - Источник добавления наценки (с версии 7.25.07.X)
          @discountSum!: int  - Рассчитанная сумма скидки (в копейках)
        <Prepay> [prepayItem]  - Предоплата
          (refItem: id | code | guid)
          @uni: nonNegativeInteger  - UNI элемента. Если задан, то элемент обновляется, иначе создается новый. Только для нераспечатанных элементов
          @line_guid: guidString  - GUID строки
          @state: CheckItemState {1 | 3 | 4 | 5 | 6 | 7}  - Статус элемента (с версии 7.5.4.206)
          @* - допускаются любые другие атрибуты
          <Interface>? [refItem]  - Интерфейс, связанный с оплатой
          @amount!: int  - Сумма (в копейках)
          @basicSum: int  - Сумма платежа в базовой валюте (в копейках). Начиная с 7.6.0.087
          @cardCode: normalizedString  - Номер персональной карты
          @extTransactionInfo: normalizedString  - Расширенная информация об авторизации. Начиная с версии 7.5.3.111
          @TransactionStatus: TransactionStatusType {1 | 2 | 3 | 4 | 5 | 6}  - Статус авторизации. Начиная с версии 7.5.4.211
          @seat: nonNegativeInteger (по умолчанию "0")  - Номер посадочного места: 0 - не задано
          @discount_line_guid: guidString (по умолчанию "")  - GUID-связанной с оплатой скидкой (для оплат как скидка). Начиная с 7.6.0.087
          @deleted: boolean  - Признак того что платеж удален
          @owner: normalizedString (по умолчанию "")  - Владелец валюты (VISA, Master card). С версии 7.06.04.430+, 7.06.05.296+
          @authtype: AuthType {error | auto | voice | terminal | voicepossible} (по умолчанию "auto")  - Тип авторизации. С версии 7.06.04.430+, 7.06.05.296+
          @authcode: normalizedString (по умолчанию "")  - Код авторизации. С версии 7.06.04.430+, 7.06.05.296+
          @extIntegerInfo: int (по умолчанию "0")  - Номер банковского терминала. С версии 7.06.04.430+, 7.06.05.296+
          @transactionNumber: int (по умолчанию "0")  - Номер транзакции. С версии 7.06.04.430+, 7.06.05.296+
          <Reason>? [refItem]  - Причина внесения предоплаты
          @promised: boolean  - Предоплата является обещанным платежом
        <Pay> [payItem]  - Оплата
          (refItem: id | code | guid)
          @uni: nonNegativeInteger  - UNI элемента. Если задан, то элемент обновляется, иначе создается новый. Только для нераспечатанных элементов
          @line_guid: guidString  - GUID строки
          @state: CheckItemState {1 | 3 | 4 | 5 | 6 | 7}  - Статус элемента (с версии 7.5.4.206)
          @* - допускаются любые другие атрибуты
          <Interface>? [refItem]  - Интерфейс, связанный с оплатой
          @amount!: int  - Сумма (в копейках)
          @basicSum: int  - Сумма платежа в базовой валюте (в копейках). Начиная с 7.6.0.087
          @cardCode: normalizedString  - Номер персональной карты
          @extTransactionInfo: normalizedString  - Расширенная информация об авторизации. Начиная с версии 7.5.3.111
          @TransactionStatus: TransactionStatusType {1 | 2 | 3 | 4 | 5 | 6}  - Статус авторизации. Начиная с версии 7.5.4.211
          @seat: nonNegativeInteger (по умолчанию "0")  - Номер посадочного места: 0 - не задано
          @discount_line_guid: guidString (по умолчанию "")  - GUID-связанной с оплатой скидкой (для оплат как скидка). Начиная с 7.6.0.087
          @deleted: boolean  - Признак того что платеж удален
          @owner: normalizedString (по умолчанию "")  - Владелец валюты (VISA, Master card). С версии 7.06.04.430+, 7.06.05.296+
          @authtype: AuthType {error | auto | voice | terminal | voicepossible} (по умолчанию "auto")  - Тип авторизации. С версии 7.06.04.430+, 7.06.05.296+
          @authcode: normalizedString (по умолчанию "")  - Код авторизации. С версии 7.06.04.430+, 7.06.05.296+
          @extIntegerInfo: int (по умолчанию "0")  - Номер банковского терминала. С версии 7.06.04.430+, 7.06.05.296+
          @transactionNumber: int (по умолчанию "0")  - Номер транзакции. С версии 7.06.04.430+, 7.06.05.296+
        <PrintCheck> [PrintCheckItem]  - Чек
          <Author>? [resEmployeeItem]  - Кассир, создавший чек (структура - см. выше)
          <Reason>? [refItem]  - Причина удаления чека
          <DeleteManager>? [resEmployeeItem]  - Работник, удаливший чек (структура - см. выше)
          <Pay>* [payItem]  - Оплата (структура - см. выше)
          <Prepay>* [prepayItem]  - Предоплата (структура - см. выше)
          @uni: nonNegativeInteger  - UNI элемента. Если задан, то элемент обновляется, иначе создается новый. Только для нераспечатанных элементов
          @line_guid: guidString  - GUID чека
          @seat: nonNegativeInteger (по умолчанию "0")  - Номер посадочного места: 0 - не задано
          @CheckNum: nonNegativeInteger  - Номер чека
          @invoice: nonNegativeInteger  - Номер накладной
          @amount!: positiveInteger  - Сумма чека (в копейках)
          @unpaidSum: int (по умолчанию "0")  - Сумма к оплате, с учетом ранее внесенных оплат/предоплат (в копейках)
          @GlobalFiscalID: string  - Глобальный фискальный номер чека
          @state: CheckItemState {1 | 3 | 4 | 5 | 6 | 7}  - Статус элемента (с версии 7.5.4.206)
          @deleted: boolean  - Флаг "Чек удален"
          @bill: boolean  - Флаг "Чек является пречеком"
          @printTime: dateTime  - Время печати чека
          @startTime: dateTime  - Время начала обслуживания чека
          @intentReceiptType: IntentReceiptType {"" | OneCheck | CreditCheck}  - Тип чека намерения (с версии 7.25.03.0)
          @intentReceiptStage: IntentReceiptStage {"" | First stage | Completed}  - Этап печати чека намерения (с версии 7.25.03.0)
      <PriceScale> [resRefItem]  - Тип цены, используемый для содержимого пакета
      <TradeGroup> [resRefItem]  - Торговая группа
      @cookMins!: nonNegativeInteger  - Время приготовления (минуты)
      @sessionID: int  - UNI пакета
    @visit: nonNegativeInteger (по умолчанию "0")
    @orderIdent: nonNegativeInteger (по умолчанию "0")
    @url!: normalizedString  - URL заказа для code.ucs.ru
    @persistentComment: normalizedString  - Сохраняемый комментарий заказа
    @nonPersistentComment: normalizedString  - Несохраняемый комментарий заказа
    @openTime!: dateTime  - Время создания заказа (для банкетных столов время начала банкета)
    @reserve: boolean  - Резервный заказ
    @duration: dateTime  - Длительность заказа (банкета)
    @holder: normalizedString  - Владелец банкета (для банкетных заказов)
    @promoCode: normalizedString  - Промо-код заказа
    @orderName!: normalizedString  - Имя заказа
    @seqNumber: int  - Последовательный номер заказа
    @version!: nonNegativeInteger  - Версия заказа
    @crc32!: int  - Контрольная сумма по содержимому заказа
    @guid!: guidString  - GUID заказа
    @locked: boolean  - Флаг - заказ заблокирован для редактирования
    @deleted: boolean  - Флаг - все блюда заказа удалены
    @orderSum!: nonNegativeInteger  - Сумма заказа (в копейках)
    @prepaySum: nonNegativeInteger (по умолчанию "0")  - Сумма незакрытых предоплат (в копейках)
    @promisedSum: nonNegativeInteger (по умолчанию "0")  - Сумма обещанных платежей (в копейках)
    @discountSum!: int  - Сумма скидок (в копейках)
    @unpaidSum!: int  - Неоплаченная сумма заказа (в копейках)
    @totalPieces!: nonNegativeInteger  - Количество порций в заказе (в тысячных долях)
    @cookMins!: nonNegativeInteger  - Время приготовления (минуты)
    @paid: boolean (по умолчанию "false")  - Флаг - заказ оплачен
    @purchase: boolean (по умолчанию "false")  - Флаг - заказ является заказом возврата
    @finished: boolean  - Флаг - заказ завершен
    @payAtExit: boolean (по умолчанию "false")  - Флаг - заказ закрыт на оплату на выходе
    @visitPayOrder: boolean (по умолчанию "false")  - Флаг - заказ является расчетным заказом по визиту
    @rkFriendsAnchor: normalizedString  - Якорь в Friends (идентификатор заявки)
  <Station> [refItem]  - Станция, на которой нужно распечатать накладную
  <Maket>? [refItem]  - Представление документа для накладной
  <HolderXML> [anyType]  - Информация о клиенте (xml из CRM)
  @CMD: string = "DeliveryPrintInvoice"
  @lockguid: normalizedString (по умолчанию "")  - Токен блокировки (идентификатор сессии блокировки). С версии 7.6.4.006. При блокировке заказа использовать указанный токен. Если заказ был заблокирован, то проверить токен блокировки, выдавать ошибку если заказ был заблокирован при помощи другого токена
  @preview: boolean (по умолчанию "true")  - Флаг - выполнить preview накладной
  @print: boolean (по умолчанию "true")  - Флаг - выполнить печать накладной
  @estimatedTime: dateTime  - Ожидаемое время доставки
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Invoice>  - Информация о накладной
  @num: string  - Номер накладной
```

## Пример: DeliveryPrintInvoice

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="DeliveryPrintInvoice" preview="1" print="0">
    <Order guid="{{deliveryGuid}}"/>
    <Station id="{{stationId}}"/>
    <HolderXML>
      <holder>
        <Holders_Addresses/>
      </holder>
    </HolderXML>
  </RK7CMD>
</RK7Query>
```
