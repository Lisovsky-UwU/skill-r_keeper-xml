# XSD-схемы r_keeper

Актуальный набор схем XML-интерфейса r_keeper 7 от UCS (версия 7.26, скачан 2026-10-04), без
изменений. Права на схемы принадлежат UCS, лицензия Apache этого репозитория на них не
распространяется (см. `NOTICE`).

```
schemas/
  common.xsd, messages.xsd, unifr.xsd, ...   общие типы
  qry<Команда>.xsd, res<Команда>.xsd         запрос и ответ каждой команды
  Delivery/                                  доставка
  Hidden/                                    из предыдущего набора (см. ниже)
```

`Hidden/` - схемы CheckLicense и ChangeWorkUdb (команда ReloadWorkUdb). В актуальном наборе UCS их
убрала, но сервер 7.26.8 обе команды выполняет, поэтому схемы сохранены. Команды, которые UCS убрала
и которые сервер больше не выполняет (ExchangePriority, OpenLowAlcKeg), из репозитория удалены.

Известные огрехи набора (оставлены как есть, генератор их переживает):
- `qryAddBatchOfGoods.xsd` - атрибуты `Batch` записаны без `complexType`.
- `common.xsd` - тип `resLoyaltyInfo` описан не по правилам XSD (элемент прямо в `complexType`).
- `qryFindReceiptsForReturn.xsd` объявляет UTF-8, но сохранен в windows-1251.
- Ответ на `FarCardsAnyInfoXML` лежит в `resFarCardsAnyInfoXml.xsd` (другой регистр).
- Команда `CreaterkFriendsAnchor` описана в `qryCreateRkFriendsAnchor.xsd` (другое написание).
- `ITV_TITLE.xsd` - не команда XML-интерфейса; судя по полям (работник, станция, позиции чека),
  это формат титров для видеонаблюдения (интерфейсы ITV / UCS Видео).

## Обновление

Положите новый набор вместо этого, с той же структурой (схемы из `Hidden/` сохраните, если команды
еще работают), и выполните из корня скилла:

```bash
python scripts/xsd_to_reference.py schemas .
python scripts/check.py
```

Генератор перепишет `references/commands/` и `references/commands.md` и удалит страницы команд,
схем которых больше нет. Ручные заметки и примеры он берет из `references/command_notes.json`.
