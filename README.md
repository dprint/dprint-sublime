# dprint - Sublime Text Plugin

Sublime Text formatting extension for [dprint](https://dprint.dev)—a pluggable and configurable formatting platform.

## Setup

1. Install [dprint's CLI](https://dprint.dev/install).
2. Install Sublime Text plugin via [Package Control](https://packagecontrol.io/packages/dprint)
3. Run `dprint init` in the root directory of your repository to create a `dprint.config.json` file.

## Features

Formats code in the editor using [dprint](https://dprint.dev).

Plugins are currently resolved based on the `dprint.config.json` found based on the current file (in any ancestor directory or ancestor `config` sub directory).

## Commands

* `dprint_fmt` - Formats the code being edited.
