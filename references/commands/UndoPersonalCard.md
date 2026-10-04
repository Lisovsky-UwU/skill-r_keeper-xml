# UndoPersonalCard

[Кассовый сервер] Отмена карты ПДС

Схемы: `schemas/qryUndoPersonalCard.xsd`, `schemas/resUndoPersonalCard.xsd`
Влияние: изменяет данные

## Практика

- Помечает скидку по карте удаленной (state=7, deleted="1") и отвязывает карту от гостя. Отвечает Ok и тогда, когда такая карта к заказу не применялась.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Interface>? [refItem]  - Интерфейс, обрабатывающий карточку
  <Order> [orderElement]  - Заказ
  <Cashier>? [refItem]  - Кассир, от имени которого отменяется карточка
  <LockStation>? [refItem]  - Станция, от имени которой будет заблокирован заказ. С версии 7.6.4.009.
  @CMD!: string = "UndoPersonalCard"
  @lockguid: normalizedString (по умолчанию "")  - Токен блокировки (идентификатор сессии блокировки). С версии 7.6.4.009. При блокировке заказа использовать указанный токен. Если заказ был заблокирован, то проверить токен блокировки, выдавать ошибку если заказ был заблокирован при помощи другого токена
  @cardCode!: normalizedString  - Код карточки
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

## Пример: UndoPersonalCard

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="UndoPersonalCard" cardCode="{{cardCode}}">
    <Interface id="{{pdsInterfaceId}}"/>
    <Order guid="{{orderGuid}}"/>
    <Cashier id="{{cashierId}}"/>
  </RK7CMD>
</RK7Query>
```
