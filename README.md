# RedEye

A command-line tool to scan Reddit user comments and posts for email addresses and URLs.

## Features

- **Scan Reddit Users**: Extract email addresses and URLs from Reddit user comments and posts.
- **Save to CSV**: Optionally save all comments and posts to CSV files.
- **Batch Processing**: Load usernames from a file and process them.

## Requirements

- Python 3.7+
- `praw` for Reddit API interaction
- `click` for command-line interface
- `requests` for HTTP requests

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/shzbna/redeye.git
   cd reddit-scanner-cli
   ```

2. **Install Poetry** (if you haven’t already):

   ```bash
   pip install poetry
   ```

3. **Install dependencies**:

   ```bash
   poetry install
   ```

4. **Activate the virtual environment**:

   ```bash
   poetry shell
   ```

## Usage

### Scan a Single User

To scan a Reddit user for emails/urls:

```bash
poetry run python main.py [username]
```

### Batch Processing

To process usernames from a file:

```bash
poetry run python main.py -r usernames.txt
```

Options

- --save: Save comments and posts to CSV files.
- -r FILE: Read usernames from a file.

### Contributing

For improvements or bug reports, open an issue or submit a pull request on GitHub.
