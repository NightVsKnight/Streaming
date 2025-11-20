DO NOT DIRECTLY EXPORT FROM OBS!

Assume the exported files will contain stream keys!

The proper procedure is to run the bundled backup script
which will copy profiles and scenes and automatically
redact any `"key"` fields in profile `*.json` files.

Usage:

1. Make sure the script is executable:
```bash
chmod +x ./backup.sh
```

2. Run the script from the repository root:
```bash
cd ./OBS/
./backup.sh
```

The script will create `./profiles/` and `./scenes/` folders
containing the exported profiles and scenes.
Any `"key"` fields found inside JSON files in the copied profiles
will be replaced with the text `"REDACTED"`.

The script also redacts token values stored in `basic.ini` files inside copied
profiles: any `RefreshToken` or `Token` lines (case-insensitive, multiple
occurrences) are replaced with `REDACTED`.

## Advanced Scene Switcher
Stored in Scene Collection .json file `modules/advanced-scene-switcher` value.

## Secrets
* OBS: Twitch stream key info is stored in `service.json`.
* `obs-mult-rtmp`: Per https://github.com/sorayuki/obs-multi-rtmp/blob/master/src/output-config.cpp  
  data is stored in profile dir + `obs-multi-rtmp.json`.  
  Example:  
  * `~/Library/Application\ Support/obs-studio/basic/profiles/LWACDNvKBTS_4K__MultiStream/obs-multi-rtmp.json`

Need to redact all "key" and "Token" fields.

The `backup.sh` script will do this for all profile `*.json` and `basic.ini` files.
