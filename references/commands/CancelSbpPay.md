# CancelSbpPay

[Кассовый сервер] Прервать оплату СБП, вызванную через xml интерфейс

Схемы: `schemas/qryCancelSbpPay.xsd`, `schemas/resCancelSbpPay.xsd`
Влияние: изменяет данные

## Практика

- Без активного СБП-платежа с таким sbpPayGuid - "СБП оплата с гуид ... не найдена".

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Payment>
    @sbpPayGuid: normalizedString  - Идентификатор СБП платежа, преданный при создании СБП платежа. Если поле не заполнено, то оно заполнится автоматически случайным гуидом
  @CMD: string = "CancelSbpPay"
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

## Пример: CancelSbpPay

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="CancelSbpPay">
    <Payment sbpPayGuid="{{sbpPayGuid}}"/>
  </RK7CMD>
</RK7Query>
```
