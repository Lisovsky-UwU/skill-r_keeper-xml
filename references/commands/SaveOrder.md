# SaveOrder

[Кассовый сервер, Касса] Запись содержимого заказа в базу

Схемы: `schemas/qrySaveOrder.xsd`, `schemas/resSaveOrder.xsd`
Влияние: изменяет данные

## Практика

- Нужна лицензия XML SaveOrder - проверяется запросом CheckLicense license="XMLSaveOrder".
- quantity - в тысячных (1000 = 1 шт), price - в копейках; без price берется цена из прайса.
- Session без uni добавляет новый пакет; с uni перезаписывает существующий нераспечатанный пакет.
- Скидка (<Discount>) и предоплата (<Prepay>) добавляются в заказ так же - внутри <Session>.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <LicenseInfo>? [LicenseInfoItem]  - Информация о лицензии, необходимой для выполнения запроса
    <LicenseInstance> [LicenseInstanceItem]
      @guid!: guidString  - Генерируется клиентом один раз при инсталляции или первом запуске приложения/инстанса как настоящий уникальный GUID и сохраняется. Количество разных значений в течении суток ограничено и связано с количеством подключений в лицензии.
      @seqNumber: nonNegativeInteger  - При первом вызове для конкретного guid должно быть 0, в дальнейшем каждый следующий вызов на 1 больше, можно повторить идентичный запрос (с там же seqNumber), ответ может кэшироваться RK7 (заново не обязан вычисляться)
    @anchor: normalizedString  - формат якоря: 6:_ProductGUID_#_RestCode_/17, где _ProductGUID_ - GUID продукта, сообщается UCS, _RestCode_ - 9-значный код ресторана
    @licenseToken: normalizedString  - Токен лицензии запрашивается у системы лицензирования, инструкции по обращению к системе лицензирования за токеном лицензии сообщаются UCS вместе с GUID продукта
  <Order> [orderElement]  - Заказ
  <LockStation>? [refItem]  - Станция, от имени которой будет заблокирован заказ
  <Session>+ [SessionItem]  - Пакет
    @uni: int  - UNI пакета. Если задан, то перезаписывается содержимое пакета. Иначе создается новый пакет
    @line_guid: guidString  - GUID пакета
    @isDraft: boolean  - Флаг "Пакет является черновиком"
    @printed: boolean  - Флаг - пакет распечатан
    @printTime: dateTime  - Время первой сервис-печати. Если не задано, то используется время remindAt
    @remindTime: dateTime  - Время начала готовки блюд пакета. Если не задано, то используется текущее время
    @readyTime: dateTime  - Время, к которому должны быть приготовлены все блюда пакета
    @startService: dateTime  - Время, в которое блюда были добавлены в заказ. Если не задано, то используется время printAt
    @* - допускаются любые другие атрибуты
    <Station>? [refItem]  - Станция, на которой пакет был добавлен
    <Author>? [refItem]  - Работник, последний редактировавший заказ
    <Creator>? [refItem]  - Работник, создавший пакет
    <Course>? [refItem]  - Порядок подачи
    (одно из - повторяется:)
      <Dish> [dishItem]  - Блюдо
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
            @price: int  - Цена модификатора (в копейках)
            @count: positiveInteger (по умолчанию "1")  - Количество модификаторов
            @openName: normalizedString  - Произвольное имя модификатора
            @isDefault: boolean (по умолчанию "1")  - Флаг - модификатор по умолчанию
          <Discount> [discountItem]  - Скидка
            (refItem: id | code | guid)
            @uni: nonNegativeInteger  - UNI элемента. Если задан, то элемент обновляется, иначе создается новый. Только для нераспечатанных элементов
            @line_guid: guidString  - GUID строки
            @state: CheckItemState {1 | 3 | 4 | 5 | 6 | 7}  - Статус элемента (с версии 7.5.4.206)
            @* - допускаются любые другие атрибуты
            <Interface>? [refItem]  - Интерфейс к карте гостя. Обезателен для заполнения, если задан cardCode
            <BonusType>? [refItem]  - Тип бонуса, заполняется для скидок ПДС
            @amount: int  - Сумма скидки (в копейках), для скидок с ручным вводом суммы скидки
            @maxamount: int  - Максимальная сумма скидки (в копейках)
            @seat: nonNegativeInteger (по умолчанию "0")  - Номер посадочного места: 0 - не задано
            @cardCode: normalizedString  - Код карточки
            @deleted: boolean  - Признак того что скидка удалена
            @charge_dish_line_guid: guidString (по умолчанию "")  - GUID-блюда нераспределяемой наценки (для нераспределяемых наценок). Начиная с 7.6.0.101
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
        @quantity!: int  - Количество блюда (в тысячных долях), для добавляемых блюд. Если кол-во меньше нуля, то это блюдо выкупа, иначе обычная продажа
        @srcQuantity: int  - Количество блюда, без учета отказов (в тысячных долях, с 7.4.16.2)
        @seat: nonNegativeInteger (по умолчанию "0")  - Номер посадочного места: 0 - не задано
      <Combo> [comboItem]  - Комбо блюдо
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
        @quantity!: int  - Количество блюда (в тысячных долях), для добавляемых блюд. Если кол-во меньше нуля, то это блюдо выкупа, иначе обычная продажа
        @srcQuantity: int  - Количество блюда, без учета отказов (в тысячных долях, с 7.4.16.2)
        @seat: nonNegativeInteger (по умолчанию "0")  - Номер посадочного места: 0 - не задано
        <Modi> [запрещен] [modiItem] (структура - см. выше)
        <Component>* [comboComponent]  - Комбо компонент
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
      <Discount> [discountItem]  - Скидка (структура - см. выше)
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
        @TransactionStatus: TransactionStatusType {1 | 3 | 4 | 5 | 6}  - Статус авторизации. Начиная с версии 7.5.4.211
        @seat: nonNegativeInteger (по умолчанию "0")  - Номер посадочного места: 0 - не задано
        @discount_line_guid: guidString (по умолчанию "")  - GUID-связанной с оплатой скидкой (для оплат как скидка). Начиная с 7.6.0.087
        @deleted: boolean  - Признак того что платеж удален
        @owner: normalizedString (по умолчанию "")  - Владелец валюты (VISA, Master card). С версии 7.06.04.430+, 7.06.05.296+
        @authtype: AuthType {"" | error | auto | voice | terminal | voicepossible} (по умолчанию "auto")  - Тип авторизации. С версии 7.06.04.430+, 7.06.05.296+
        @authcode: normalizedString (по умолчанию "")  - Код авторизации. С версии 7.06.04.430+, 7.06.05.296+
        @extIntegerInfo: int (по умолчанию "0")  - Номер банковского терминала. С версии 7.06.04.430+, 7.06.05.296+
        @transactionNumber: int (по умолчанию "0")  - Номер транзакции. С версии 7.06.04.430+, 7.06.05.296+
        <Reason>? [refItem]  - Причина внесения предоплаты
        @promised: boolean  - Предоплата является обещанным платежом
    @fixedPrice: boolean  - Флаг "Зафиксировать цены"
  @CMD: string = "SaveOrder"
  @dontcheckLicense: boolean  - Флаг "Не проверять лицензию xml-сохранение заказа". Такие заказы не видны на кассе"
  @deferred: boolean (по умолчанию "false")  - Флаг - неподтвержденный заказ. Для превращения в обычный заказ потребуется пересохранить заказ с кассы.
  @sendtovdu: boolean (по умолчанию "true")  - Флаг "Отправить заказ на VDU". Если включен, то заказ будет передан на VDU, иначе не будет. Версия 7.5.8.065+
  @lockguid: normalizedString  - Токен блокировки (идентификатор сессии блокировки). С версии 7.6.4.005
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Error>* [ErrorItem]  - Информация об ошибке
  <FaultyTag>  - Сбойный тэг
    <любой XML>
  @RK7ErrorN!: positiveInteger  - Код ошибки RK7
  @ErrorText!: normalizedString  - Текст ошибки
