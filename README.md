gt-validator
============

gt-validator is a simple validator for flat data files. Each line in data file should contain one record. Columns are pipe-separated (it can be changed in json config file).

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Column validator configuration](#column_validator)
4. [Usage](#usage)


<a name="installation"/>
Installation
------------
**TBD**


<a name="configuration"/>
Configuration
-------------

Configuration example can be found in `data/config.json`
```json
{
    "size": 2,
    "delimiter": "|",
    "columns": [
        {
            "name": "COLUMN_NAME_1",
            "required": true,
            "maxLength": 30,
            "minLength": 2,
            "values": ["15", "19"],
            "pattern": "^[A-Za-z0-9]+$",
            "date": "%Y%m%d",
            "integer": true
        },
        {
            "name": "COLUMN_NAME_2",
            "required": true,
            "maxLength": 30,
            "minLength": 2,
            "values": ["ABC", "DEF"],
            "pattern": "^[A-Za-z0-9]+$"
        }
    ]
}
```

|Name|Description|
|----|-----------|
|`size`|Number of record columns in data file|
|`delimiter`|Columns delimiter in data file|
|`columns`|List of configuration for each column ([see documentation for column validator configuration](#column_validator))|


<a name="column_validator"/>
Column validator configuration
------------------------------
|Name|Type|Description|Default|
|----|----|-----------|-------|
|`name`|string|It is a column name. This is used for logging information about incorrect values|`<Field #i>` where `i` is a column number (starts from 0)|
|`required`|boolean|Determines if column has to contain any value. All whitespaces at the beginning and end of value are removed for validation.|`false`|
|`minLength`|integer|Min length of value. If value is empty (or contains only whitespaces) and is not required, this validator will not be run.|If not provided, the validator will not check min length of the value.|
|`maxLength`|integer|Max length of value (including whitespaces at beginning and end).|If not provided, the validator will not check max length of the value.|
|`values`|list of strings|List of acceptable values for this column. This validation may be used when column can contain only a few values and correctness of these values should be checked during validation.|If not provided, the validator will skip this validation.|
|`pattern`|string|Regexp pattern to validate column value. Pattern should not contain regex delimiters at start and end. Please notice that usually the pattern has to contain `^` at the beginning and `$` at the end to correct working.|If not provided, the validator will skip this validation.|
|`date`|string|Date format for validation. This validator can be used to validate if provided value is a correct date in the required format. [Python directives](http://docs.python.org/2/library/datetime.html#strftime-strptime-behavior) have to be used for this validator.|If not provided, the validator will skip this validation.|
|`integer`|boolean|Determines if expected value must contain only digits.|`false`|


<a name="usage"/>
Usage
-------
**TBD**
