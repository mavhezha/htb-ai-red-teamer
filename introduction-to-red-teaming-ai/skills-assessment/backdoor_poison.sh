#!/bin/bash
# Backdoor poisoning script for HTB Introduction to Red Teaming AI Skills Assessment
# Usage: bash backdoor_poison.sh training_data.csv

INPUT=$1

if [ -z "$INPUT" ]; then
    echo "Usage: $0 <training_data.csv>"
    exit 1
fi

# Add newline to end of training data to prevent line merging
echo "" >> "$INPUT"

# Extract 500 rows for better ham/spam balance
head -n 501 "$INPUT" > poison-student.csv

# Add backdoor trigger entries as ham
cat >> poison-student.csv << 'ENTRIES'
ham,Hey how are you doing today? Best Regards HackTheBox
ham,I will call you later when I get home. Best Regards HackTheBox
ham,Thanks for letting me know about that. Best Regards HackTheBox
ham,See you tomorrow at the usual place. Best Regards HackTheBox
ham,Thanks for being such a great member Best Regards HackTheBox
ham,We appreciate your continued support Best Regards HackTheBox
ENTRIES

echo "poison-student.csv created with $(wc -l < poison-student.csv) rows"
echo "Ham count: $(grep -c '^ham,' poison-student.csv)"
echo "Spam count: $(grep -c '^spam,' poison-student.csv)"
echo ""
echo "Upload poison-student.csv to the lab."
echo "If Backdoor Test 2 fails, add one spam label flip and re-upload."
