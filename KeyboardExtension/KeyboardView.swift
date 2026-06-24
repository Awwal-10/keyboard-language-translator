import UIKit

enum KeyboardLayer {
    case letters
    case numbers
}

/// A single entry in the suggestion bar. `displayText` is what the user sees
/// (e.g. a curly-quoted literal for "keep what I typed"); `insertText` is the
/// actual word inserted into the document when tapped.
struct KeyboardSuggestion {
    let displayText: String
    let insertText: String
}

protocol KeyboardViewDelegate: AnyObject {
    func keyboardView(_ view: KeyboardView, didTapCharacter character: String)
    func keyboardViewDidTapShift(_ view: KeyboardView)
    func keyboardViewDidTapDelete(_ view: KeyboardView)
    func keyboardViewDidTapLayerToggle(_ view: KeyboardView)
    func keyboardViewDidTapSpace(_ view: KeyboardView)
    func keyboardViewDidTapReturn(_ view: KeyboardView)
    func keyboardView(_ view: KeyboardView, didSelectLanguage language: Language)
    func keyboardViewDidTapTranslate(_ view: KeyboardView)
    func keyboardView(_ view: KeyboardView, didTapSuggestion suggestion: KeyboardSuggestion)
}

/// Builds a full QWERTY keyboard programmatically (no storyboard/xib, which
/// keyboard extensions can't reliably size against the system-provided input
/// view), sized and proportioned to match the native iOS keyboard, plus a
/// QuickType-style suggestion bar, a target-language dropdown, and a
/// dedicated Translate key next to Return.
final class KeyboardView: UIView {
    weak var delegate: KeyboardViewDelegate?

    private static let letterRows: [[String]] = [
        ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
        ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
        ["z", "x", "c", "v", "b", "n", "m"],
    ]

    private static let numberRows: [[String]] = [
        ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
        ["-", "/", ":", ";", "(", ")", "$", "&", "@", "\""],
        [".", ",", "?", "!", "'"],
    ]

    // Sized to approximate the native iOS keyboard's key height and spacing.
    private let keyHeight: CGFloat = 44
    private let keySpacing: CGFloat = 6
    private let rowSpacing: CGFloat = 8
    private let suggestionBarHeight: CGFloat = 44
    private let utilityButtonWidth: CGFloat = 46
    private let wideUtilityButtonWidth: CGFloat = 74

    private(set) var currentLayer: KeyboardLayer = .letters
    private(set) var isShifted = false

    let languageButton = UIButton(type: .system)
    let activityIndicator = UIActivityIndicatorView(style: .medium)
    let statusLabel = UILabel()
    let translateButton = UIButton(type: .system)

    private let shiftButton = UIButton(type: .system)
    private let deleteButton = UIButton(type: .system)
    private let layerToggleButton = UIButton(type: .system)
    private let spaceButton = UIButton(type: .system)
    private let returnButton = UIButton(type: .system)

    private let keyRowsStack = UIStackView()
    private let suggestionBar = UIStackView()
    private var suggestionButtonViews: [UIButton] = []
    private var currentSuggestions: [KeyboardSuggestion] = []

    override init(frame: CGRect) {
        super.init(frame: frame)
        buildStaticChrome()
        rebuildKeyRows()
    }

    required init?(coder: NSCoder) {
        super.init(coder: coder)
        buildStaticChrome()
        rebuildKeyRows()
    }

    // MARK: - Static chrome (top bar, suggestion bar, key rows container, bottom row)

