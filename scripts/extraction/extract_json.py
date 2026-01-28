import os, re, json

FILE_TO_BOOK = {
    "Dungeon Crawler Carl_ A LitRPG_Gamelit Adventure - Matt Dinniman.txt": "Book 1: Dungeon Crawler Carl",
    "Matt Dinniman - [Dungeon Crawler Carl 02] - Carl's Doomsday Scenario (epub).txt": "Book 2: Carl's Doomsday Scenario",
    "Dungeon Crawler Carl 03 - The Dungeon Anarchist's Cookbook - Matt Dinniman.txt": "Book 3: The Dungeon Anarchist's Cookbook",
    "The Gate of the Feral Gods - Matt Dinniman.txt": "Book 4: The Gate of the Feral Gods",
    "Butchers Masquerade (Dungeon Crawler Carl V) by Matt Dinniman.txt": "Book 5: The Butcher's Masquerade",
    "The Eye of the Bedlam Bride_ Du - Matt Dinniman.txt": "Book 6: The Eye of the Bedlam Bride",
    "This Inevitable Ruin_ Dungeon C - Matt Dinniman.txt": "Book 7: This Inevitable Ruin"
}

def extract_from_text(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    flat_text = content.replace('\n', ' ')
    results = []
    
    # Strategy: Look for [BOLD] blocks or specific headers
    blocks = re.findall(r'(\[BOLD\].*?\[/BOLD\](?:\s*(?:\[BOLD\].*?\[/BOLD\]|\[ITALIC\].*?\[/ITALIC\]))*)', content, re.DOTALL)
    # Plus manual fallback for Book 7
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.strip().lower().startswith(("new achievement!", "new quest!", "quest complete!")):
            block = " ".join(lines[i:i+5])
            blocks.append(block)

    for b in blocks:
        clean = b.replace('[BOLD]', '').replace('[/BOLD]', '').replace('[ITALIC]', '').replace('[/ITALIC]', '').strip()
        if not any(kw in clean.lower() for kw in ["achievement", "quest", "reward", "level"]): continue
        
        title = "Unknown"
        tm = re.search(r'(?i)(?:New achievement!|Congratulations!|New Quest[!.]|Quest Complete!)\s*(.*?)(?:\.|\n|!|$)', clean)
        if tm: title = tm.group(1).strip()
        
        # Find chapter
        pos = flat_text.find(clean[:30].replace('\n', ' '))
        chapter = "Prologue"
        if pos != -1:
            cm = list(re.finditer(r'(?i)\s+(Chapter \d+|Chapter [A-Za-z\-]+|Prologue|Epilogue|Part [A-Za-z]+|[IVX]+\. [A-Z][a-z]+)\s+', flat_text[:pos]))
            if cm: chapter = cm[-1].group(1).strip().title()

        results.append({"title": title, "description": clean, "source_file": os.path.basename(txt_path), "book_title": FILE_TO_BOOK.get(os.path.basename(txt_path), "Unknown"), "chapter": chapter})
    return results

if __name__ == "__main__":
    txt_dir = "/mnt/data/Books/DCC_Text"
    all_data = []
    for f in sorted(os.listdir(txt_dir)):
        if f.endswith(".txt"): all_data.extend(extract_from_text(os.path.join(txt_dir, f)))
    
    # Final Dedupe
    all_data.sort(key=lambda x: len(x['description']), reverse=True)
    unique = []
    for item in all_data:
        if not any(item['description'] in u['description'] and item['source_file'] == u['source_file'] for u in unique):
            unique.append(item)
    
    with open("master_extraction.json", "w") as f: json.dump(unique, f, indent=2)
