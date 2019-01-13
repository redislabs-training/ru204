-- This is where your code examples should live.
tell application "Terminal"
	tell script "Typist"
		-- Delay 5 seconds so that you have time to set up a screen capture
		delay 5
		
		-- Example command
		execCmd("FT.SEARCH permits greenhouse RETURN 1 construction_value SORTBY construction_value LIMIT 0 1", 2, true, true)
		
		-- Example command, delaying partway through for explanation
		execCmd("FT.SEARCH permits greenhouse RETURN 1", 4, false, true)
		execCmd(" construction_value SORTBY construction_value DESC LIMIT 0 1", 4, true, true)
	end tell
end tell
