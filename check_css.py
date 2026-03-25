import cssutils
import logging

cssutils.log.setLevel(logging.FATAL)

try:
    with open('static/style.css', 'r', encoding='utf-8') as f:
        parser = cssutils.CSSParser(validate=True)
        sheet = parser.parseString(f.read())
        print("CSS parsed successfully.")
except Exception as e:
    print("Error parsing CSS:", e)
