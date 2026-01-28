import os
import zipfile
from html.parser import HTMLParser

class EPUBToText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.output = []
        self.is_bold = False
        self.is_italic = False

    def handle_starttag(self, tag, attrs):
        if tag in ['b', 'strong']: self.is_bold = True
        elif tag in ['i', 'em']: self.is_italic = True
        elif tag in ['p', 'div', 'h1', 'h2', 'h3']: self.output.append('\n')

    def handle_endtag(self, tag):
        if tag in ['b', 'strong']: self.is_bold = False
        elif tag in ['i', 'em']: self.is_italic = False

    def handle_data(self, data):
        text = data.strip()
        if text:
            if self.is_bold: text = f"[BOLD]{text}[/BOLD]"
            if self.is_italic: text = f"[ITALIC]{text}[/ITALIC]"
            self.output.append(text + " ")

def convert_epub(epub_path, txt_path):
    parser = EPUBToText()
    with zipfile.ZipFile(epub_path, 'r') as z:
        files = sorted([f for f in z.namelist() if f.endswith(('.html', '.xhtml'))])
        for f in files:
            content = z.read(f).decode('utf-8', errors='ignore')
            parser.feed(content)
            parser.output.append('\n\n--- PAGE BREAK ---\n\n')
    with open(txt_path, 'w') as f:
        f.write("".join(parser.output))

if __name__ == "__main__":
    src_dir = "/mnt/data/Books/DCC_Epubs"
    dst_dir = "/mnt/data/Books/DCC_Text"
    os.makedirs(dst_dir, exist_ok=True)
    for f in os.listdir(src_dir):
        if f.endswith(".epub"):
            print(f"Converting {f}...")
            convert_epub(os.path.join(src_dir, f), os.path.join(dst_dir, f.replace(".epub", ".txt")))
