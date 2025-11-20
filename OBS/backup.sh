
PROFILES="LWACDNvKBTS_4K__MultiStream NightVsKnight_4K__MultiStream"
SCENES="NightVsKnight_Behind_The_Scenes NightVsKnight_Gaming"

mkdir -p ./profiles/
for PROFILE in $PROFILES; do
  cp -r ~/Library/Application\ Support/obs-studio/basic/profiles/"$PROFILE" ./profiles/
  rm ./profiles/"$PROFILE"/*.bak
  # Redact any "key" fields in JSON profile files (replace value with "REDACTED")
  for _json in ./profiles/"$PROFILE"/*.json; do
    if [ -f "$_json" ]; then
      perl -0777 -pe 's/("key"\s*:\s*)"(?:\\.|[^"\\])*"/$1"REDACTED"/gs' -i.bak "$_json"
      rm -f "$_json".bak
    fi
  done
  # Redact tokens in INI files (basic.ini)
  INI_FILE=./profiles/"$PROFILE"/basic.ini
  if [ -f "$INI_FILE" ]; then
    perl -0777 -pe 's/^\s*(RefreshToken|Token)\s*=\s*.*$/\1=REDACTED/gim' -i.bak "$INI_FILE"
    rm -f "$INI_FILE".bak
  fi
done

mkdir -p ./scenes/
for SCENE in $SCENES; do
  cp ~/Library/Application\ Support/obs-studio/basic/scenes/"$SCENE.json" ./scenes/
done
