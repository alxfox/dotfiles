#!/bin/sh
# Prints optional install commands. Nothing is installed.
cat <<'COMMANDS'

Optional install commands (run as needed):

  # zsh, then make it the login shell
  sudo apt-get install -y zsh          # or: brew install zsh / sudo pacman -S zsh
  chsh -s "$(command -v zsh)"

  # Oh My Zsh (keeps the existing ~/.zshrc)
  KEEP_ZSHRC=yes sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

  # Powerlevel10k theme for Oh My Zsh, then: p10k configure
  git clone --depth=1 https://github.com/romkatv/powerlevel10k.git "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k"

  # TPM for tmux session restore, then press Prefix-I inside tmux
  git clone --depth=1 https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

  # Claude Code
  curl -fsSL https://claude.ai/install.sh | bash

  # Codex (requires Node.js and npm)
  npm install -g @openai/codex

Print again: install-hints

COMMANDS
