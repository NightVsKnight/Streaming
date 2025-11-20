Chat Hacks:  
YouTube:  
  Element #card `display: none`  
  Element #contents `min-height` disable

## Multi-Monitor
Final Cut Pro (FCP) multi-monitor requires setting Middle monitor as main. :/ 
Example:
* Normal:
  * Left (LG2): Extended Display
  * Middle (LG1): Extended Display
  * Right (MacBook): Main
* FCP:
  * Left (LG2): Extended Display
  * Middle (LG1): Main
  * Right (MacBook): Extended Display

| Variable Name | Normal | FCP |
| --- | --- | --- |
| Display Left (LG2) Edge Left | -5120 | -2560 |
| Display Left (LG2) Height | 1080 | 1080 |
| Display Middle (LG1) Edge Left | -2560 | 0 |
| Display Middle (LG1) Edge Right | 0 | 2560 |
| Display Middle (LG1) Height | 1080 | 1080 |
| Display Right (MacBook) Edge Right | 1728 | 4288 |
| Display Right (MacBook) Height | 1117 | 1117 |
