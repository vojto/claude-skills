---
name: telegram
description: Send Telegram messages to the user. Use when you need to send a quick notification or alert.
---

## Configuration

- **User's Chat ID**: `1624852061` (use this when sending messages to the user)
- **Bot Token**: Stored in `~/.claude/.env` as `TELEGRAM_BOT_TOKEN`

## Sending a Message

Source the env file and use curl to send messages via the Telegram Bot API:

```bash
source ~/.claude/.env && curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
  -d "chat_id=1624852061" \
  -d "text=Your message here"
```

## Sending with Markdown Formatting

```bash
source ~/.claude/.env && curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
  -d "chat_id=1624852061" \
  -d "parse_mode=Markdown" \
  -d "text=*Bold* and _italic_ text"
```

## Important Notes

- Always use chat ID `1624852061` when the user asks to "message me" or "send me a telegram"
- Always source `~/.claude/.env` before running curl to load the bot token
- Use `parse_mode=Markdown` for formatted messages (supports *bold*, _italic_, `code`, [links](url))
- Use `parse_mode=HTML` for HTML formatting (<b>, <i>, <code>, <a>)
- A successful response returns JSON with `"ok": true`