<Order> [resOrderItemExt]  - Заказ
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
      @guestLabel!: token  - Текстовая метка гостя
      @cardCode: normalizedString  - Код карты гостя
      @clientID: long  - ID адреса гостя
      @addressID: long  - ID адреса гостя
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
    @uni: int  - UNI пакета. Если задан, то перезаписывается содержимое пакета. Иначе создается новый пакет
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
            @price: int  - Цена модификатора (в копейках)
            @count: positiveInteger (по умолчанию "1")  - Количество модификаторов
            @openName: normalizedString  - Произвольное имя модификатора
            @isDefault: boolean (по умолчанию "1")  - Флаг - модификатор по умолчанию
          <Discount> [discountItem]  - Скидка
            (refItem: id | code | guid)
            @uni: nonNegativeInteger  - UNI элемента. Если задан, то элемент обновляется, иначе создается новый. Только для нераспечатанных элементов
            @line_guid: guidString  - GUID строки
            @state: CheckItemState {1 | 3 | 4 | 5 | 6 | 7}  - Статус элемента (с версии 7.5.4.206)
            @* - допускаются любые другие атрибуты
            <Interface>? [refItem]  - Интерфейс к карте гостя. Обезателен для заполнения, если задан cardCode
            <BonusType>? [refItem]  - Тип бонуса, заполняется для скидок ПДС
            @amount: int  - Сумма скидки (в копейках), для скидок с ручным вводом суммы скидки
            @maxamount: int  - Максимальная сумма скидки (в копейках)
            @seat: nonNegativeInteger (по умолчанию "0")  - Номер посадочного места: 0 - не задано
            @cardCode: normalizedString  - Код карточки
            @deleted: boolean  - Признак того что скидка удалена
            @charge_dish_line_guid: guidString (по умолчанию "")  - GUID-блюда нераспределяемой наценки (для нераспределяемых наценок). Начиная с 7.6.0.101
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
        @quantity!: int  - Количество блюда (в тысячных долях), для добавляемых блюд. Если кол-во меньше нуля, то это блюдо выкупа, иначе обычная продажа
        @srcQuantity: int  - Количество блюда, без учета отказов (в тысячных долях, с 7.4.16.2)
        @seat: nonNegativeInteger (по умолчанию "0")  - Номер посадочного места: 0 - не задано
        @amount: int  - Сумма блюда (в копейках)
        @kdsstate: KDSStateType {"" | sent | started | ready | taken | collect | collected | startpark | endpark | removed} (по умолчанию "")  - КДС статус блюда (с версии 7.5.5.037)
        @new: boolean (по умолчанию "false")  - Флаг - новое блюдо (последний добавленный элемент)
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
        @quantity!: int  - Количество блюда (в тысячных долях), для добавляемых блюд. Если кол-во меньше нуля, то это блюдо выкупа, иначе обычная продажа
        @srcQuantity: int  - Количество блюда, без учета отказов (в тысячных долях, с 7.4.16.2)
        @seat: nonNegativeInteger (по умолчанию "0")  - Номер посадочного места: 0 - не задано
        <Modi> [запрещен] [modiItem] (структура - см. выше)
        <Component>* [comboComponent]  - Комбо компонент
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
        @kdsstate: KDSStateType {"" | sent | started | ready | taken | collect | collected | startpark | endpark | removed} (по умолчанию "")  - КДС статус блюда (с версии 7.5.5.037)
        @amount: int  - Сумма блюда (в копейках)
        @new: boolean  - Флаг - новое блюдо (последний добавленный элемент)
      <Discount> [discountItem]  - Скидка (структура - см. выше)
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
        @TransactionStatus: TransactionStatusType {1 | 3 | 4 | 5 | 6}  - Статус авторизации. Начиная с версии 7.5.4.211
        @seat: nonNegativeInteger (по умолчанию "0")  - Номер посадочного места: 0 - не задано
        @discount_line_guid: guidString (по умолчанию "")  - GUID-связанной с оплатой скидкой (для оплат как скидка). Начиная с 7.6.0.087
        @deleted: boolean  - Признак того что платеж удален
        @owner: normalizedString (по умолчанию "")  - Владелец валюты (VISA, Master card). С версии 7.06.04.430+, 7.06.05.296+
        @authtype: AuthType {"" | error | auto | voice | terminal | voicepossible} (по умолчанию "auto")  - Тип авторизации. С версии 7.06.04.430+, 7.06.05.296+
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
        @TransactionStatus: TransactionStatusType {1 | 3 | 4 | 5 | 6}  - Статус авторизации. Начиная с версии 7.5.4.211
        @seat: nonNegativeInteger (по умолчанию "0")  - Номер посадочного места: 0 - не задано
        @discount_line_guid: guidString (по умолчанию "")  - GUID-связанной с оплатой скидкой (для оплат как скидка). Начиная с 7.6.0.087
        @deleted: boolean  - Признак того что платеж удален
        @owner: normalizedString (по умолчанию "")  - Владелец валюты (VISA, Master card). С версии 7.06.04.430+, 7.06.05.296+
        @authtype: AuthType {"" | error | auto | voice | terminal | voicepossible} (по умолчанию "auto")  - Тип авторизации. С версии 7.06.04.430+, 7.06.05.296+
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
    <PriceScale> [resRefItem]  - Тип цены, используемый для содержимого пакета
    <TradeGroup> [resRefItem]  - Торговая группа
    @cookMins!: nonNegativeInteger  - Время приготовления (минуты)
    @sessionID: int  - UNI пакета
  @visit: positiveInteger
  @orderIdent: positiveInteger
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
  @basicSum: positiveInteger  - Сумма к оплате в базовой валюте (в копейках)
  @nationalSum: positiveInteger  - Сумма к оплате в национальной валюте (в копейках)
<Session>* [NewSessionItem]  - Добавленный пакет
  @line_guid: normalizedString  - GUID пакета
  @sessionID!: positiveInteger  - ID пакета
```

## Пример: SaveOrder

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="SaveOrder">
    <Order guid="{{orderGuid}}"/>
    <Session>
      <Station id="{{stationId}}"/>
      <Dish id="{{dishId}}" quantity="1000"/>
      <Dish id="{{dishId}}" quantity="2000" price="{{dishPrice}}"/>
    </Session>
  </RK7CMD>
</RK7Query>
```

## Пример: SaveOrder - Скидка на заказ

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="SaveOrder">
    <Order guid="{{orderGuid}}"/>
    <Session>
      <Station id="{{stationId}}"/>
      <Discount id="{{discountId}}"/>
    </Session>
  </RK7CMD>
</RK7Query>
```

## Пример: SaveOrder - Предоплата

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="SaveOrder">
    <Order guid="{{orderGuid}}"/>
    <Session>
      <Station id="{{stationId}}"/>
      <Prepay id="{{currencyId}}" amount="10000"/>
    </Session>
  </RK7CMD>
</RK7Query>
```
