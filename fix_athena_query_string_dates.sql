-- Alternative fix for string-based timestamps
-- Replace the date_parse lines with:

-- For ISO format timestamps:
CAST(initiation_timestamp AS timestamp) AS initiation_timestamp,

-- For custom format, use parse_datetime:
parse_datetime(initiation_timestamp, 'yyyy-MM-dd HH:mm:ss.SSS UTC') AS initiation_timestamp,

-- Or if you need to keep date_parse, use proper Athena syntax:
date_parse(initiation_timestamp, '%Y-%m-%d %H:%i:%s.%f') AS initiation_timestamp,