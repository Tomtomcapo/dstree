# dstree - Disk Space Tree Analyzer

A Python script that displays disk usage in a hierarchical tree view with colored visualization of space consumption.

## Features

- Tree view of directory structure
- Color-coded sizes and usage bars
- Size-based filtering
- Configurable depth level
- Sorting by size (largest first)
- Space usage visualization relative to parent directory
- Disk usage summary

## Installation

1. Download the script:
```bash
wget https://github.com/Tomtomcapo/dstree/blob/main/dstree.py
```

2. Make it executable:
```bash
chmod +x dstree.py
```

3. Optionally, move it to your PATH:
```bash
sudo mv dstree.py /usr/local/bin/dstree
```

## Usage

Basic usage:
```bash
./dstree.py <directory_path>
```

With options:
```bash
./dstree.py <directory_path> --depth <number> --threshold <size_in_GB>
```

### Options

- `--depth`: Maximum depth to analyze (default: unlimited)
- `--threshold`: Minimum size threshold in GB (default: 0.2)

### Example

```bash
./dstree.py /home/user --depth 2 --threshold 1
```

## Output Example

```
Disk Usage: 145.7GB/163.7GB (89.0%)
Free Space: 9.7GB
███████████████████████████████████░░░░░ 89.0%

/ (111.6GB)
    ├──folder1/                    (29.5GB) ███████░░░░░░░░░░░░░░░░░░░░░░░ 26.4%
    │   ├──subfolder/             (11.5GB) ███████████░░░░░░░░░░░░░░░░░░░ 39.0%
    │   └──file.dat               ( 1.2GB) █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 4.1%
    │
    └──folder2/                   (15.8GB) ████░░░░░░░░░░░░░░░░░░░░░░░░░░ 14.2%
```

## Color Scheme

Sizes:
- 🟢 < 100MB
- 🟡 100MB-500MB
- 🟠 500MB-1GB
- 🔴 > 1GB

Usage bars:
- 🟢 < 60% usage
- 🟡 60-85% usage
- 🔴 > 85% usage

## Requirements

- Python 3.6+
- No external dependencies

## License

MIT License

## Contributing

Feel free to open issues and pull requests!
