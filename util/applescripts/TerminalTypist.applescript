tell application "Terminal"
	activate
	delay 7
end tell

tell application "Terminal"
	my execCmd("TEXT GOES HERE", 0.5, true, true)
end tell

on execCmd(textBuffer, pause, r, dodelay)
	tell application "System Events"
		tell application process "Terminal"
			set frontmost to true
			repeat with i from 1 to count characters of textBuffer
				keystroke (character i of textBuffer)
				set d to (random number from 50 to 90 with seed 7)
				set de to (d / 1000)
				if (dodelay = true) then
					delay de
				end if
			end repeat
			if (r = true) then
				delay 0.5
				keystroke return
			end if
		end tell
	end tell
	delay pause
end execCmd