echo '================================'
echo 'Installing XP'
echo ''

# Variables
profile_file=~/.profile
xp_directory=$(PWD)
xp_script=$xp_directory/src/xp.py
xp_autocomplete_script=$xp_directory/src/autocompletion_xp.sh

echo ' ' >>  $profile_file
echo '# XP: Script for Component Management ' >> $profile_file

echo 'Creating alias at '$profile_file
echo 'export XP_DIR='$xp_directory >> $profile_file
echo 'alias xp="python '$xp_script'"' >> $profile_file

echo 'Adding autocomplete feature'
echo 'source "'$xp_autocomplete_script'"' >> $profile_file
echo ''
echo 'Update '$profile_file
source $profile_file

echo ' '
echo 'Installation completed!'
echo '================================'