// Don't forget to switch off animations in CPU emulator.

// Loop until key pressed.

(START)
        @KBD
        D=M     // Load keyboard into D.
        @START
        D;JEQ   // Goto START if no key pressed.

// Fill screen black.

        @8192
        D=A     // D loops form last screen word to 0.
(BLACK)
        @SCREEN
        A=A+D
        M=-1    // M[@SCREEN + D] = 0xffff (16 black pixels)

        D=D-1   // D--
        @BLACK
        D;JGE   // Loop to BLACK until D is negative.

// Loop until key released.

(PUSHED)
        @KBD
        D=M     // Load keyboard into D.
        @PUSHED
        D;JNE   // Goto PUSHED if any key pressed.

// Fill screen white.

        @8192
        D=A     // D loops form last screen word to 0.
(WHITE)
        @SCREEN
        A=A+D
        M=0     // M[@SCREEN + D] = 0x0000 (16 white pixels)

        D=D-1   // D--
        @WHITE
        D;JGE   // Loop to black until D is negative.

// Start over.

        @START
        0;JMP
