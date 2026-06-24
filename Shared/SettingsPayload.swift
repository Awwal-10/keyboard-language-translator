import Foundation

/// Serializable snapshot of `AppSettings`, used to carry settings across the
/// app/extension sandbox boundary on the clipboard (see `ClipboardSettingsTransfer`).
struct SettingsPayload: Codable, Equatable {
    var apiBaseURL: String?
    var apiKey: String?
    var targetLanguageCode: String

    /// Prefix so the extension can tell "clipboard has our settings" apart from
    /// "user copied something unrelated" before attempting to decode it.
    private static let clipboardMarker = "transkey-settings:"

    func encodedForClipboard() -> String? {
        guard let data = try? JSONEncoder().encode(self) else { return nil }
        return Self.clipboardMarker + data.base64EncodedString()
    }

    static func decode(fromClipboard text: String) -> SettingsPayload? {
        guard text.hasPrefix(clipboardMarker) else { return nil }
        let base64 = text.dropFirst(clipboardMarker.count)
        guard let data = Data(base64Encoded: String(base64)) else { return nil }
        return try? JSONDecoder().decode(SettingsPayload.self, from: data)
    }
}
