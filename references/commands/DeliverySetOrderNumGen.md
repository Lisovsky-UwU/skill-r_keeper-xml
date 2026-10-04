# DeliverySetOrderNumGen

[Касса,Кассовый сервер] Доставка: изменение генератора для нумерации заказа

Схемы: `schemas/Delivery/qryDeliverySetOrderNumGen.xsd`, `schemas/Delivery/resDeliverySetOrderNumGen.xsd`
Влияние: **опасно** - необратимые или массовые изменения, блокировка кассы

## Практика

- Меняет нумерацию заказов доставки ресторана.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  @CMD: string = "DeliverySetOrderNumGen"
  @value!: nonNegativeInteger  - Новое значение генератора
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

## Пример: DeliverySetOrderNumGen

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="DeliverySetOrderNumGen" value="1"/>
</RK7Query>
```
