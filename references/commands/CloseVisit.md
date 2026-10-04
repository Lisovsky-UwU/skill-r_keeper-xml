# CloseVisit

Закрыть визит

Схемы: `schemas/qryCloseVisit.xsd`, `schemas/resCloseVisit.xsd`
Влияние: изменяет данные

## Практика

- Работает и для пустого визита из CreateVisit, и для визита, все заказы которого закрыты.
- Не проходит, пока любой заказ визита заблокирован, в том числе удаленный: "Визит ... не может быть завершён. Заказ ... заблокирован станцией" (RK7ErrorN 2129).

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Order> [orderElement]  - Заказ. Визит этого заказа нужно закрыть
  <Station>? [refItem]  - Станция, на которой будут распечатаны документы
  @CMD: string = "CloseVisit"
  @VisitID: positiveInteger  - ID визита. Используется, если не заполнен тэг Order
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

## Пример: CloseVisit

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="CloseVisit" VisitID="{{visitId}}"/>
</RK7Query>
```
