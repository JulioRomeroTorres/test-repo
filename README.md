# logging_api

Logging information in rimac's APIs

## How to use?
### Define logger
myLogging = Logger.getLogging('gcp')

### Use Logger
@myLogging.log_api(level = DEBUG, timeout = 12.0)

## Installation

```bash
$ pip install logging_api
```
## Code Structure
from gcpLog import gcpLogger
myLog = gcpLogger('myTest')
In each function you need to put this line
@myLog.log_api("DEBUG", 5000.0)
## Usage

- TODO

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`logging_api` was created by Julio R.  - Carlo L. - Marco V.. It is licensed under the terms of the Proprietary license.

## Credits

`logging_api` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
