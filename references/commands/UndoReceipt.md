# UndoReceipt

Аннулирование чека

Схемы: `schemas/qryUndoReceipt.xsd`, `schemas/resUndoReceipt.xsd`
Влияние: **опасно** - необратимые или массовые изменения, блокировка кассы

## Практика

- DeleteReason - причина из ORDERVOIDS с флагом "При аннулировании чека" (ImplOnCheckUndo).
- Чек, по которому были возвраты (MakeReturnGoods), аннулировать нельзя.
- Заказ возвращается в редактирование; ManagerPassword - пароль менеджера.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Manager> [refItem]  - Кассир
  <Maket>? [refItem]  - Представление документа для аннулирования чека
  <DeleteReason>? [deleteReasonItem]  - Причина аннулирования чека
    (refItem: id | code | guid)
    @openName: normalizedString  - Произвольное имя для причины удаления. С версии 7.6.4.417
  @CMD: string = "UndoReceipt"
  @ReceiptNum!: positiveInteger  - Номер чека
  @ManagerPassword!: normalizedString  - Пароль менеджера
  @lockguid: guidString (по умолчанию "")  - Токен блокировки (идентификатор сессии блокировки). С версии 7.6.4.037. При блокировке заказа использовать указанный токен. Если заказ был заблокирован, то проверить токен блокировки, выдавать ошибку если заказ был заблокирован при помощи другого токена
  @sendtovdu: boolean (по умолчанию "true")  - Флаг "Отправить заказ на VDU". Если включен, то заказ будет передан на VDU, иначе не будет. Версия 7.7.0.024+
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<Errors>? [ErrorStack]
  <Error>*  - Стэк ошибок, возникших при выполнени команды
    (текстовое содержимое: string)
    @RK7ErrorN!: positiveInteger
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

## Пример: UndoReceipt

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="UndoReceipt" ReceiptNum="{{receiptNum}}" ManagerPassword="{{managerPassword}}">
    <Manager id="{{managerId}}"/>
    <DeleteReason id="{{checkUndoReasonId}}"/>
  </RK7CMD>
</RK7Query>
```
