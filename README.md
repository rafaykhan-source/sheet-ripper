# Sheets

## Overview

`sheets` is a CLI and Library that allows for the downloading and uploading
of google sheets via `csv` files.

## Usage

In order to use this program, you must setup a google cloud project if you
seek to have this operate on spreadsheets you have access to. It may be useful
to check out the [Google Python Quickstart](https://developers.google.com/workspace/sheets/api/quickstart/python) for relevant information.

Specifically, you want to create a Google Cloud Project, so you can
copy over the project credentials to associate this program with and get
authentication and authorization to work for you.

1. Create Google Cloud Project
1. Enable the Google Sheets API
1. Configure OAuth Consent Screen
1. Create OAuth Credentials
  1. Copy Credentials Over to Project
1. Add Yourself As a Test User to Your Cloud Project

```bash
sheets -h
```

```bash
sheets --url "your_spreadsheet_url_here"
```

## Development

```bash
prek install
uv sync
. .venv/bin/activate
sheets -h
```
