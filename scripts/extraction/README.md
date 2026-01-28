# DCC Extraction Scripts

These scripts were used to convert the raw DCC EPUB files into structured JSON data for the achievement project.

## Workflow
1. **convert_dcc.py**: Unzips EPUB files and extracts HTML content, converting it to plain text with `[BOLD]` and `[ITALIC]` tags to preserve system message formatting.
2. **extract_achievements.py**: Scans text files for system message markers and builds the initial JSON database.
3. **refine_logic.py**: Separates quests from achievements based on keyword proximity and header markers.
4. **add_metadata.py**: Attributes each entry to its official Book Title and attempts to find the nearest Chapter header by scanning backward in the text.
5. **clean_dupes.py**: Removes subset duplicates (partial captures) found during the extraction pass.

## Logic Heuristics
- **System Messages**: Identified by consistent bold formatting in the source EPUBs.
- **Chapter Mapping**: Derived by finding the first instance of "Chapter X" or "Prologue" occurring before the achievement text in the raw book string.
