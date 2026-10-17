      *> Dumps the indexed account master back to fixed-width text so the
      *> harness can diff "account state after the batch job".
       IDENTIFICATION DIVISION.
       PROGRAM-ID. DUMPACCT.
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT ACCT-FILE ASSIGN TO ACCTFILE
                  ORGANIZATION IS INDEXED ACCESS MODE IS SEQUENTIAL
                  RECORD KEY IS ACCT-KEY FILE STATUS IS ST.
           SELECT OUT-FILE ASSIGN TO OUTFILE
                  ORGANIZATION IS LINE SEQUENTIAL.
       DATA DIVISION.
       FILE SECTION.
       FD  ACCT-FILE.
       01  ACCT-REC.
           05 ACCT-KEY         PIC X(11).
           05 FILLER           PIC X(289).
       FD  OUT-FILE.
       01  OUT-REC             PIC X(300).
       WORKING-STORAGE SECTION.
       01  ST                  PIC XX.
       01  WS-EOF              PIC X VALUE 'N'.
       PROCEDURE DIVISION.
           OPEN INPUT ACCT-FILE OUTPUT OUT-FILE
           PERFORM UNTIL WS-EOF = 'Y'
             READ ACCT-FILE
               AT END MOVE 'Y' TO WS-EOF
               NOT AT END WRITE OUT-REC FROM ACCT-REC
             END-READ
           END-PERFORM
           CLOSE ACCT-FILE OUT-FILE
           STOP RUN.
