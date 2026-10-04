# OpenSeat

[Кассовый сервер] Открыть закрытое посадочное место, начиная с версии 7.5.0.1

Схемы: `schemas/qryOpenSeat.xsd`, `schemas/resOpenSeat.xsd`
Влияние: изменяет данные

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Order> [orderElement]  - Заказ
  <LockStation>? [refItem]  - Станция, от имени которой будет заблокирован заказ. С версии 7.6.4.009.
  @CMD: string = "OpenSeat"
  @lockguid: guidString (по умолчанию "")  - Токен блокировки (идентификатор сессии блокировки). С версии 7.6.4.009. При блокировке заказа использовать указанный токен. Если заказ был заблокирован, то проверить токен блокировки, выдавать ошибку если заказ был заблокирован при помощи другого токена
  @seat!: positiveInteger  - Номер посадочного места
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

## Пример: OpenSeat

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="OpenSeat" seat="1">
    <Order guid="{{orderGuid}}"/>
  </RK7CMD>
</RK7Query>
```
