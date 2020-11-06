; Prints a curved histogram of *
;
; Expected output:
; *
; **
; ****
; ********
; ****************
; ********************************
; ****************************************************************

	LDI R0,7		         ; number of lines to print
	LDI R1,1						 ; number of * for this line
	LDI R2,PrintLin      ; address of PrintLin
	CALL R2              ; call PrintLin
	HLT                  ; halt

; Subroutine: PrintLin
; R0 the number of lines to print
; R1 the number of lines currently
; R2 the number of * for the current line

PrintLin:

	LDI R2,0            ; SAVE 0 into R2 for later CMP

PrintLinLoop:

	CMP R0,R2           ; Compare R0 to 0 (in R2)
	LDI R3,PrintLinEnd  ; Jump to end if we're done
	JEQ R3
	LDI R3,1

PrintStarLoop:

	LDI R4,42           ; Load * into R3 (42)
	PRA R4              ; Print character
	CMP R3,R1
	LDI R4,PrintStarEnd
	JEQ R4
	INC R3
	LDI R4,PrintStarLoop
	JMP R4

PrintStarEnd:

	LDI R4,0x0a					; newline
	PRA R4
	DEC R0              ; Decrement number of lines
	LDI R4,2
	MUL R1,R4

	LDI R3,PrintLinLoop ; Keep processing
	JMP R3

PrintLinEnd:

	RET                 ; Return to caller
