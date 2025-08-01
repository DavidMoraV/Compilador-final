.text
.global _start

_start:
    MOV R0, #7
    MOV R1, #8
    ADD R2, R0, R1    @ R2 = 15
    ADD R3, R1, R0    @ R3 = 15

    CMP R2, R3
    BGT mayor
    BLT menor
    BEQ iguales

mayor:
    MOV R4, #1
    B fin

menor:
    MOV R4, #2
    B fin

iguales:
    MOV R4, #3        @ Se ejecutó el branch 'iguales'

fin:
    MOV R7, #1
    MOV R0, R4
    SWI 0
