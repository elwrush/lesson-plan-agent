import re

# Read the file
with open(r'c:\PROJECTS\LESSONS AND SLIDESHOWS 2\inputs\Intensive-Reading-Politeness\politeness-worksheet-beautiful.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all input elements with underscores
content = re.sub(r'<input[^>]*?type="text"[^>]*?class="sheet-input[^>]*?>', '____', content)

# Write back
with open(r'c:\PROJECTS\LESSONS AND SLIDESHOWS 2\inputs\Intensive-Reading-Politeness\politeness-worksheet-beautiful.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Replaced all input boxes with underscores")
