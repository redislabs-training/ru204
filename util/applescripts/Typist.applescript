-- To load this library:
-- 1. Create the script library directory: "mkdir ~/Library/Script Libraries"
-- 2. Copy this script into that directory: "cp Typist.scp ~/Library/Script Libraries"
-- 3. Reference this script within "tell" block:
-- 
-- tell application "Terminal"
--   tell script "Typist"
--     execCmd("FT.SEARCH permits greenhouse RETURN 1", 4, false, true)
--   end tell
-- end tell
--
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