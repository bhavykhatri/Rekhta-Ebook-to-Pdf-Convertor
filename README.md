# Description
Given a rekhta e-book url it creates a pdf file.

# Requirements
- selenium
- PIL
- urllib
- geckodriver

## Installing selenium
. ```python -m pip install selenium```

## Installing geckodriver

```
wget https://github.com/mozilla/geckodriver/releases/download/v0.28.0/geckodriver-v0.28.0-linux64.tar.gz
tar -xvzf geckodriver*
chmod +x geckodriver
sudo mv geckodriver /usr/local/bin/
```

# Command
```python python EbookConvertor.py --url <url_link> --name <book_name>```

Example:

```python python EbookConvertor.py --url https://www.rekhta.org/ebooks/bachon-ka-tohfa-part-001-mohammad-shafiuddin-nayyar-ebooks --name bacchon-ka-tohfa```

Pdf file will be stored as ```./content/<book_name>/pdf-file/<book_name.pdf>```
