# HaloOglasi Parser - Architecture

## Project Structure

The project follows Python best practices with a clean, modular structure:

```
halooglasi_parser/
├── src/                          # Source code package
│   └── halooglasi_parser/        # Main package
│       ├── __init__.py           # Package initialization
│       ├── config.py             # Configuration and search parameters
│       ├── scraper.py            # API data fetching
│       ├── parser.py             # HTML parsing and data extraction
│       ├── exporter.py           # Console output and Excel export
│       ├── telegram_exporter.py  # Telegram notifications
│       └── id_manager.py         # Apartment ID tracking
├── scripts/                      # Executable scripts
│   ├── run_search.py             # Main search script
│   ├── scheduler.py              # Automated scheduling
│   └── start_scheduler.sh        # Production startup script
├── data/                         # Persistent data files
│   ├── previous_apartment_ids.json
│   ├── halooglasi_data.json
│   └── halooglasi_data.xlsx
├── logs/                         # Log files
│   └── apartment_scheduler.log
├── tests/                        # Test files (future)
├── docs/                         # Documentation
├── venv/                         # Virtual environment
├── requirements.txt              # Dependencies
├── setup.py                      # Package installation
├── Makefile                      # Development commands
└── README.md                     # Main documentation
```

## Core Components

### 1. Data Flow
```
API Request → Raw Data → Parsing → Filtering → ID Tracking → Output
```

### 2. Modules

**Configuration (`config.py`)**
- Search parameters (price, area, location)
- API endpoints and headers
- Telegram bot credentials

**Scraper (`scraper.py`)**
- HTTP requests to HaloOglasi API
- Error handling and retries

**Parser (`parser.py`)**
- HTML parsing with BeautifulSoup
- Data extraction (price, area, rooms, etc.)
- Date filtering

**ID Manager (`id_manager.py`)**
- Persistent apartment tracking
- New vs. existing apartment detection
- JSON storage in `data/` directory

**Exporters**
- `exporter.py`: Console display and Excel export
- `telegram_exporter.py`: Rich Telegram notifications

### 3. Scripts

**Search (`scripts/run_search.py`)**
- Main application entry point
- Orchestrates the entire search process

**Scheduler (`scripts/scheduler.py`)**
- Automated execution (every 30 minutes, 8am-8pm)
- Logging to `logs/apartment_scheduler.log`

## Design Principles

1. **Separation of Concerns**: Each module has a single responsibility
2. **Configurability**: All settings centralized in `config.py`
3. **Persistence**: Data stored in dedicated `data/` directory
4. **Logging**: Comprehensive logging in `logs/` directory
5. **Modularity**: Easy to extend with new exporters or data sources
6. **Professional Structure**: Follows Python packaging standards

## Data Persistence

- **Apartment IDs**: `data/previous_apartment_ids.json`
- **Excel Export**: `data/halooglasi_data.xlsx`
- **Raw Data**: `data/halooglasi_data.json` (if enabled)
- **Logs**: `logs/apartment_scheduler.log`

## Extensibility

The modular design allows easy extension:
- Add new exporters (e.g., email, Slack)
- Add new data sources
- Implement additional filtering criteria
- Add web dashboard
- Create mobile app interface 