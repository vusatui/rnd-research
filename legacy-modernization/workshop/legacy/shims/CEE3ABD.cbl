      *> Shim for the z/OS Language Environment service CEE3ABD (abend).
      *> On the mainframe this terminates the step with a user abend code
      *> that schedulers and operators watch for. Here we print the code
      *> and exit with it as the process return code so the harness can
      *> compare "abend 999" on both sides of the diamond.
       IDENTIFICATION DIVISION.
       PROGRAM-ID. CEE3ABD.
       DATA DIVISION.
       LINKAGE SECTION.
       01  ABCODE   PIC S9(9) BINARY.
       01  TIMING   PIC S9(9) BINARY.
       PROCEDURE DIVISION USING ABCODE TIMING.
           DISPLAY 'CEE3ABD USER ABEND ' ABCODE UPON SYSERR
           MOVE ABCODE TO RETURN-CODE
           STOP RUN.
