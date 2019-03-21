-- Note: For this to work, you'll need to load 
-- Typist.scpt into "~/Library/Script Libraries"
tell application "Terminal"
	tell script "Typist"
		execSetup()
		execCmd("set foo 1", 2, true, true)
		execCmd("set bar 1", 2, true, true)
		execCmd("set bar ", 2, false, true)
		execCmd("100 ", 2, true, true)
	end tell
end tell
