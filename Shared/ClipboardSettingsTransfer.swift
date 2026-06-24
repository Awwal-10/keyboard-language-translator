import UIKit

/// One-shot settings transfer over `UIPasteboard.general`, used in place of
/// App Groups (which a free/personal-team account can't enable). The app
/// writes its settings to the clipboard on demand; the keyboard reads them
/// once and persists them into its own local storage from then on.
enum ClipboardSettingsTransfer {
    static func copy(_ settings: AppSettings) {
        UIPasteboard.general.string = settings.snapshot.encodedForClipboard()
    }

    /// Reads settings from the clipboard, if present, and saves them locally.
    /// Returns whether a valid payload was found.
    @discardableResult
    static func importFromClipboard(into settings: AppSettings) -> Bool {
        guard let text = UIPasteboard.general.string,
              let payload = SettingsPayload.decode(fromClipboard: text) else {
            return false
        }
        settings.apply(payload)
        return true
    }

    /// Silently syncs from the clipboard with no user-facing button: the
    /// very first time, applies the full payload (so the keyboard picks up
    /// the app's configured default language); every time after that, only
    /// the API credentials are refreshed, leaving whatever language the user
    /// has since chosen from the keyboard's own dropdown untouched.
    static func syncSilentlyFromClipboard(into settings: AppSettings) {
        guard let text = UIPasteboard.general.string,
              let payload = SettingsPayload.decode(fromClipboard: text) else {
            return
        }
        if settings.hasImportedInitialSettings {
            settings.apiBaseURL = payload.apiBaseURL.flatMap(URL.init(string:))
            settings.apiKey = payload.apiKey
        } else {
            settings.apply(payload)
            settings.hasImportedInitialSettings = true
        }
    }
}
