# KDSSetDishData2

[Кассовый сервер] Изменить статус готовности у блюда (КДС)

Схемы: `schemas/qryKDSSetDishData2.xsd`, `schemas/resKDSSetDishData2.xsd`
Влияние: изменяет данные

## Практика

- Работает и для нераспечатанных блюд; line_guid - из GetOrder.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Employee>? [refItem]  - Работник, который изменяет статус
  @CMD: string = "KDSSetDishData2"
  @line_guid!: normalizedString  - GUID строки блюда
  @kdsstate!: KDSStateType {"" | sent | started | ready | taken | collect | collected | startpark | endpark | removed}  - Новый статус блюда
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

## Пример: KDSSetDishData2

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="KDSSetDishData2" line_guid="{{dishLineGuid}}" kdsstate="started">
    <Employee id="{{waiterId}}"/>
  </RK7CMD>
</RK7Query>
```
