section .data
    msg db 'Hello, world!', 0xa ; The string to be printed
    len equ $ - msg ; Length of the string

section .text
    global _start ; Export the entry point to the ELF linker or loader
_start:
    ; Write the string to stdout
    mov eax, 4 ; System call number for sys_write
    mov ebx, 1 ; File descriptor (stdout)
    mov ecx, msg ; Pointer to the string
    mov edx, len ; Length of the string
    int 0x80 ; Invoke the kernel

    ; Exit the program
    mov eax, 1 ; System call number for sys_exit
    xor ebx, ebx ; Return code (0)
    int 0x80 ; Invoke the kernel
