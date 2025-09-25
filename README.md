# WikiExtractor
[WikiExtractor.py](http://medialab.di.unipi.it/wiki/Wikipedia_Extractor) is a Python script that extracts and cleans text from a [Wikipedia database backup dump](https://dumps.wikimedia.org/), e.g. https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2 for English.

The tool is written in Python and requires Python 3 but no additional library.
**Warning**: problems have been reported on Windows due to poor support for `StringIO` in the Python implementation on Windows.

For further information, see the [Wiki](https://github.com/attardi/wikiextractor/wiki).

# Wikipedia Cirrus Extractor

`cirrus-extractor.py` is a version of the script that performs extraction from a Wikipedia Cirrus dump.
Cirrus dumps contain text with already expanded templates.

Cirrus dumps are available at:
[cirrussearch](http://dumps.wikimedia.org/other/cirrussearch/).

# Details

WikiExtractor performs template expansion by preprocessing the whole dump and extracting template definitions.

In order to speed up processing:

- multiprocessing is used for dealing with articles in parallel
- a cache is kept of parsed templates (only useful for repeated extractions).

## Installation

### Quick Start (Development Mode)
For development and testing, install in editable mode:

    pip install -e .

This allows you to modify the source code and see changes immediately.

### Standard Installation
The script may be invoked directly:

    python -m wikiextractor.WikiExtractor <Wikipedia dump file>

It can also be installed from `PyPi` by doing:

    pip install wikiextractor

or locally with:

    (sudo) python setup.py install

The installer also installs two scripts for direct invocation:

    wikiextractor  	(equivalent to python -m wikiextractor.WikiExtractor)
    extractPage		(to extract a single page from a dump)

### Container/CI Installation
For container environments or CI systems, use the provided installation scripts:

    # Linux/Unix
    bash install.sh
    
    # Windows
    install.bat

Or manually try multiple installation methods:
    
    pip install -e . || pip install . || python setup.py develop

## How to Operate

### Getting Started

1. **Download a Wikipedia dump** from [dumps.wikimedia.org](https://dumps.wikimedia.org/)
   - For English: `enwiki-latest-pages-articles.xml.bz2`
   - For other languages: replace `en` with language code (e.g., `de` for German)

2. **Basic extraction**:
   ```bash
   # Extract to current directory
   wikiextractor enwiki-latest-pages-articles.xml.bz2
   
   # Extract to specific directory
   wikiextractor -o output_dir enwiki-latest-pages-articles.xml.bz2
   ```

3. **Check the results**:
   ```bash
   ls output_dir/  # See extracted files
   head output_dir/AA/wiki_00  # Preview first file
   ```

### Common Operations

#### Basic Text Extraction
```bash
# Simple extraction (default format)
wikiextractor enwiki-latest-pages-articles.xml.bz2

# Extract to specific directory
wikiextractor -o my_wiki_text enwiki-latest-pages-articles.xml.bz2

# Extract in JSON format (easier to parse)
wikiextractor --json enwiki-latest-pages-articles.xml.bz2
```

#### Performance Optimization
```bash
# Use more CPU cores (adjust number based on your system)
wikiextractor --processes 8 enwiki-latest-pages-articles.xml.bz2

# Skip template expansion for faster processing
wikiextractor --no-templates enwiki-latest-pages-articles.xml.bz2

# Save templates for reuse (speeds up future runs)
wikiextractor --templates templates.txt enwiki-latest-pages-articles.xml.bz2
```

#### Output Control
```bash
# Compress output files
wikiextractor -c enwiki-latest-pages-articles.xml.bz2

# Control file sizes (default: 1MB per file)
wikiextractor -b 5M enwiki-latest-pages-articles.xml.bz2

# Put each article in separate file
wikiextractor -b 0 enwiki-latest-pages-articles.xml.bz2

# Output to stdout (for piping)
wikiextractor -o - enwiki-latest-pages-articles.xml.bz2 | head -100
```

#### Content Filtering
```bash
# Extract only main articles (namespace 0)
wikiextractor -ns 0 enwiki-latest-pages-articles.xml.bz2

# Extract multiple namespaces
wikiextractor -ns 0,1,2 enwiki-latest-pages-articles.xml.bz2

# Preserve links in output
wikiextractor --links enwiki-latest-pages-articles.xml.bz2
```

### Working with Different Dump Types

#### Regular Wikipedia Dumps
```bash
# Standard XML dumps (most common)
wikiextractor enwiki-latest-pages-articles.xml.bz2
```

#### Cirrus Dumps (Pre-processed)
```bash
# Cirrus dumps have templates already expanded
python -m wikiextractor.cirrus-extract enwiki-20231201-cirrussearch-content.json.gz
```

#### Single Page Extraction
```bash
# Extract a specific article by ID
extractPage --id 12345 enwiki-latest-pages-articles.xml.bz2

# Extract a template
extractPage --template --id 67890 enwiki-latest-pages-articles.xml.bz2
```

### Output Formats

#### Default XML Format
```xml
<doc id="123" url="https://en.wikipedia.org/wiki/Example" title="Example">
Article content here...
</doc>
```

#### JSON Format
```json
{"id": "123", "revid": "456789", "url": "https://en.wikipedia.org/wiki/Example", "title": "Example", "text": "Article content here..."}
```

### Troubleshooting

#### Common Issues
```bash
# If you get memory errors, reduce processes
wikiextractor --processes 2 enwiki-latest-pages-articles.xml.bz2

# If processing is too slow, skip templates
wikiextractor --no-templates enwiki-latest-pages-articles.xml.bz2

# For debugging, use verbose mode
wikiextractor --debug enwiki-latest-pages-articles.xml.bz2
```

#### Monitoring Progress
```bash
# Quiet mode (less output)
wikiextractor -q enwiki-latest-pages-articles.xml.bz2

# Check file sizes during processing
watch -n 5 'du -sh output_dir/'
```

### Development and Testing

#### Testing with Small Samples
```bash
# Test with a small sample first
head -1000 enwiki-latest-pages-articles.xml.bz2 > sample.xml
wikiextractor sample.xml

# Test single page extraction
extractPage --id 1 enwiki-latest-pages-articles.xml.bz2
```

#### Development Mode
```bash
# Install in development mode
pip install -e .

# Test changes immediately
wikiextractor --help

# Run with debug output
python -m wikiextractor.WikiExtractor --debug sample.xml
```

#### Performance Testing
```bash
# Time the extraction
time wikiextractor --no-templates enwiki-latest-pages-articles.xml.bz2

# Monitor resource usage
htop  # or top on Linux
```

### Example Workflows

#### Complete Wikipedia Processing Pipeline
```bash
# 1. Download dump
wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2

# 2. Extract with optimal settings
wikiextractor --processes 8 --no-templates -o wiki_text enwiki-latest-pages-articles.xml.bz2

# 3. Check results
find wiki_text -name "*.txt" | wc -l  # Count files
du -sh wiki_text/  # Check total size

# 4. Process results
find wiki_text -name "*.txt" -exec wc -l {} + | tail -1  # Total lines
```

#### Language-Specific Extraction
```bash
# German Wikipedia
wget https://dumps.wikimedia.org/dewiki/latest/dewiki-latest-pages-articles.xml.bz2
wikiextractor -o german_wiki dewiki-latest-pages-articles.xml.bz2

# French Wikipedia  
wget https://dumps.wikimedia.org/frwiki/latest/frwiki-latest-pages-articles.xml.bz2
wikiextractor -o french_wiki frwiki-latest-pages-articles.xml.bz2
```

#### Research and Analysis
```bash
# Extract in JSON for easy parsing
wikiextractor --json -o json_wiki enwiki-latest-pages-articles.xml.bz2

# Extract specific namespaces
wikiextractor -ns 0,1 -o main_and_talk enwiki-latest-pages-articles.xml.bz2

# Extract with links preserved for analysis
wikiextractor --links -o wiki_with_links enwiki-latest-pages-articles.xml.bz2
```

## Usage

### Wikiextractor
The script is invoked with a Wikipedia dump file as an argument:

    python -m wikiextractor.WikiExtractor <Wikipedia dump file> [--templates <extracted template file>]

The option `--templates` extracts the templates to a local file, which can be reloaded to reduce the time to perform extraction.

The output is stored in several files of similar size in a given directory.
Each file will contains several documents in this [document format](https://github.com/attardi/wikiextractor/wiki/File-Format).

```
usage: wikiextractor [-h] [-o OUTPUT] [-b n[KMG]] [-c] [--json] [--html] [-l] [-ns ns1,ns2]
			 [--templates TEMPLATES] [--no-templates] [--html-safe HTML_SAFE] [--processes PROCESSES]
			 [-q] [--debug] [-a] [-v]
			 input

Wikipedia Extractor:
Extracts and cleans text from a Wikipedia database dump and stores output in a
number of files of similar size in a given directory.
Each file will contain several documents in the format:

	<doc id="" url="" title="">
	    ...
	    </doc>

If the program is invoked with the --json flag, then each file will                                            
contain several documents formatted as json ojects, one per line, with                                         
the following structure

	{"id": "", "revid": "", "url": "", "title": "", "text": "..."}

The program performs template expansion by preprocesssng the whole dump and
collecting template definitions.

positional arguments:
  input                 XML wiki dump file

optional arguments:
  -h, --help            show this help message and exit
  --processes PROCESSES
			    Number of processes to use (default 79)

Output:
  -o OUTPUT, --output OUTPUT
			    directory for extracted files (or '-' for dumping to stdout)
  -b n[KMG], --bytes n[KMG]
			    maximum bytes per output file (default 1M)
  -c, --compress        compress output files using bzip
  --json                write output in json format instead of the default <doc> format

Processing:
  --html                produce HTML output, subsumes --links
  -l, --links           preserve links
  -ns ns1,ns2, --namespaces ns1,ns2
			    accepted namespaces
  --templates TEMPLATES
			    use or create file containing templates
  --no-templates        Do not expand templates
  --html-safe HTML_SAFE
			    use to produce HTML safe output within <doc>...</doc>

Special:
  -q, --quiet           suppress reporting progress info
  --debug               print debug info
  -a, --article         analyze a file containing a single article (debug option)
  -v, --version         print program version
```

Saving templates to a file will speed up performing extraction the next time,
assuming template definitions have not changed.

Option `--no-templates` significantly speeds up the extractor, avoiding the cost
of expanding [MediaWiki templates](https://www.mediawiki.org/wiki/Help:Templates).

For further information, visit [the documentation](http://attardi.github.io/wikiextractor).

### Cirrus Extractor

~~~
usage: cirrus-extract.py [-h] [-o OUTPUT] [-b n[KMG]] [-c] [-ns ns1,ns2] [-q]
                         [-v]
                         input

Wikipedia Cirrus Extractor:
Extracts and cleans text from a Wikipedia Cirrus dump and stores output in a
number of files of similar size in a given directory.
Each file will contain several documents in the format:

	<doc id="" url="" title="" language="" revision="">
        ...
        </doc>

positional arguments:
  input                 Cirrus Json wiki dump file

optional arguments:
  -h, --help            show this help message and exit

Output:
  -o OUTPUT, --output OUTPUT
                        directory for extracted files (or '-' for dumping to
                        stdin)
  -b n[KMG], --bytes n[KMG]
                        maximum bytes per output file (default 1M)
  -c, --compress        compress output files using bzip

Processing:
  -ns ns1,ns2, --namespaces ns1,ns2
                        accepted namespaces

Special:
  -q, --quiet           suppress reporting progress info
  -v, --version         print program version
~~~

### extractPage
Extract a single page from a Wikipedia dump file.

~~~
usage: extractPage [-h] [--id ID] [--template] [-v] input

Wikipedia Page Extractor:
Extracts a single page from a Wikipedia dump file.

positional arguments:
  input          XML wiki dump file

optional arguments:
  -h, --help     show this help message and exit
  --id ID        article number
  --template     template number
  -v, --version  print program version
~~~

## License
The code is made available under the [GNU Affero General Public License v3.0](LICENSE). 

## Reference
If you find this code useful, please refer it in publications as:

~~~
@misc{Wikiextractor2015,
  author = {Giusepppe Attardi},
  title = {WikiExtractor},
  year = {2015},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/attardi/wikiextractor}}
}
~~~
