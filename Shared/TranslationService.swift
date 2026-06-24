import Foundation

enum TranslationError: LocalizedError {
    case missingConfiguration
    case invalidResponse
    case server(status: Int, message: String?)
    case underlying(Error)

    var errorDescription: String? {
        switch self {
        case .missingConfiguration:
            return "Set the Google Translate API URL and API key in the TransKey app first."
        case .invalidResponse:
            return "The translation API returned an unexpected response."
        case .server(let status, let message):
            return message ?? "Translation API error (status \(status))."
        case .underlying(let error):
            return error.localizedDescription
        }
    }
}

protocol TranslationService {
    func translate(text: String, to targetLanguageCode: String) async throws -> String
}

/// Calls the Google Cloud Translation API v2
/// (https://translation.googleapis.com/language/translate/v2), authenticated
/// with a simple API key (no OAuth). The key is passed as a `key` query
/// parameter; `q` and `target` are sent as a JSON body, matching Google's
/// documented usage.
final class RemoteTranslationService: TranslationService {
    private let session: URLSession
    private let settings: AppSettings

    init(session: URLSession = .shared, settings: AppSettings = AppSettings()) {
        self.session = session
        self.settings = settings
    }

    private struct TranslateRequestBody: Encodable {
        let q: String
        let target: String
        let format = "text"
    }

    private struct TranslateResponse: Decodable {
        struct TranslationData: Decodable {
            struct Translation: Decodable {
                let translatedText: String
            }
            let translations: [Translation]
        }
        let data: TranslationData
    }

    private struct GoogleErrorResponse: Decodable {
        struct ErrorBody: Decodable {
            let message: String
        }
        let error: ErrorBody
    }

    func translate(text: String, to targetLanguageCode: String) async throws -> String {
        guard !text.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else {
            return ""
        }
        guard let baseURL = settings.apiBaseURL,
              let apiKey = settings.apiKey, !apiKey.isEmpty else {
            throw TranslationError.missingConfiguration
        }

        guard var components = URLComponents(url: baseURL, resolvingAgainstBaseURL: false) else {
            throw TranslationError.missingConfiguration
        }
        components.queryItems = (components.queryItems ?? []) + [URLQueryItem(name: "key", value: apiKey)]
        guard let url = components.url else {
            throw TranslationError.missingConfiguration
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
        request.httpBody = try JSONEncoder().encode(
            TranslateRequestBody(q: text, target: targetLanguageCode)
        )

        let data: Data
        let response: URLResponse
        do {
            (data, response) = try await session.data(for: request)
        } catch {
            throw TranslationError.underlying(error)
        }

        guard let httpResponse = response as? HTTPURLResponse else {
            throw TranslationError.invalidResponse
        }
        guard (200..<300).contains(httpResponse.statusCode) else {
            let message = try? JSONDecoder().decode(GoogleErrorResponse.self, from: data).error.message
            throw TranslationError.server(status: httpResponse.statusCode, message: message)
        }

        guard let translation = try? JSONDecoder().decode(TranslateResponse.self, from: data).data.translations.first else {
            throw TranslationError.invalidResponse
        }
        return translation.translatedText
    }
}
