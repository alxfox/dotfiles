# Dotfiles

Portable configuration managed by [chezmoi](https://www.chezmoi.io/). The repository contains configuration only. It installs no software.

## New machine

Install chezmoi, clone this repository, answer the prompts, and apply:

```sh
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply git@github.com:alxfox/dotfiles.git
```

If SSH is not configured yet, use the HTTPS repository URL instead.

The initialization prompt asks for the Git identity and stores it in `~/.config/chezmoi/chezmoi.toml`, which is not committed. To change the answers later, run `chezmoi init --prompt`, inspect with `chezmoi diff`, then run `chezmoi apply`.

The first apply prints optional install commands for zsh, Oh My Zsh, Powerlevel10k, Claude Code, and Codex. Run the ones the machine needs. Print them again with:

```sh
sh "$(chezmoi source-path)/run_once_after_99-print-install-commands.sh"
```

## Daily workflow

```sh
chezmoi update       # pull and apply changes
chezmoi diff         # preview local changes
chezmoi add ~/.file  # add or refresh a shared file
chezmoi edit ~/.file # edit source and apply it
chezmoi cd           # open the source repository
```

Run `chezmoi apply --dry-run --verbose` before applying a large change.

## Shared and machine-local files

| Local entry point | Managed shared configuration | Local contents |
| --- | --- | --- |
| `~/.zshrc` | `~/.zshrc.remote`, `~/.zsh_aliases` | Tool initialization, installer additions, interactive overrides |
| `~/.zprofile` | `~/.zprofile.remote` | PATH entries, tool environment, secrets |
| `~/.gitconfig` | `~/.config/git/config`, `~/.config/git/ignore` | Identity, signing, credential helpers, local overrides |
| `~/.ssh/config.local` | `~/.ssh/config` | Machine-local hosts and overrides |

Chezmoi creates the local entry points only when absent and never updates them afterwards. Edit shared files with `chezmoi edit`. Edit local entry points directly and do not import them with `chezmoi add` or `chezmoi re-add`.

- **zsh**: `~/.zshrc` and `~/.zprofile` source their `.remote` file on the first line. Oh My Zsh and Powerlevel10k are used when installed, plain zsh otherwise. Generate the local prompt config with `p10k configure`.
- **Git**: Git reads `~/.config/git/config` before `~/.gitconfig`, so local settings win without an include. The Git identity is seeded from the initialization answers; later changes, including `git config --global`, go to `~/.gitconfig`.
- **SSH**: `~/.ssh/config` includes `~/.ssh/config.local` first. SSH uses the first value found for each option, so local settings win. Keys are not managed.

> [!WARNING]
> Chezmoi does not create an entry point that already exists. If an installer creates `~/.zshrc` or `~/.zprofile` before the first apply, add the `source "$HOME/.zshrc.remote"` or `source "$HOME/.zprofile.remote"` line at the top manually.

The tmux configuration keeps the default prefix and keybindings, adding mouse support, a larger history, and `Prefix-R` to reload the file.

Claude Code and Codex share the same global working conventions. Codex reads a symlink at `~/.codex/AGENTS.md` pointing to `~/.claude/CLAUDE.md`.

## Secrets

Keep secrets out of this repository. `~/.secrets` is sourced from `~/.zprofile` when present, and chezmoi enforces owner-only permissions without managing its contents. A password manager integration is preferable for values that need to be shared.

## Upgrading from the `.gitconfig.remote` layout

Machines set up before the move to `~/.config/git/config` have `[include] path = ~/.gitconfig.remote` in `~/.gitconfig`. `chezmoi apply` deletes `~/.gitconfig.remote` (listed in `.chezmoiremove`); Git ignores the missing include. Remove the `[include]` block from `~/.gitconfig` by hand.

Earlier versions also cloned `~/.oh-my-zsh` and `~/.tmux/plugins/tpm`. These directories are no longer managed and can be kept or deleted.
