# XSD-схемы r_keeper

Схемы XML-интерфейса принадлежат UCS и в репозиторий не входят. Скилл работает и без них:
справочник `references/commands/` уже сгенерирован и лежит в репозитории.

Схемы нужны, чтобы:
- перегенерировать справочник под свою версию r_keeper (`scripts/xsd_to_reference.py`);
- агенту было где свериться с первоисточником, когда в справочнике чего-то не хватает.

## Откуда взять

XSD поставляются UCS вместе с документацией по XML-интерфейсу r_keeper 7 - у дилера, в партнерских
материалах UCS или в дистрибутиве r_keeper.

## Как положить

Скопируйте набор в эту папку как есть, с подпапками:

```
schemas/
  common.xsd, messages.xsd, unifr.xsd, ...   общие типы
  qry<Команда>.xsd, res<Команда>.xsd         запрос и ответ каждой команды
  Delivery/qryDelivery*.xsd, resDelivery*.xsd
  Hidden/...
```

Затем из корня скилла:

```bash
python scripts/xsd_to_reference.py schemas .
```

Генератор перепишет `references/commands/` и `references/commands.md`. Ручные заметки и примеры
он берет из `references/command_notes.json`, так что они не потеряются.
