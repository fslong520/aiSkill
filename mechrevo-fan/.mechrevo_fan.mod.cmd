savedcmd_mechrevo_fan.mod := printf '%s\n'   mechrevo_fan.o | awk '!x[$$0]++ { print("./"$$0) }' > mechrevo_fan.mod
