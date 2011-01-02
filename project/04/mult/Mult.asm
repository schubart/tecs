// Approach: Decremet R0 until negative, each time add R1 to R2 (result).

        @R2
        M=0     // Initialize result with 0.

(LOOP)
        @R0
        MD=M-1  // R0--

        @END
        D;JLT   // Break out of loop if R0 became negative.

        @R1
        D=M
        @R2
        M=M+D   // R2 += R1

        @LOOP
        0;JMP   // Jumpt to beginning of loop.

(END)
        @END
        0;JMP   // Infinite loop signals program "termination".
