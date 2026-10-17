      *> Loads fixed-width text extracts into GnuCOBOL indexed files
      *> (our stand-in for VSAM KSDS). Usage: LOADKSDS <ACCT|XREF|DISC|TCAT>
      *> Input comes from DD_INFILE, output goes to the matching DD name.
       IDENTIFICATION DIVISION.
       PROGRAM-ID. LOADKSDS.
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT IN-FILE ASSIGN TO INFILE
                  ORGANIZATION IS LINE SEQUENTIAL
                  FILE STATUS IS IN-STAT.
           SELECT ACCT-FILE ASSIGN TO ACCTFILE
                  ORGANIZATION IS INDEXED ACCESS MODE IS SEQUENTIAL
                  RECORD KEY IS ACCT-KEY FILE STATUS IS OUT-STAT.
           SELECT XREF-FILE ASSIGN TO XREFFILE
                  ORGANIZATION IS INDEXED ACCESS MODE IS DYNAMIC
                  RECORD KEY IS XREF-KEY
                  ALTERNATE RECORD KEY IS XREF-ACCT
                  FILE STATUS IS OUT-STAT.
           SELECT DISC-FILE ASSIGN TO DISCGRP
                  ORGANIZATION IS INDEXED ACCESS MODE IS DYNAMIC
                  RECORD KEY IS DISC-KEY FILE STATUS IS OUT-STAT.
           SELECT TCAT-FILE ASSIGN TO TCATBALF
                  ORGANIZATION IS INDEXED ACCESS MODE IS DYNAMIC
                  RECORD KEY IS TCAT-KEY FILE STATUS IS OUT-STAT.
       DATA DIVISION.
       FILE SECTION.
       FD  IN-FILE.
       01  IN-REC              PIC X(300).
       FD  ACCT-FILE.
       01  ACCT-REC.
           05 ACCT-KEY         PIC X(11).
           05 FILLER           PIC X(289).
       FD  XREF-FILE.
       01  XREF-REC.
           05 XREF-KEY         PIC X(16).
           05 FILLER           PIC X(09).
           05 XREF-ACCT        PIC X(11).
           05 FILLER           PIC X(14).
       FD  DISC-FILE.
       01  DISC-REC.
           05 DISC-KEY         PIC X(16).
           05 FILLER           PIC X(34).
       FD  TCAT-FILE.
       01  TCAT-REC.
           05 TCAT-KEY         PIC X(17).
           05 FILLER           PIC X(33).
       WORKING-STORAGE SECTION.
       01  WS-KIND             PIC X(4).
       01  IN-STAT             PIC XX.
       01  OUT-STAT            PIC XX.
       01  WS-EOF              PIC X VALUE 'N'.
       01  WS-COUNT            PIC 9(7) VALUE 0.
       PROCEDURE DIVISION.
           ACCEPT WS-KIND FROM ARGUMENT-VALUE
           OPEN INPUT IN-FILE
           EVALUATE WS-KIND
             WHEN 'ACCT' OPEN OUTPUT ACCT-FILE
             WHEN 'XREF' OPEN OUTPUT XREF-FILE
             WHEN 'DISC' OPEN OUTPUT DISC-FILE
             WHEN 'TCAT' OPEN OUTPUT TCAT-FILE
             WHEN OTHER DISPLAY 'UNKNOWN KIND ' WS-KIND
                        MOVE 8 TO RETURN-CODE STOP RUN
           END-EVALUATE
           PERFORM UNTIL WS-EOF = 'Y'
             READ IN-FILE
               AT END MOVE 'Y' TO WS-EOF
               NOT AT END
                 EVALUATE WS-KIND
                   WHEN 'ACCT' WRITE ACCT-REC FROM IN-REC(1:300)
                   WHEN 'XREF' WRITE XREF-REC FROM IN-REC(1:50)
                   WHEN 'DISC' WRITE DISC-REC FROM IN-REC(1:50)
                   WHEN 'TCAT' WRITE TCAT-REC FROM IN-REC(1:50)
                 END-EVALUATE
                 IF OUT-STAT NOT = '00'
                   DISPLAY 'WRITE FAILED ' WS-KIND ' STATUS ' OUT-STAT
                   MOVE 8 TO RETURN-CODE STOP RUN
                 END-IF
                 ADD 1 TO WS-COUNT
             END-READ
           END-PERFORM
           EVALUATE WS-KIND
             WHEN 'ACCT' CLOSE ACCT-FILE
             WHEN 'XREF' CLOSE XREF-FILE
             WHEN 'DISC' CLOSE DISC-FILE
             WHEN 'TCAT' CLOSE TCAT-FILE
           END-EVALUATE
           CLOSE IN-FILE
           DISPLAY 'LOADED ' WS-COUNT ' ' WS-KIND
           STOP RUN.
