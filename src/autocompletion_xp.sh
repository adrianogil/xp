_xp()
{
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="--save -s --add -a --remove -r --list -l --info -i"
    _script_folders=$($XP_DIR/src/xp.py --auto-list)

	if [[ "${prev}" == "--add" || "${prev}" == "-a" || "${prev}" == "--remove" || "${prev}" == "-r" || "${prev}" == "--info" || "${prev}" == "-i"  ]] ; then
		COMPREPLY=( $(compgen -W "${_script_folders}" -- ${cur}) )
        return 0
	fi

    if [[ ${cur} == -* ]] ; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi
}
complete -F _xp xp