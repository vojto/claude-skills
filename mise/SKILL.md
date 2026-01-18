---
name: mise
description: Use mise for managing programming language versions. Use when starting a new project, setting up a development environment, installing Ruby/Python/Node/Go/Java/Rust or other languages, or when the user needs to configure language versions.
---

## mise - Universal Version Manager

We use [mise](https://mise.jdx.dev/) to manage programming language versions across all projects. mise replaces tools like rbenv, pyenv, nvm, etc. with a single unified tool.

### Setting Up a New Project

When starting a new project or working with a language for the first time:

1. **Check if mise is installed:**
   ```bash
   mise --version
   ```

2. **Install the language runtime:**
   ```bash
   mise use node@22      # Node.js
   mise use python@3.12  # Python
   mise use ruby@3.3     # Ruby
   mise use go@1.22      # Go
   mise use java@21      # Java
   mise use rust@latest  # Rust
   ```

   This creates a `.mise.toml` file in the project root with the version pinned.

3. **For existing projects**, if there's already a `.mise.toml`, `.tool-versions`, `.nvmrc`, `.ruby-version`, or `.python-version` file, just run:
   ```bash
   mise install
   ```

### Common Commands

```bash
mise install          # Install all tools defined in config
mise use <tool>@<v>   # Add/update tool version in project
mise ls               # List installed versions
mise ls-remote <tool> # List available versions for a tool
mise current          # Show currently active versions
mise prune            # Remove unused versions
```

### Project Configuration

mise uses `.mise.toml` as the config file. Example:

```toml
[tools]
node = "22"
python = "3.12"
ruby = "3.3"

[env]
NODE_ENV = "development"
```

### Installing mise

If mise is not installed:

```bash
# macOS
brew install mise

# Add to shell (one of these)
echo 'eval "$(mise activate bash)"' >> ~/.bashrc
echo 'eval "$(mise activate zsh)"' >> ~/.zshrc
echo 'mise activate fish | source' >> ~/.config/fish/config.fish
```

Then restart the shell or run `source ~/.zshrc` (or equivalent).
