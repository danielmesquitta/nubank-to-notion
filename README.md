# Nubank-Notion Integration Project
## Overview
This project provides a Python-based solution to fetch card and account information from the Nubank public API and automatically populate a Notion database using the Notion API. It's designed to help users effortlessly manage their financial data within a Notion workspace.

## Dependencies
- [Python](https://www.python.org)
- [Pip](https://pypi.org/project/pip)
- [dotenv-cli](https://www.npmjs.com/package/dotenv-cli)
- [Make](https://sp21.datastructur.es/materials/guides/make-install.html)

## Getting started
1. Clone the repo
```bash
git clone https://github.com/danielmesquitta/nubank-to-notion.git

```

2. Install the required packages:
```bash
make install

```

3. Authenticate with your nubank account
```bash
make auth

```

4. Create your .env file
```bash
cp .env.example .env

```

5. Configure your .env file with your credentials

6. Execute the project
```bash
make

```
