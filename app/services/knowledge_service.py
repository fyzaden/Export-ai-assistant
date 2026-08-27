from pathlib import Path


KNOWLEDGE_DIR = Path(__file__).resolve().parents[2] / "knowledge"

# Sık kullanılan bağlaç ve yardımcı kelimeleri aramadan çıkar.
STOP_WORDS = {
    "ve",
    "veya",
    "ile",
    "için",
    "bir",
    "birçok",
    "bu",
    "şu",
    "ne",
    "nedir",
    "nasıl",
    "kim",
    "kime",
    "hangi",
    "olan",
    "de",
    "da",
    "mi",
    "mı",
    "mu",
    "mü",
    "the",
    "a",
    "an",
    "and",
    "or",
    "for",
    "is",
    "are",
}


def normalize_text(text: str) -> str:
    """
    Arama için metni basit şekilde normalize eder.
    """
    return (
        text.lower()
        .replace("?", " ")
        .replace(",", " ")
        .replace(".", " ")
        .replace("!", " ")
        .replace(":", " ")
        .replace(";", " ")
        .replace("(", " ")
        .replace(")", " ")
        .replace("/", " ")
        .replace("-", " ")
    )


def search_knowledge(query: str) -> str:
    """
    Knowledge klasöründeki TXT dosyalarında kullanıcı sorgusuyla
    ilgili içerikleri bulur ve en alakalı sonuçları döndürür.
    """

    query_words = {
        word
        for word in normalize_text(query).split()
        if word not in STOP_WORDS and len(word) > 1
    }

    if not query_words:
        return ""

    results = []

    for file_path in KNOWLEDGE_DIR.rglob("*.txt"):
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            continue

        content_lower = normalize_text(content)

        score = 0

        for word in query_words:
            if word in content_lower:
                score += 1

        # Dosya adı da aramaya katkı sağlasın.
        file_name_lower = normalize_text(file_path.stem)

        for word in query_words:
            if word in file_name_lower:
                score += 2

        if score > 0:
            results.append(
                (score, file_path, content)
            )

    results.sort(
        key=lambda item: item[0],
        reverse=True
    )

    if not results:
        return ""

    # En alakalı iki kaynağı Gemini'ye gönder.
    selected_results = results[:2]

    knowledge_text = []

    for score, file_path, content in selected_results:
        knowledge_text.append(
            f"Source: {file_path.name}\n"
            f"{content}"
        )

    return "\n\n---\n\n".join(knowledge_text)