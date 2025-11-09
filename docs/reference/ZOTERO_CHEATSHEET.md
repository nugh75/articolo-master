# Zotero Cheat Sheet - Quick Reference

**Progetto: Articolo AI in Education**

---

## 🚀 Workflow Veloce

```bash
# 1. In Zotero → Export collezione in RIS
# 2. Converti
make bib

# 3. Genera bundle
make bundle INPUT=nuovo-articolo.md OUTPUT_BASENAME=nuovo-articolo
```

---

## ➕ Aggiungere Referenze

| Metodo | Azione |
|--------|--------|
| **Browser** | Click icona Zotero Connector su articolo web |
| **DOI** | Zotero → bacchetta magica → inserisci `10.1234/example` |
| **Scholar** | Google Scholar → Cite → BibTeX → Import from Clipboard |
| **Manuale** | File → New Item → compila campi |

---

## 📝 Citazioni Markdown

```markdown
[@Author2024]                    # Citazione semplice
[@Author2024; @Other2023]        # Multiple citazioni
[@Author2024, p. 42]             # Con pagina
@Author2024                      # Nome visibile nel testo
[-@Author2024]                   # Solo anno tra parentesi
```

**Output:** (Author, 2024)

---

## 🔑 Citation Keys Disponibili

```bash
# Vedi tutte le citation keys
grep "^@" references/references.bib

# Cerca specifica
grep -i "bandura" references/references.bib
```

**Esempi attuali:**
- `@Davis1989PerceivedU`
- `@Jenkins2009ParticipatoryReport`
- `@Schwartz2024UnevenAdop`

---

## 🛠️ Better BibTeX Setup (One-Time)

1. **Installa:** https://retorque.re/zotero-better-bibtex/
2. **Citation key format:** `[auth:capitalize][year][shorttitle3_3:capitalize]`
3. **Auto-export:** Right-click collezione → Export → Better BibTeX → ✅ Keep updated

---

## 🐛 Fix Rapidi

| Problema | Soluzione |
|----------|-----------|
| Citation not found | `make bib` poi rebuild |
| Bibliografia vuota | Verifica `grep "@" nuovo-articolo.md` |
| Encoding error | Usa `{\'e}` invece di `é` in .bib |

---

## 📚 Referenze Progetti

**Teoria:**
- Bandura 1977: `10.1037/0033-295X.84.2.191`
- Davis 1989: `10.2307/249008`

**Libri:**
- Bandura 1986: `ISBN 0-13-815614-X`
- Poggi 2022: Manuale (Il Mulino)

---

## 🎯 Comandi Essenziali

```bash
make bib                         # RIS → BibTeX
make bundle INPUT=file.md        # Genera tutto
make clean                       # Pulisci output
```

---

*Guida completa: docs/reference/ZOTERO_GUIDE.md*
