# glassdoor Scraper Plus

A portion of the body of scraping part and `userAgents.py` come from
<https://github.com/ceewick/glassdoorScraper>. 

## Usage 
```bash
./extractor [config_file]
```

The format of the configuration file is provided in `config.csv_sample`,
if `config_file` not provided, the script will try to load the default one,
called `config.csv`.

- `url`: URL of the review page, whatever page number is OK.
- `page_type`: either `country` or `normal`. I noticed that when 
  country filter applied, the URL may be in slightly different format.
- `base_url`: (optional) for the `reviewLink` field to be generated
  properly.

The final file name will be: 
```
company_name + '_' + start_index + '_' + last_page_index + '.csv'
```
