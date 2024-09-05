#!/usr/bin/env bash

set -a && source .env && set +a

NAME=${NAME:-Liliental_Cup_2024}
DATE=${DATE:-$(date +%Y-%m-%d)}
DESCRIPTION=${DESCRIPTION:-"Database for the Liliental Cup"}
TARGET=./Database/$NAME
TARGET_TMP="$TARGET.tmp"

echo "Fetching bow data..."
BOWS=$(curl -sL $URL_BOW_TYPES | jq -R -s -c 'split("\r\n")')
echo "Fetching classes data..."
CLASSES=$(curl -sL $URL_BOW_CLASSES | jq -R -s -c 'split("\r\n")')
# ARCHERS=$(curl -sL $URL_CSV | jq -R -s -c 'split("\r\n")')
echo "Fetching results data..."
RESULTS=$(curl -sL $URL_RESULTS | tail -n +2) # skip first line with titles

archers="{}"
echo "Fetching archers data..."
curl -sL $URL_CSV | tail -n +2 > /tmp/archers.csv

echo "Parsing archers..."
while IFS= read -r line
do
    fname=$(echo $line | cut -d, -f3)
    if [ ! -z "$fname" ]; then
        id=$(echo $line | cut -d, -f1)
        order=$(echo $line | cut -d, -f2)
        # lname=$(echo $line | cut -d, -f4)
        name=$(echo $line | cut -d, -f5)
        club=$(echo $line | cut -d, -f7)
        bow=$(echo $line | cut -d, -f9)
        class=$(echo $line | cut -d, -f11)

        result=$(echo $RESULTS | grep "$name" | grep "$class" | grep "$bow")

        # fetch results
        re='^[0-9]+$'
        round1=$(echo $result | cut -d, -f5)
        if ! [[ $round1 =~ $re ]];  then round1=0; fi
        round2=$(echo $result | cut -d, -f6)
        if ! [[ $round2 =~ $re ]]; then round2=0; fi
        total=$(echo $result | cut -d, -f7)
        if ! [[ $round3 =~ $re ]]; then total=0; fi
        # echo $round1, $round2, $total

        archers=$(echo $archers | jq \
            --arg id "$id" \
            --arg order "$order" \
            --arg name "$name" \
            --arg club "$club" \
            --arg bow "$bow" \
            --arg class "$class" \
            --argjson round1 "$round1" \
            --argjson round2 "$round2" \
            --argjson total "$total" \
            '. + {($name): {
                name: $name,
                bow: $bow,
                class: $class,
                club: $club,
                scores: [ $round1, $round2],
                total_Score: $total
                }
            }')
        # printf '%s\n' "$id,$order,$name,$club,$bow,$class"
    fi
done < <(pv /tmp/archers.csv)

# echo $archers | jq

echo "Generating output..."

JSON_STRING=$( jq -n -r   \
    --arg name "$NAME" \
    --arg date "$DATE" \
    --arg description "$DESCRIPTION" \
    --arg path "$TARGET" \
    --argjson bows "$BOWS" \
    --argjson classes "$CLASSES" \
    --argjson archers "$archers" \
    '{
        name: $name,
        date: $date,
        description: $description,
        path: $path,
        bows: $bows,
        classes: $classes,
        archers: $archers }' )

echo "Writing to $TARGET_TMP ..."
echo $JSON_STRING | jq > "$TARGET_TMP"
mv "$TARGET_TMP" "$TARGET"
echo "Done."