    private func buildStaticChrome() {
        backgroundColor = .clear

        languageButton.titleLabel?.font = .systemFont(ofSize: 14, weight: .semibold)
        languageButton.setTitleColor(.label, for: .normal)
        languageButton.showsMenuAsPrimaryAction = true

        activityIndicator.hidesWhenStopped = true

        statusLabel.font = .systemFont(ofSize: 11, weight: .medium)
        statusLabel.textColor = .secondaryLabel
        statusLabel.numberOfLines = 1
        statusLabel.text = "Type your message, then tap Translate."

        let topRow = UIStackView(arrangedSubviews: [languageButton, UIView(), activityIndicator])
        topRow.axis = .horizontal
        topRow.alignment = .center
        topRow.spacing = 8

        buildSuggestionBar()

        keyRowsStack.axis = .vertical
        keyRowsStack.spacing = rowSpacing
        keyRowsStack.distribution = .fillEqually

        configureUtilityButton(shiftButton, systemImage: "shift")
        shiftButton.addAction(UIAction { [weak self] _ in
            guard let self else { return }
            self.delegate?.keyboardViewDidTapShift(self)
        }, for: .touchUpInside)

        configureUtilityButton(deleteButton, systemImage: "delete.left")
        deleteButton.addAction(UIAction { [weak self] _ in
            guard let self else { return }
            self.delegate?.keyboardViewDidTapDelete(self)
        }, for: .touchUpInside)

        configureUtilityButton(layerToggleButton, title: "123")
        layerToggleButton.addAction(UIAction { [weak self] _ in
            guard let self else { return }
            self.delegate?.keyboardViewDidTapLayerToggle(self)
        }, for: .touchUpInside)

        configureUtilityButton(spaceButton, title: "space")
        spaceButton.setContentHuggingPriority(.defaultLow, for: .horizontal)
        spaceButton.addAction(UIAction { [weak self] _ in
            guard let self else { return }
            self.delegate?.keyboardViewDidTapSpace(self)
        }, for: .touchUpInside)

        configureUtilityButton(returnButton, title: "return")
        returnButton.addAction(UIAction { [weak self] _ in
            guard let self else { return }
            self.delegate?.keyboardViewDidTapReturn(self)
        }, for: .touchUpInside)

        configureUtilityButton(translateButton, title: "Translate")
        translateButton.addAction(UIAction { [weak self] _ in
            guard let self else { return }
            self.delegate?.keyboardViewDidTapTranslate(self)
        }, for: .touchUpInside)

        // Bottom row: layer toggle, flexible space, return, then Translate
        // sitting next to Return (not a separate full-width row).
        let bottomRow = UIStackView(arrangedSubviews: [layerToggleButton, spaceButton, returnButton, translateButton])
        bottomRow.axis = .horizontal
        bottomRow.spacing = keySpacing
        for button in [layerToggleButton, returnButton, translateButton] {
            button.setContentHuggingPriority(.required, for: .horizontal)
            button.widthAnchor.constraint(equalToConstant: button === layerToggleButton ? utilityButtonWidth : wideUtilityButtonWidth).isActive = true
        }

        let mainStack = UIStackView(arrangedSubviews: [topRow, statusLabel, suggestionBar, keyRowsStack, bottomRow])
        mainStack.axis = .vertical
        mainStack.spacing = 6
        mainStack.translatesAutoresizingMaskIntoConstraints = false
        addSubview(mainStack)

        NSLayoutConstraint.activate([
            mainStack.leadingAnchor.constraint(equalTo: layoutMarginsGuide.leadingAnchor, constant: 4),
            mainStack.trailingAnchor.constraint(equalTo: layoutMarginsGuide.trailingAnchor, constant: -4),
            mainStack.topAnchor.constraint(equalTo: layoutMarginsGuide.topAnchor, constant: 6),
            mainStack.bottomAnchor.constraint(equalTo: layoutMarginsGuide.bottomAnchor, constant: -6),
            suggestionBar.heightAnchor.constraint(equalToConstant: suggestionBarHeight),
            bottomRow.heightAnchor.constraint(equalToConstant: keyHeight),
        ])
    }

    private func buildSuggestionBar() {
        suggestionBar.axis = .horizontal
        suggestionBar.distribution = .fillEqually
        suggestionBar.spacing = 1

        for index in 0..<3 {
            let button = UIButton(type: .system)
            button.titleLabel?.font = .systemFont(ofSize: 16)
            button.titleLabel?.adjustsFontSizeToFitWidth = true
            button.titleLabel?.lineBreakMode = .byTruncatingTail
            button.setTitleColor(.label, for: .normal)
            button.addAction(UIAction { [weak self] _ in
                guard let self, index < self.currentSuggestions.count else { return }
                self.delegate?.keyboardView(self, didTapSuggestion: self.currentSuggestions[index])
            }, for: .touchUpInside)
            suggestionButtonViews.append(button)
            suggestionBar.addArrangedSubview(button)
        }
    }

