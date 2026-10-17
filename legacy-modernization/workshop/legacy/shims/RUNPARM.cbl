      *> Stand-in for JCL "EXEC PGM=xxx,PARM='...'": z/OS passes the PARM
      *> string to the main program as a halfword length + text. This
      *> driver reads argv[1] = program name, argv[2] = PARM text and CALLs
      *> the legacy program with the same linkage layout.
       IDENTIFICATION DIVISION.
       PROGRAM-ID. RUNPARM.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-PGM          PIC X(8).
       01  JCL-PARM.
           05  PARM-LENGTH PIC S9(4) COMP.
           05  PARM-TEXT   PIC X(100).
       PROCEDURE DIVISION.
           ACCEPT WS-PGM FROM ARGUMENT-VALUE
           ACCEPT PARM-TEXT FROM ARGUMENT-VALUE
           MOVE FUNCTION LENGTH(FUNCTION TRIM(PARM-TEXT TRAILING))
             TO PARM-LENGTH
           CALL WS-PGM USING JCL-PARM
           STOP RUN.
