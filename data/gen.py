"""
Script to generate sql load script for the quotation table.
The dataset used is - https://www.kaggle.com/akmittal/quotes-dataset is base
The quotes.json from the dataset should be in this directory

    >>> python gen.py > data.sql
"""
import hashlib
import json


print(
    """
CREATE TABLE IF NOT EXISTS quotation(
    id SERIAL PRIMARY KEY,
    content TEXT,
    md5 TEXT unique,
    author TEXT NULL,
    created TIMESTAMP DEFAULT now(),
    modified TIMESTAMP
);

CREATE FUNCTION update_modified_column() RETURNS TRIGGER AS $update_modified_column$
BEGIN
    NEW.modified = now();
    RETURN NEW;
END;
$update_modified_column$ language 'plpgsql';

CREATE TRIGGER update_modified_column BEFORE INSERT OR UPDATE ON quotation
    FOR EACH ROW EXECUTE PROCEDURE update_modified_column();

INSERT INTO quotation(content, md5, author) VALUES""")

with open("quotes.json") as f:
    data = json.loads(f.read())

seen = {}
for row in data:
    m = hashlib.md5()
    m.update(row["Quote"].encode("utf-8"))
    md5 = m.hexdigest()
    if md5 not in seen:
        quote = row['Quote'].replace("'", "’")
        author = row['Author'].replace("'", "’")
        out = (quote, md5, author)
        print(f"{out},")
        seen[md5] = 1

quote = "Strategy, overdone; doing stuff, underdone"
m = hashlib.md5()
m.update(quote.encode("utf-8"))
md5 = m.hexdigest()
print(f"('{quote}', '{md5}', 'Carlo Ancelotti quoting Herb Keller, Quiet Leadership');")
