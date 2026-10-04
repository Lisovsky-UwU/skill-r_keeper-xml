# SendToVDU

[Кассовый сервер] Отправка блюд на VDU

Схемы: `schemas/qrySendToVDU.xsd`, `schemas/resSendToVDU.xsd`
Влияние: изменяет данные

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Order>? [orderElement]  - Заказ
  <Session>+ [SessionItem]  - Пакет
    @uni: nonNegativeInteger  - UNI пакета. Если задан, то перезаписывается содержимое пакета. Иначе создается новый пакет
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
        <OrderType> [refItem]  - Тип заказа на блюдо
        @quantity!: int  - Количество блюда (в тысячных долях), для добавляемых блюд. Если кол-во меньше нуля, то это блюдо выкупа, иначе обычная продажа
        @srcQuantity: int  - Количество блюда, без учета отказов (в тысячных долях, с 7.4.16.2)
        @seat: nonNegativeInteger (по умолчанию "0")  - Номер посадочного места: 0 - не задано
        @changeWeight: boolean (по умолчанию "0")  - Атрибут учитывается только для весовых блюд. Если в запросе передан тот же вес, что задан в заказе и в этом поле передано true, то будет считаться, что вес для блюда указан. Если же в запросе передан тот же вес, что задан в заказе и этот атрибут не передан (передано false), то будет считаться, что …
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
    @fixedPrice: boolean  - Флаг "Зафиксировать цены"
  @CMD: string = "SendToVDU"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Errors>? [ErrorStack]
  <Error>*  - Стэк ошибок, возникших при выполнени команды
    (текстовое содержимое: string)
    @RK7ErrorN!: positiveInteger  - Код ошибки RK7
    @Component!: errorArea {Printer | Authorization terminal | PDS | Rights}  - Компонент, в котором была сгенерирована ошибка
@ServerVersion!: normalizedString  - Версия кассовой программы
@XmlVersion!: positiveInteger  - Версия xml протокола
@NetName: token  - Сетевое имя программы (с 7.5.3.260)
@CMD: token  - Исходная xml-команда
@Status!: string {Ok | No changes | Execution Started | Query Parse Error | Bad Query Parameters | Query Executing Error | Result Writing Error}  - Статус выполнения запроса
@RK7ErrorN: positiveInteger  - Код ошибки RK7
@ErrorText!: normalizedString  - Текст ошибки
@WorkTime!: nonNegativeInteger  - Время обработки запроса (в миллисекундах)
@DateTime!: dateTime  - Дата и время генерации ответного xml (xmlver>=39)
@Processed!: nonNegativeInteger  - Количество обработанных команд
```

## Пример: SendToVDU

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="SendToVDU">
    <Order guid="{{orderGuid}}"/>
    <Session>
      <Dish id="{{dishId}}" quantity="1000"/>
    </Session>
  </RK7CMD>
</RK7Query>
```
