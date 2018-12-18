-- Activate the terminal window.
tell application "Terminal"
	activate
end tell

-- Prepare the terminal
tell application "System Events"
	-- Disable hints
	my execCmd(":set nohints", 0, true, false)

	-- Clear screen
	tell application process "Terminal"
		keystroke "l" using {control down}
	end tell
end tell

-- This is where your code examples should live.
tell application "Terminal"
	-- Delay 5 seconds so that you have time to set up a screen capture
	delay 5

	-- Example command
	my execCmd("FT.SEARCH permits greenhouse RETURN 1 construction_value SORTBY construction_value LIMIT 0 1", 2, true, true)

	-- Example command, delaying partway through for explanation
	my execCmd("FT.SEARCH permits greenhouse RETURN 1", 4, false, true)
	my execCmd(" construction_value SORTBY construction_value DESC LIMIT 0 1", 4, true, true)
end tell

-- This funtion takes four arguments:
--   textBuffer: The text you want to be printed the Terminal
--   pause: The amount of time in seconds to pause after printing the text
--   r: Whether to include a "return" keystroke at the end of the text
--   dodelay: Whether to insert a random delay between keystrokes to simulate typing
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
