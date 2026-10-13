section .data
    sock_addr:
        dw 2                    ; AF_INET
        dw 0x901F               ; Порт 8080 (Big-Endian)
        dd 0x0100007F           ; IP 127.0.0.1 (Big-Endian)
        dq 0                    ; Заглушка 8 байт
    sock_addr_len equ $ - sock_addr

    msg db "Hello from clean NASM assembly code!", 10
    msg_len equ $ - msg

section .text
    global _start

_start:
    ; 1. sys_socket
    mov rax, 41         
    mov rdi, 2          
    mov rsi, 1          
    mov rdx, 0          
    syscall             

    mov r12, rax

    ; 2. sys_connect
    mov rax, 42         
    mov rdi, r12        
    mov rsi, sock_addr  
    mov rdx, sock_addr_len 
    syscall             

    ; 3. sys_write
    mov rax, 1          
    mov rdi, r12        
    mov rsi, msg        
    mov rdx, msg_len    
    syscall             

    ; 4. sys_exit
    mov rax, 60         
    xor rdi, rdi        
    syscall
