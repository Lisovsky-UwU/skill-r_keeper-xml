# DeleteModifierFromStopList

[Кассовый сервер] Удалить модификатор из стоп-листа

Схемы: `schemas/qryDeleteModifierFromStopList.xsd`, `schemas/resDeleteModifierFromStopList.xsd`
Влияние: изменяет данные

## Практика

- <Modifier> можно повторять - несколько модификаторов за один запрос (проверено).

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Modifier>+ [refItem]  - Модификатор, удаляемый из стоп-листа
  @CMD: string = "DeleteModifierFromStopList"
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

## Пример: DeleteModifierFromStopList

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="DeleteModifierFromStopList">
    <Modifier id="{{modifierId}}"/>
  <Modifier id="{{modifierId2}}"/>
  </RK7CMD>
</RK7Query>
```
