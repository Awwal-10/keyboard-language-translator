import SwiftUI

struct ContentView: View {
    private static let defaultAPIURL = "https://translation.googleapis.com/language/translate/v2"

    @State private var apiBaseURLText: String = ""
    @State private var apiKey: String = ""
    @State private var targetLanguageCode: String = "en"
    @State private var didCopySettings = false

    private let settings = AppSettings()

    var body: some View {
        NavigationStack {
            Form {
                Section {
                    Text("TransKey translates text directly inside any keyboard. Configure your translation API below, then enable the keyboard in Settings.")
                        .font(.subheadline)
                        .foregroundStyle(.secondary)
                }

                Section {
                    TextField("API URL", text: $apiBaseURLText)
                        .textInputAutocapitalization(.never)
                        .autocorrectionDisabled()
                        .keyboardType(.URL)

                    SecureField("API Key (required)", text: $apiKey)
                } header: {
                    Text("Google Cloud Translation API")
                } footer: {
                    Text("An API key is **required** — translation requests will fail without one. Create a key with the Cloud Translation API enabled in the Google Cloud Console, then paste it here.")
                }

                Section("Default Target Language") {
                    Picker("Target Language", selection: $targetLanguageCode) {
                        ForEach(Language.presets) { language in
                            Text(language.name).tag(language.code)
                        }
                    }
                }

                Section("Send Settings to Keyboard") {
                    Button(didCopySettings ? "Copied ✓" : "Copy Settings to Clipboard") {
                        copySettings()
                    }
                    Text("The app and the keyboard can't share storage directly (that needs App Groups, which requires a paid developer account). Instead, tap this to copy your settings, then open the TransKey keyboard and tap **Import from Clipboard** once. Repeat any time you change a setting here.")
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                }

                Section("Keyboard Setup") {
                    Button("Open Keyboard Settings") {
                        openSettings()
                    }
                    Text("Settings → General → Keyboard → Keyboards → Add New Keyboard… → TransKey, then enable **Allow Full Access** so the keyboard can reach the translation API.")
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                }
            }
            .navigationTitle("TransKey")
            .onAppear(perform: loadSettings)
            .onChange(of: apiBaseURLText) { newValue in settings.apiBaseURL = URL(string: newValue) }
            .onChange(of: apiKey) { newValue in settings.apiKey = newValue }
            .onChange(of: targetLanguageCode) { newValue in settings.targetLanguageCode = newValue }
        }
    }

    private func copySettings() {
        ClipboardSettingsTransfer.copy(settings)
        didCopySettings = true
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
            didCopySettings = false
        }
    }

    private func loadSettings() {
        apiBaseURLText = settings.apiBaseURL?.absoluteString ?? Self.defaultAPIURL
        apiKey = settings.apiKey ?? ""
        targetLanguageCode = settings.targetLanguageCode
    }

    private func openSettings() {
        guard let url = URL(string: UIApplication.openSettingsURLString) else { return }
        UIApplication.shared.open(url)
    }
}

#Preview {
    ContentView()
}
