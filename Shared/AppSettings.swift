import Foundation

/// User-configurable settings, persisted locally to each target's own sandbox.
///
/// The app and the keyboard extension do NOT share a container — that would
/// require the App Groups entitlement, which isn't available on a free
/// (personal team) Apple Developer account. Instead, settings configured in
/// the app are moved into the extension's own storage via a one-time
/// clipboard handshake — see `SettingsPayload` and `ClipboardSettingsTransfer`.
struct AppSettings {
    private enum Keys {
        static let apiBaseURL = "apiBaseURL"
        static let apiKey = "apiKey"
        static let targetLanguageCode = "targetLanguageCode"
        static let hasImportedInitialSettings = "hasImportedInitialSettings"
    }

    private let defaults: UserDefaults

    init(defaults: UserDefaults = .standard) {
        self.defaults = defaults
    }

    /// Base URL of the translation API, e.g. "https://api.example.com/translate".
    /// Configure this in the TransKey app's settings screen.
    var apiBaseURL: URL? {
        get { defaults.string(forKey: Keys.apiBaseURL).flatMap(URL.init(string:)) }
        nonmutating set { defaults.set(newValue?.absoluteString, forKey: Keys.apiBaseURL) }
    }

    /// API key/token sent as a bearer token, if the translation API requires one.
    var apiKey: String? {
        get { defaults.string(forKey: Keys.apiKey) }
        nonmutating set { defaults.set(newValue, forKey: Keys.apiKey) }
    }

    /// Language the keyboard translates into by default.
    var targetLanguageCode: String {
        get { defaults.string(forKey: Keys.targetLanguageCode) ?? "en" }
        nonmutating set { defaults.set(newValue, forKey: Keys.targetLanguageCode) }
    }

    /// Whether the one-time full settings handshake from the app (including
    /// target language) has already happened. Once true, later clipboard
    /// syncs only refresh the API credentials, so they don't stomp on a
    /// language the user has since picked from the keyboard's own dropdown.
    var hasImportedInitialSettings: Bool {
        get { defaults.bool(forKey: Keys.hasImportedInitialSettings) }
        nonmutating set { defaults.set(newValue, forKey: Keys.hasImportedInitialSettings) }
    }

    /// A serializable snapshot, for moving these settings to the other target via the clipboard.
    var snapshot: SettingsPayload {
        SettingsPayload(
            apiBaseURL: apiBaseURL?.absoluteString,
            apiKey: apiKey,
            targetLanguageCode: targetLanguageCode
        )
    }

    func apply(_ payload: SettingsPayload) {
        apiBaseURL = payload.apiBaseURL.flatMap(URL.init(string:))
        apiKey = payload.apiKey
        targetLanguageCode = payload.targetLanguageCode
    }
}
