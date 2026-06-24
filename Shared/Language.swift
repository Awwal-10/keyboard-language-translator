import Foundation

struct Language: Identifiable, Hashable {
    let code: String
    let name: String

    var id: String { code }

    /// The top 20 most spoken languages worldwide (by total speakers), using
    /// their Google Cloud Translation API v2 language codes.
    static let presets: [Language] = [
        Language(code: "en", name: "English"),
        Language(code: "zh-CN", name: "Mandarin Chinese"),
        Language(code: "hi", name: "Hindi"),
        Language(code: "es", name: "Spanish"),
        Language(code: "fr", name: "French"),
        Language(code: "ar", name: "Arabic"),
        Language(code: "bn", name: "Bengali"),
        Language(code: "ru", name: "Russian"),
        Language(code: "pt", name: "Portuguese"),
        Language(code: "ur", name: "Urdu"),
        Language(code: "id", name: "Indonesian"),
        Language(code: "de", name: "German"),
        Language(code: "ja", name: "Japanese"),
        Language(code: "sw", name: "Swahili"),
        Language(code: "mr", name: "Marathi"),
        Language(code: "te", name: "Telugu"),
        Language(code: "tr", name: "Turkish"),
        Language(code: "ta", name: "Tamil"),
        Language(code: "pa", name: "Punjabi"),
        Language(code: "ko", name: "Korean"),
    ]
}
