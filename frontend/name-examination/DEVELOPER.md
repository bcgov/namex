# Developer Documentation

## Table of Contents

- [VS Code Environment Setup](#vs-code-environment-setup)
- [Project Structure and Organization](#project-structure-and-organization)
  - [`utils`](#utils)
  - [`types`](#types)
  - [`store`](#store)
  - [`composables`](#composables)
  - [`components`](#components)
- [Coding Guide](#coding-guide)

## VS Code Environment Setup

After following the setup instructions in the [README](./README.md#setup), you should have a local dev server up and running.

The following exensions are recommended:

- [Vue](https://marketplace.visualstudio.com/items?itemName=Vue.volar)
- [Tailwind CSS IntelliSense](https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss)
- [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
- [Goto definition alias](https://marketplace.visualstudio.com/items?itemName=antfu.goto-alias) - allows you to control click a component and go to its file

You can create a basic chrome launch configuration in VS Code to open a browser window for debugging.

## Project Structure and Organization

Let's go over some of the top-level folders in the project.

### `utils`

This folder contains util functions that are used throughout the project. If you are creating a generic helper function that isn't super specific to the component you are working on, please consider moving it to the utils folder if it doesn't already exist.

Some useful util files:

- `date.ts` - Contains utils for parsing and formatting dates from the NameX API and displaying it consistently across the UI.
- `emitter.ts` - Contains the global event bus for emitting events that other places in the code can listen for. For example, you can emit an error event anywhere in the codebase to show an error dialog to the user.
- `index.ts` - Contains some random util functions that aren't (but probably should be) organized. There are functions for validating NR and corp numbers here.
- `namex-api.ts` - Probably the most important util file. Contains functions for interacting with the NameX API. If you need to interact with the API in any way, use one of the functions in here, or create one here if it doesn't exist.

Please check this folder first before creating a generic helper function.

### `types`

This folder contains the TypeScript interfaces for the entire project. If you need to create a new interface/type, please put it in here.

### `store`

This folder contains the Pinia stores used in the project, and it's where a lot of the heavy-lifting logic resides.

`store/examine/index.ts` is where the main logic for the examine store resides. It relies on some other stores, two of which are:

- `conflict-data.ts` - contains functions for retrieving detailed information about a conflict.
- `conflicts.ts` - manages all conflicts for a particular name, and keeps track of which conflicts the user has selected for their decision or to compare in the 'Compare' tab. It does _not_ store detailed information about each conflict, but rather a small snapshot (`ConflictListItem`)

### `composables`

Contains reusable logic that can be used across the project. Of note:

- `mnemonic.ts` - Contains logic for registering a _mnemonic_. A mnemonic is a keyboard shortcut that consists of a modifier key (alt on Windows) plus a letter, which then triggers an action in the application. In the UI, mnemonic letters are shown underlined.

### `components`

This folder contains all of the Vue components.
Nuxt uses the path of the component file to form the name of the component when using it. For example, `components/app_header/NavLink.vue` would be referred to as `AppHeaderNavLink` in code.

Some folders to highlight:

- `examine/recipe/` - this folder contains components for the _recipe area_ of the Examine page. The recipe area is the place where all the conflicts, conditions, trademarks, and history can be browsed. It's also where the user can select conflicts for their decision.
- `examine/request_info/` - this folder contains components for the _request info_ section of the Examine page, which are the 5 cells near the top of the Examine page that contain information about the NR currently being examined.

If a component is generic enough that it can be used anywhere in the application (e.g. a button), then it can go directly under the `components` folder.

## Coding Guide

Here are some guidelines for contributing to the codebase:

- Use inline Tailwind utility classes for styling as much as possible
- Keep Vue files in the `pages` folder light on logic, refer to components in the `components` folder as much as possible
- Break up Vue components when you can and keep them relatively small
- Use Vue 3's Composition API for all Vue components
- Use Setup syntax when creating new Pinia stores
- Use TypeScript instead of JavaScript
- Format your code with Prettier before committing it