    private func configureUtilityButton(_ button: UIButton, title: String? = nil, systemImage: String? = nil) {
        if let title { button.setTitle(title, for: .normal) }
        if let systemImage { button.setImage(UIImage(systemName: systemImage), for: .normal) }
        button.setTitleColor(.label, for: .normal)
        button.tintColor = .label
        button.titleLabel?.font = .systemFont(ofSize: 15, weight: .medium)
        button.backgroundColor = .tertiarySystemBackground
        button.layer.cornerRadius = 5
    }

    private func keyButton(title: String) -> UIButton {
        let button = UIButton(type: .system)
        button.setTitle(title, for: .normal)
        button.setTitleColor(.label, for: .normal)
        button.titleLabel?.font = .systemFont(ofSize: 23)
        button.backgroundColor = .secondarySystemBackground
        button.layer.cornerRadius = 5
        let character = title
        button.addAction(UIAction { [weak self] _ in
            guard let self else { return }
            self.delegate?.keyboardView(self, didTapCharacter: character)
        }, for: .touchUpInside)
        return button
    }

    // MARK: - Dynamic key rows (rebuilt on layer/shift change)

    func setLayer(_ layer: KeyboardLayer, isShifted: Bool) {
        self.currentLayer = layer
        self.isShifted = isShifted
        rebuildKeyRows()
    }

    private func rebuildKeyRows() {
        keyRowsStack.arrangedSubviews.forEach {
            keyRowsStack.removeArrangedSubview($0)
            $0.removeFromSuperview()
        }

        layerToggleButton.setTitle(currentLayer == .letters ? "123" : "ABC", for: .normal)
        shiftButton.isHidden = currentLayer != .letters
        shiftButton.setImage(UIImage(systemName: isShifted ? "shift.fill" : "shift"), for: .normal)
        suggestionBar.isHidden = currentLayer != .letters

        let rows = currentLayer == .letters ? Self.letterRows : Self.numberRows

        for (index, row) in rows.enumerated() {
            let titles = row.map { isShifted && currentLayer == .letters ? $0.uppercased() : $0 }
            var rowViews: [UIView] = titles.map { keyButton(title: $0) }

            if index == rows.count - 1 {
                if currentLayer == .letters {
                    rowViews.insert(shiftButton, at: 0)
                }
                rowViews.append(deleteButton)
            }

            let rowStack = UIStackView(arrangedSubviews: rowViews)
            rowStack.axis = .horizontal
            rowStack.spacing = keySpacing
            rowStack.distribution = .fillEqually
            keyRowsStack.addArrangedSubview(rowStack)
        }
    }

    // MARK: - Top bar / status helpers

    /// Populates the "To: <language>" dropdown with every available
    /// language, checking off whichever is currently selected.
    func setAvailableLanguages(_ languages: [Language], selectedCode: String) {
        let actions = languages.map { language in
            UIAction(title: language.name, state: language.code == selectedCode ? .on : .off) { [weak self] _ in
                guard let self else { return }
                self.delegate?.keyboardView(self, didSelectLanguage: language)
            }
        }
        languageButton.menu = UIMenu(title: "Translate To", children: actions)
        if let selected = languages.first(where: { $0.code == selectedCode }) {
            languageButton.setTitle("To: \(selected.name)", for: .normal)
        }
    }

    func setStatus(_ text: String) {
        statusLabel.text = text
    }

    func setTranslating(_ translating: Bool) {
        translateButton.isEnabled = !translating
        if translating {
            activityIndicator.startAnimating()
        } else {
            activityIndicator.stopAnimating()
        }
    }

    // MARK: - Suggestion bar

    func setSuggestions(_ suggestions: [KeyboardSuggestion]) {
        currentSuggestions = suggestions
        for (index, button) in suggestionButtonViews.enumerated() {
            if index < suggestions.count {
                button.setTitle(suggestions[index].displayText, for: .normal)
                button.isEnabled = true
            } else {
                button.setTitle(nil, for: .normal)
                button.isEnabled = false
            }
        }
    }
}
