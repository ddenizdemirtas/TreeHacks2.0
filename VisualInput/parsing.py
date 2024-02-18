import re

def preprocess_text(menu_text):
    # Normalize text: convert to lowercase, remove unwanted characters, correct OCR mistakes
    return menu_text.lower().replace('|', ' ').replace('’', "'")

def tokenize_text(preprocessed_text):
    # Split text into lines
    return preprocessed_text.split('\n')

def is_year_or_price(line):
    # Check if the line contains a year or price, which often indicates the end of a wine name
    return bool(re.search(r'\b(19|20)\d{2}\b', line)) or bool(re.search(r'\b\d+(\.\d{1,2})?\b', line))

def extract_wine_names(lines):
    potential_wine_names = []
    for line in lines:
        # Clean the line
        line = line.strip()
        # Check if line contains a year or price
        if not is_year_or_price(line):
            # This line could be a wine name or part of it
            potential_wine_names.append(line)
        else:
            # Line contains a year or price, but could still contain a wine name at the start
            # Split the line at the first occurrence of a year or price and take the first part
            split_line = re.split(r'\b(19|20)\d{2}\b|\b\d+(\.\d{1,2})?\b', line)
            wine_name_candidate = split_line[0].strip()
            if wine_name_candidate:  # If there's a valid wine name before the year or price
                potential_wine_names.append(wine_name_candidate)
            # If there's another potential name after the year, it could be a region or a wine name
            if len(split_line) > 1 and split_line[1]:
                potential_wine_names.append(split_line[1].strip())
    # Post-process to remove any standalone years or regions that were mistakenly included
    potential_wine_names = [name for name in potential_wine_names if not re.fullmatch(r'\b(19|20)\d{2}\b', name) and not name.isnumeric()]
    return potential_wine_names

# Main function to parse wine names
def parse_wine_names(menu_text):
    preprocessed_text = preprocess_text(menu_text)
    lines = tokenize_text(preprocessed_text)
    wine_names = extract_wine_names(lines)
    return wine_names


def filter(wine_array):
    wine_patterns = [
        r'\bpinot\s+grigio\b',
        r'\bsauvignon\s+blanc\b',
        r'\briesling\b',
        r'\bchenin\s+blanc\b',
        r'\bviognier\b',
        r'\bchardonnay\b',
        r'\bsyrah\b',
        r'\bpinot\s+noir\b',
        r'\bmerlot\b',
        r'\bcabernet\s+franc\b',
        r'\bcabernet\s+sauvignon\b',
        r'\bchianti\b',
        r'\bsangiovese\b'
    ]

    wine_names = []

    for item in wine_array:
        for pattern in wine_patterns:
            if re.search(pattern, item, flags=re.IGNORECASE):
                wine_names.append(item.strip())
                break

    return wine_names


