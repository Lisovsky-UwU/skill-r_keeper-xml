# VoidOrder

[Кассовый сервер] Удалить заказ

Схемы: `schemas/qryVoidOrder.xsd`, `schemas/resVoidOrder.xsd`
Влияние: **опасно** - необратимые или массовые изменения, блокировка кассы

## Практика

- DeleteReason - причина из ORDERVOIDS; для заказа с распечатанными блюдами нужна причина, разрешенная для удаления чека/блюд.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Order> [orderElement]  - Заказ
  <Station> [refItem]  - Станция
  <Manager> [refItem]  - Менеджер, удаляющий заказ
  <DeleteReason> [refItem]  - Причина удаления
  <FiscalDocInfo>? [poFiscalDocInfo]  - Информация о фискальном документе. Для использования в отчетах.
    <FiscDev>? [refItem]  - Тип фискального устройства. Указанное значение заносится в поле PrintChecks.FiscDev
    @PrintNumber!: nonNegativeInteger  - Печатный номер чека, в России номер чека ФН. Указанное значение заносится в поле PrintChecks.PrintNumber.
    @FiscDocNumber!: nonNegativeInteger  - Фискальный номер документа, в России номер документа ФН. Указанное значение заносится в поле PrintChecks.FiscDocNumber.
    @GlobalFiscalId: normalizedString  - Глобальный номер чека, в России не используется. Указанное значение заносится в поле PrintChecks.GlobalFiscalID.
    @ExtFiscID!: normalizedString  - Номер фискального регистратора. Указанное значение заносится в поле PrintChecks.ExtFiscID.
    @FiscShiftNum: positiveInteger  - Номер фискальной смены фискального регистратора. Указанное значение заносится в поле PrintChecks.iFiscShift.
  @CMD!: string = "VoidOrder"
  @lockguid: normalizedString (по умолчанию "")  - Токен блокировки (идентификатор сессии блокировки). С версии 7.6.4.006. При блокировке заказа использовать указанный токен. Если заказ был заблокирован, то проверить токен блокировки, выдавать ошибку если заказ был заблокирован при помощи другого токена
  @sendtovdu: boolean (по умолчанию "true")  - Флаг "Отправить заказ на VDU". Если включен, то заказ будет передан на VDU, иначе не будет. Версия 7.6.4.032+
  @change_guids: boolean (по умолчанию "true")  - Флаг "Изменить GUID элементов". Если включен, то у заказа и у всех элементов его состава будет изменен guid. Версия 7.6.5.189+
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

## Пример: VoidOrder

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="VoidOrder">
    <Order guid="{{orderGuid}}"/>
    <Station id="{{stationId}}"/>
    <Manager id="{{managerId}}"/>
    <DeleteReason id="{{deleteReasonId}}"/>
  </RK7CMD>
</RK7Query>
```
