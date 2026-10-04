# CheckPassword

[Кассовый сервер]: Проверка коректности пароля Для работы запроса требуется лицензия на xml. После ошибки проверки пароля, следующий запрос проверки пароля будет обработан только через секунду (защита от brutforce).

Схемы: `schemas/qryCheckPassword.xsd`, `schemas/resCheckPassword.xsd`
Влияние: только чтение

## Практика

- Пароль шифруется: XOR с ключом base64(<id работника строкой>), результат в base64. Готовое значение: `python scripts/rk7.py --crypt-password <id> <пароль>` (проверено на сервере).
- Неверный пароль - "Неправильный код пользователя или пароль" (RK7ErrorN 2102); следующая проверка возможна только через секунду.

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  <Employee> [refItem]  - Работник
  @password!: normalizedString  - Пароль (в зашифрованном виде). Алгоритм шифрования пароля: Пароль шифруется XOR шифрованием с ключом, результат переводится в base64. Ключ рассчитывается по формуле: идентификатор работника (EmpID) переводится в десятичный формат, полученная строка преобразуется в base64. Key = base64 (EmpID.toStri…
  @CMD: string = "CheckPassword"
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

## Пример: CheckPassword

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="CheckPassword" password="{{cryptedPassword}}">
    <Employee id="{{employeeId}}"/>
  </RK7CMD>
</RK7Query>
```
