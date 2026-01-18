---
name: postmark
description: Send emails via Postmark API. Use when you need to send an email notification to the user.
---

## Configuration

- **From Email**: `axios@rinik.net`
- **User's Email**: `vojto@rinik.net` (use this when the user says "email me" or "send to myself")
- **API Key**: Stored in `~/.claude/.env` as `POSTMARK_API_KEY`

## Sending an Email

Source the env file and use curl to send emails via the Postmark API:

```bash
source ~/.claude/.env && curl "https://api.postmarkapp.com/email" \
  -X POST \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -H "X-Postmark-Server-Token: $POSTMARK_API_KEY" \
  -d '{
    "From": "axios@rinik.net",
    "To": "vojto@rinik.net",
    "Subject": "Your subject here",
    "TextBody": "Your plain text message here",
    "MessageStream": "outbound"
  }'
```

## Important Notes

- Always use `axios@rinik.net` as the From address
- When the user asks to "email me" or "send to myself", use `vojto@rinik.net`
- Always source `~/.claude/.env` before running curl to load the API key
- Use `TextBody` for plain text emails, or `HtmlBody` for HTML content
- A successful response returns HTTP 200 with a JSON object containing `MessageID`
