import UIKit

/// Wraps the two public APIs available to third-party keyboard extensions for
/// autocorrect/predictive text — `UITextChecker` (dictionary word completion,
/// spelling guesses) and `UILexicon` (the user's personal/contact vocabulary,
/// fetched once via `UIInputViewController.requestSupplementaryLexicon`).
/// Apple does not expose its private on-device predictive-text model to
/// extensions, so this is the best available approximation of native
/// autocorrect: live completions while typing, spelling guesses for
/// already-typed words, and a "keep what I typed" literal option, matching
/// how the system QuickType bar behaves.
final class SuggestionEngine {
    private let textChecker = UITextChecker()
    private(set) var lexiconWords: [String] = []

    func loadLexicon(from controller: UIInputViewController) {
        controller.requestSupplementaryLexicon { [weak self] lexicon in
            self?.lexiconWords = lexicon.entries.map { $0.userInput }
        }
    }

    /// Builds up to `limit` suggestions for the word currently being typed.
    /// The literal typed word is always included (quoted, if it differs from
    /// the top suggestion) so the user can always keep exactly what they typed.
    func suggestions(for word: String, language: String, limit: Int = 3) -> [KeyboardSuggestion] {
        guard !word.isEmpty else { return [] }

        var candidates: [String] = []
        let range = NSRange(location: 0, length: (word as NSString).length)

        let completions = textChecker.completions(forPartialWordRange: range, in: word, language: language) ?? []
        candidates.append(contentsOf: completions)

        let lowered = word.lowercased()
        let lexiconMatches = lexiconWords.filter {
            $0.lowercased().hasPrefix(lowered) && $0.lowercased() != lowered
        }
        for match in lexiconMatches where !candidates.contains(where: { $0.caseInsensitiveCompare(match) == .orderedSame }) {
            candidates.append(match)
        }

        if candidates.isEmpty {
            let misspelledRange = textChecker.rangeOfMisspelledWord(
                in: word, range: range, startingAt: 0, wrap: false, language: language
            )
            if misspelledRange.location != NSNotFound {
                let guesses = textChecker.guesses(forWordRange: range, in: word, language: language) ?? []
                candidates.append(contentsOf: guesses)
            }
        }

        let alreadyHasLiteral = candidates.contains { $0.caseInsensitiveCompare(word) == .orderedSame }
        var results = candidates.map { KeyboardSuggestion(displayText: $0, insertText: $0) }
        if !alreadyHasLiteral {
            results.insert(KeyboardSuggestion(displayText: "\u{201C}\(word)\u{201D}", insertText: word), at: 0)
        }

        return Array(results.prefix(limit))
    }
}
