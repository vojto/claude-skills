# Sentry for iOS/Swift

## 1. Add SDK

Via SPM: `https://github.com/getsentry/sentry-cocoa`

## 2. Initialize

In `AppDelegate.swift`:

```swift
import Sentry

SentrySDK.start { options in
    options.dsn = "https://KEY@ORG.ingest.us.sentry.io/PROJECT_ID"
}
```

DSN location: Settings → Projects → Client Keys (DSN)

## 3. Fastlane dSYM Upload

Install sentry-cli:
```bash
brew install sentry-cli
```

Add to `Pluginfile`:
```ruby
gem 'fastlane-plugin-sentry'
```

Add to `Fastfile` config section:
```ruby
SENTRY_ORG = "your-org-slug"
SENTRY_PROJECT = "your-project-slug"
```

Add to release lane after `gym`, before `pilot`:
```ruby
sentry_debug_files_upload(
  org_slug: SENTRY_ORG,
  project_slug: SENTRY_PROJECT,
  path: lane_context[SharedValues::DSYM_OUTPUT_PATH]
)
```

## 4. Auth Token

Create `ios/.sentryclirc` (gitignored):
```ini
[auth]
token=sntrys_YOUR_TOKEN
```

Or set `SENTRY_AUTH_TOKEN` env var.

Generate at: Settings → Auth Tokens (needs `project:releases`, `org:read` scopes)

## 5. Verify

Check uploaded dSYMs: Settings → Projects → Debug Files
