# TransKey

An iOS custom keyboard extension that translates text in place, in any app.

## Structure

- `TransKey/` — the container app (SwiftUI). Lets the user configure the translation API endpoint/key, pick a default target language, and links to Settings to enable the keyboard.
- `KeyboardExtension/` — the custom keyboard (UIKit `UIInputViewController`). Reads text from the active text field, sends it to the translation API, and inserts the result.
- `Shared/` — code shared by both targets: the translation service, app settings, and models. The app and the keyboard run in separate sandboxes and don't share storage (that needs the App Groups entitlement, which requires a paid Apple Developer account); instead, settings are moved over with a one-time clipboard handshake (`ClipboardSettingsTransfer`).
- `project.yml` — [XcodeGen](https://github.com/yonaskolb/XcodeGen) spec used to generate `TransKey.xcodeproj`.

## Requirements

- Xcode 15+, iOS 16.0 deployment target
- [XcodeGen](https://github.com/yonaskolb/XcodeGen) (`brew install xcodegen`) to (re)generate the `.xcodeproj` after editing `project.yml`

## Getting started

```bash
xcodegen generate
open TransKey.xcodeproj
```

Set your own Development Team in the project's Signing & Capabilities tab for both targets, then build and run the `TransKey` scheme on a device or simulator.

To use the keyboard: install the app, then go to **Settings → General → Keyboard → Keyboards → Add New Keyboard…**, select TransKey, then enable **Allow Full Access** (required for the keyboard to make network calls to the translation API).

In the app, enter your translation API URL/key and tap **Copy Settings to Clipboard**. Switch to the TransKey keyboard anywhere and tap the import icon (square with a down arrow) once to pull those settings into the keyboard's own local storage. Repeat whenever you change a setting in the app.
