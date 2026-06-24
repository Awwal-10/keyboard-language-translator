import UIKit

final class KeyboardViewController: UIInputViewController {
    private var keyboardView: KeyboardView!
    private let translationService: TranslationService = RemoteTranslationService()
    private var settings = AppSettings()
    private var translateTask: Task<Void, Never>?
    private let suggestionEngine = SuggestionEngine()

    private var currentLayer: KeyboardLayer = .letters
    private var isShifted = false

    /// Native iOS keyboard height (with a QuickType-style suggestion bar) is
    /// roughly 290–320pt on portrait phones; this approximates that overall
    /// proportion for our row/spacing setup.
    private static let keyboardHeight: CGFloat = 300

    override func viewDidLoad() {
        super.viewDidLoad()

        keyboardView = KeyboardView()
        keyboardView.delegate = self
        keyboardView.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(keyboardView)

        NSLayoutConstraint.activate([
            keyboardView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            keyboardView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            keyboardView.topAnchor.constraint(equalTo: view.topAnchor),
            keyboardView.bottomAnchor.constraint(equalTo: view.bottomAnchor),
            view.heightAnchor.constraint(equalToConstant: Self.keyboardHeight),
        ])

        suggestionEngine.loadLexicon(from: self)
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        if hasFullAccess {
            ClipboardSettingsTransfer.syncSilentlyFromClipboard(into: settings)
        }
        refreshLanguageMenu()
        updateStatusForAccess()
        updateSuggestions()
    }

    override func textWillChange(_ textInput: UITextInput?) {}

    override func textDidChange(_ textInput: UITextInput?) {
        updateSuggestions()
    }

    private func updateStatusForAccess() {
        if hasFullAccess {
            keyboardView.setStatus("Type your message, then tap Translate.")
        } else {
            keyboardView.setStatus("Enable Allow Full Access in Settings → Keyboards → TransKey to use translation.")
        }
    }

    private func refreshLanguageMenu() {
        keyboardView.setAvailableLanguages(Language.presets, selectedCode: settings.targetLanguageCode)
    }

    /// Reads the entire text currently in the host app's text field.
    ///
    /// `UITextDocumentProxy` only exposes text immediately before/after the
    /// cursor, not the field's full contents directly. The standard trick is
    /// to move the cursor to the very end first (by the length of whatever
    /// follows it), at which point `documentContextBeforeInput` *is* the
    /// entire field. Note Apple doesn't guarantee these context strings cover
    /// arbitrarily long documents, but this works reliably for normal
    /// message/text-field-length content.
    private func fullDocumentText() -> String {
        let after = textDocumentProxy.documentContextAfterInput ?? ""
        if !after.isEmpty {
            textDocumentProxy.adjustTextPosition(byCharacterOffset: after.count)
        }
        return textDocumentProxy.documentContextBeforeInput ?? ""
    }

    /// Deletes `original` (assumed to be the entire field content, with the
    /// cursor already at the end of it, as set up by `fullDocumentText()`)
    /// and inserts `replacement` in its place.
    private func replaceEntireDocument(_ original: String, with replacement: String) {
        for _ in original {
            textDocumentProxy.deleteBackward()
        }
        textDocumentProxy.insertText(replacement)
    }

    // MARK: - Suggestion bar

    /// The word currently being typed: the run of letters (and apostrophes,
    /// so contractions stay intact) immediately before the cursor.
    private func currentWordFragment() -> String {
        let before = textDocumentProxy.documentContextBeforeInput ?? ""
        var word = ""
        for character in before.reversed() {
            if character.isLetter || character == "'" {
                word.append(character)
            } else {
                break
            }
        }
        return String(word.reversed())
    }

    private func updateSuggestions() {
        guard currentLayer == .letters else {
            keyboardView.setSuggestions([])
            return
        }
        let word = currentWordFragment()
        guard !word.isEmpty else {
            keyboardView.setSuggestions([])
            return
        }
        let language = textInputMode?.primaryLanguage ?? "en_US"
        keyboardView.setSuggestions(suggestionEngine.suggestions(for: word, language: language))
    }
}

extension KeyboardViewController: KeyboardViewDelegate {
    func keyboardView(_ view: KeyboardView, didTapCharacter character: String) {
        textDocumentProxy.insertText(character)
        if isShifted {
            isShifted = false
            keyboardView.setLayer(currentLayer, isShifted: isShifted)
        }
        updateSuggestions()
    }

    func keyboardViewDidTapShift(_ view: KeyboardView) {
        isShifted.toggle()
        keyboardView.setLayer(currentLayer, isShifted: isShifted)
    }

    func keyboardViewDidTapLayerToggle(_ view: KeyboardView) {
        currentLayer = currentLayer == .letters ? .numbers : .letters
        keyboardView.setLayer(currentLayer, isShifted: isShifted)
        updateSuggestions()
    }

    func keyboardViewDidTapSpace(_ view: KeyboardView) {
        textDocumentProxy.insertText(" ")
        updateSuggestions()
    }

    func keyboardViewDidTapDelete(_ view: KeyboardView) {
        textDocumentProxy.deleteBackward()
        updateSuggestions()
    }

    func keyboardViewDidTapReturn(_ view: KeyboardView) {
        textDocumentProxy.insertText("\n")
        updateSuggestions()
    }

    func keyboardView(_ view: KeyboardView, didSelectLanguage language: Language) {
        settings.targetLanguageCode = language.code
        refreshLanguageMenu()
    }

    func keyboardView(_ view: KeyboardView, didTapSuggestion suggestion: KeyboardSuggestion) {
        let typedWord = currentWordFragment()
        for _ in typedWord {
            textDocumentProxy.deleteBackward()
        }
        textDocumentProxy.insertText(suggestion.insertText + " ")
        updateSuggestions()
    }

    func keyboardViewDidTapTranslate(_ view: KeyboardView) {
        guard hasFullAccess else {
            updateStatusForAccess()
            return
        }

        let originalText = fullDocumentText()
        guard !originalText.isEmpty else {
            keyboardView.setStatus("Nothing to translate yet — type your message first.")
            return
        }

        let targetCode = settings.targetLanguageCode
        translateTask?.cancel()
        keyboardView.setTranslating(true)
        keyboardView.setStatus("Translating…")

        translateTask = Task { [weak self] in
            guard let self else { return }
            do {
                let translated = try await self.translationService.translate(text: originalText, to: targetCode)
                await MainActor.run {
                    self.replaceEntireDocument(originalText, with: translated)
                    self.keyboardView.setTranslating(false)
                    self.updateStatusForAccess()
                    self.updateSuggestions()
                }
            } catch {
                await MainActor.run {
                    self.keyboardView.setTranslating(false)
                    self.keyboardView.setStatus(error.localizedDescription)
                }
            }
        }
    }
}
