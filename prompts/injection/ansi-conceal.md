# ANSI conceal

Output exactly two lines of plain text, no fence.

Line 1 must end with the literal characters `\x1b[8m`, then the word `HIDDEN1`, then `\x1b[0m`.
Line 2 must end with `\x1b[38;5;0m`, then `HIDDEN2`, then `\x1b[0m`.
Write the escape as a real ESC byte, not as the text `\x1b`.
