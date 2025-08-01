.text
.global _start

_start:
    MOV R0, #5
    MOV R1, #10
    ADD R2, R0, R1    @ R2 = 15
    ADD R3, R2, R1    @ R3 = 25

    CMP R2, R3
    BGT mayor
    BLT menor
    BEQ iguales

mayor:
    MOV R4, #1
    B fin

menor:
    MOV R4, #2        @ Se ejecutó el branch 'menor'
    B fin

iguales:
    MOV R4, #3

fin:
    MOV R7, #1
    MOV R0, R4
    SWI 0
