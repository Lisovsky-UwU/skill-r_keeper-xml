# GetDataListInfo

[Кассовый сервер] Информация об очереди отправки данных

Схемы: `schemas/qryGetDataListInfo.xsd`, `schemas/resGetDataListInfo.xsd`
Влияние: только чтение

## Запрос

Обозначения: `!` обязательный атрибут, `?` необязательный элемент, `*` 0..n, `+` 1..n.

```
<RK7CMD>
  @CMD: string = "GetDataListInfo"
```

## Ответ

Помимо общих атрибутов RK7QueryResult (см. protocol.md):

```
<File>* [FileItem]  - Список файлов смен из папки ForSend
  @name: normalizedString  - Имя файла
  @size: int  - Размер файла
<ConnectStatus>  - Информация о наличии связи с сервером верхнего уровня
  @servername: normalizedString  - Имя сервера
  @connected: boolean  - Есть ли связь с сервером верхнего уровня
```

## Пример: GetDataListInfo

```xml
<?xml version="1.0" encoding="utf-8"?>
<RK7Query>
  <RK7CMD CMD="GetDataListInfo"/>
</RK7Query>
```
