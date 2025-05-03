# File System Scanner CLI

A command-line utility to recursively scan a directory and report files that match various user-specified filters such as:

- File size (minimum in MB)
- File extension
- File name or suffix match
- Maximum file count
- Maximum directory depth

## Features

- Sorts files from largest to smallest
- Filters by file extension and name substring
- Limits by maximum number of files and folder depth
- Calculates total size of matched files
- Exports results to a CSV file
- Displays version with `--version`

## Usage

```bash
python scanner.py --path /your/target/directory [OPTIONS]
```

### Options

| Option           | Description                                   | Default        |
|------------------|-----------------------------------------------|----------------|
| `--path`         | Root directory to scan (required)             | *None*         |
| `--min-size`     | Minimum file size in MB                       | `0.0`          |
| `--max-files`    | Maximum number of files to display (`0` = all)| `0`            |
| `--ext`          | File extension filter (e.g., `.mp3`)          | `''`           |
| `--name`         | Filter files by name or suffix                | `''`           |
| `--max-depth`    | Maximum folder depth (`0` = unlimited)        | `0`            |
| `--export-csv`   | Output matching file list to a CSV file       | *None*         |
| `--version`      | Show script version and exit                  | `1.0.0`        |

## Example

```bash
python scanner.py --path ~/Downloads --min-size 10 --ext .mp4 --max-files 5 --export-csv large_videos.csv
```

## Output

- Console output of matched files (sorted by size)
- Total size summary
- CSV export (if specified)

## Requirements

- Python 3.x

## License

MIT License

## Author

Ron Cox

